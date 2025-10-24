from datetime import datetime
from typing import List, Optional
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from app.api.model.appraiser.appraiser_table import AppraiserTable
from app.api.model.reappraisal_service.reappraisal_service_table import ReappraisalServiceTable
from app.api.model.enum.reappraisal_service_status_enum import ReappraisalServiceStatusEnum
from app.api.dao.dao import DAO
from app.api.services.search_filter.basequery import BaseQueryParams


class AppraiserDAO:
    dao: DAO[AppraiserTable, str]

    def __init__(self, session: AsyncSession):
        self.dao = DAO[AppraiserTable, str](session, AppraiserTable)

    async def create_appraiser(
        self, appraiser: AppraiserTable
    ) -> Optional[AppraiserTable]:
        return await self.dao.create_record(appraiser)

    async def get_appraiser(self, appraiser_id: str) -> Optional[AppraiserTable]:
        return await self.dao.get_record_id(appraiser_id)

    async def update_appraiser(
        self, appraiser_id: str, appraiser_update: SQLModel
    ) -> Optional[AppraiserTable]:
        return await self.dao.update_record(appraiser_id, appraiser_update)

    async def delete_appraiser(self, appraiser_id: str, soft_del: bool = True) -> bool:
        if soft_del:
            return await self.dao.delete_record(
                record_id=appraiser_id,
                field_name="deleted_at_epoch",
                time=int(datetime.now().timestamp()),
            )

        return await self.dao.delete_record(appraiser_id)

    # async def get_appraisers(self, query: BaseQueryParams) -> List[AppraiserTable]:
    #     return await self.dao.get_records(query)
    async def get_appraisers(self, include_deleted: bool = False) -> List[AppraiserTable]:
        return await self.dao.get_records(include_deleted=include_deleted)

    async def get_pan(self, appraiser_id: str) -> str | None:
        result = await self.dao.session.get(AppraiserTable, appraiser_id)
        return result.appraiser_pan if result else None

    async def get_bank_account(self, appraiser_id: str) -> str | None:
        result = await self.dao.session.get(AppraiserTable, appraiser_id)
        return result.appraiser_account_number if result else None

    async def count_services(self, appraiser_id: str) -> int:
        """Count the number of reappraisal services associated with this appraiser using back-population."""
        appraiser = await self.dao.session.get(AppraiserTable, appraiser_id)
        if not appraiser:
            return 0
        # Due to lazy="selectin", services will be loaded automatically
        return len(appraiser.services) if appraiser.services else 0

    async def get_appraisers_with_active_count(self):
        from sqlalchemy import cast, String
        query = (
            select(
                AppraiserTable,
                func.count(ReappraisalServiceTable.reappraisal_service_id).label("active_services_count")
            )
            .join(
                ReappraisalServiceTable,
                (ReappraisalServiceTable.rs_appraiser_id == cast(AppraiserTable.appraiser_id, String)) &
                (ReappraisalServiceTable.rs_status == "ACTIVE"),
                isouter=True
            )
            .group_by(AppraiserTable.appraiser_id)
        )

        result = await self.dao.session.exec(query)
        return result.all()


    async def get_active_services(self, appraiser_id: str) -> List[ReappraisalServiceTable]:
        """Get only ACTIVE reappraisal services for the appraiser."""
        query = select(ReappraisalServiceTable).options(
            selectinload(ReappraisalServiceTable.bank),
            selectinload(ReappraisalServiceTable.branch),
            selectinload(ReappraisalServiceTable.advances),
            selectinload(ReappraisalServiceTable.reimbursements)
        ).where(
            ReappraisalServiceTable.rs_appraiser_id == appraiser_id,
            ReappraisalServiceTable.rs_status == ReappraisalServiceStatusEnum.ACTIVE
        )
        result = await self.dao.session.exec(query)
        return result.scalars().all()