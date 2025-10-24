from math import ceil
from sqlalchemy import func
from typing import Any, Generic, List, Optional, Tuple, Type, TypeVar, Union
from sqlmodel import SQLModel, and_, inspect, or_, select, cast, String
from sqlmodel.ext.asyncio.session import AsyncSession
from app.api.services.search_filter.basequery import BaseQueryParams
from app.api.services.search_filter.searchfilter import T, DAOFilterSearchParam, MatchTypeEnum
from app.api.services.pagination.pagination import PaginationData, PaginationResponse
from sqlalchemy.orm import class_mapper, selectinload

DAOModel = TypeVar("DAOModel", bound=SQLModel)
DAORecordId = TypeVar("DAORecordId")


class DAO(Generic[DAOModel, DAORecordId]):

    session: AsyncSession
    model_class: type[DAOModel]

    def __init__(self, session: AsyncSession, model_class: type[DAOModel]):
        self.session = session
        self.model_class = model_class

    async def create_record(self, record: DAOModel, is_commit: bool = True) -> DAOModel:
        self.session.add(record)
        if is_commit:
            await self.session.commit()
            await self.session.refresh(record)
        return record

    async def get_record_id(self, record_id: DAORecordId) -> Optional[DAOModel]:
        result = await self.session.get(self.model_class, record_id)
        if not result:
            return None
        if result.deleted_at_epoch == -1:
            return result

    async def get_records(self, include_deleted: bool = False) -> List[DAOModel]:
        query = select(self.model_class)

        # Exclude soft-deleted records unless include_deleted=True
        if not include_deleted and hasattr(self.model_class, "deleted_at_epoch"):
            query = query.where(self.model_class.deleted_at_epoch == -1)

        result = await self.session.exec(query)
        return result.all()
    
    async def update_record(
        self, record_id: DAORecordId, record_updates: SQLModel
    ) -> Optional[DAOModel]:
        record = await self.get_record_id(record_id)
        if record:
            record_data = record_updates.model_dump(exclude_unset=True)
            for key, value in record_data.items():
                setattr(record, key, value)
            await self.session.commit()
            await self.session.refresh(record)
        return record

    async def delete_record(
        self,
        record_id: DAORecordId,
        field_name: DAORecordId,
        time: Any,
        is_commit: bool = True,
    ) -> bool:
        record = await self.get_record_id(record_id)
        if record:
            if field_name and time:
                if hasattr(record, field_name):
                    setattr(record, field_name, time)
                    if is_commit:
                        await self.session.commit()
                        await self.session.refresh(record)
                    return record
            else:
                await self.session.delete(record)
                if is_commit:
                    await self.session.commit()
                return True
        return False

    async def get_records_functionalities(
        self, query: BaseQueryParams
    ) -> Union[List[T], PaginationResponse[T]]:
        stmt = select(self.model_class)
        filters = []
        joined_rels: set[Type[SQLModel]] = set()

        for value, field_info in zip(query.search_values, query.fields):
            if value is None or (isinstance(value, str) and not value.strip()):
                continue

            # --- Unpack field info safely ---
            if isinstance(field_info, tuple):
                if isinstance(field_info[0], tuple):
                    # EPOCH_RANGE: ((start_field, end_field), match_type)
                    field, match_type = field_info
                else:
                    # Regular (field, match_type)
                    field, match_type = field_info
            else:
                # Single string field
                field, match_type = field_info, MatchTypeEnum.EXACT

            condition = None

            # --- Apply filter based on MatchTypeEnum ---
            if match_type == MatchTypeEnum.EPOCH_RANGE:
                start_field, end_field = field
                stmt, condition = await DAOFilterSearchParam.epoch_date(
                    stmt, self.model_class, value, start_field, end_field, joined_rels
                )

            elif match_type == MatchTypeEnum.FILE_PATH_STATUS:
                condition = await DAOFilterSearchParam.file_path_filter(
                    self.model_class, field, value
                )

            else:
                # Generic filter for str/int fields
                filter_obj = DAOFilterSearchParam[T](
                    model_class=self.model_class,
                    field=field,
                    match_type=match_type,
                    value=value,
                    stmt=stmt,
                    joined_rels=joined_rels,
                )
                stmt, condition = await filter_obj.generic_filter()

            if condition is not None:
                filters.append(condition)

        # Apply soft delete filter
        filters.append(self.model_class.deleted_at_epoch == -1)

        # Combine all filters
        if filters:
            stmt = stmt.where(and_(*filters))

        # Pagination
        if getattr(query, "page", None) and getattr(query, "size", None):
            return await self.paginate(stmt, query.page, query.size)

        result = await self.session.exec(stmt)
        items = result.unique().all()
        # Force relationship loading while session is active
        for item in items:
            for relationship_name in class_mapper(
                self.model_class
            ).relationships.keys():
                try:
                    getattr(item, relationship_name)  # Trigger loading
                except:
                    pass  # Ignore errors

        return items

    async def paginate(
        self,
        stmt: select,
        page: int,
        size: int,
    ) -> PaginationResponse[Any]:

        # count total
        count_query = select(func.count()).select_from(stmt.subquery())
        total_count = (await self.session.exec(count_query)).one()

        # fetch page
        offset = (page - 1) * size
        result = await self.session.exec(stmt.limit(size).offset(offset))

        total_pages = ceil(total_count / size) if size else 1

        return PaginationResponse(
            items=result.all(),
            pagination_data=PaginationData(
                total_data=total_count,
                page=page,
                size=size,
                pages=total_pages,
            ),
        )

    async def build_s3_key_prefix(
        appraiser_id: str,
        reappraisal_service_id: str,
        category: str,
        reimbursement_id: str | None = None,
    ) -> str:
        """
        Builds an S3 key prefix dynamically based on category.
        """
        base_prefix = f"{appraiser_id}/reappraisal/{reappraisal_service_id}"

        if category == "completion_certificates":
            return f"{base_prefix}/completion_certificates"

        elif category == "reimbursement_proofs" and reimbursement_id:
            return f"{base_prefix}/reimbursement_proofs/{reimbursement_id}"

        elif category == "authorization_letters":
            return f"{base_prefix}/authorization_letters"
        else:
            raise ValueError(
                f"Invalid category '{category}' or missing reimbursement_id"
            )

    async def get_total(self, amount_column, filter_column, filter_value) -> int:
        result = await self.session.exec(
            select(func.coalesce(func.sum(amount_column), 0)).where(
                filter_column == filter_value, self.model_class.deleted_at_epoch == -1
            )
        )
        return result.first()
