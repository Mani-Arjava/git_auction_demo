from datetime import datetime
from typing import List, Optional
from sqlalchemy import select
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from app.api.model.advance.advance_table import (
    ReappraisalServiceAdvanceTable,
)
from app.api.dao.dao import DAO

from app.api.services.search_filter.basequery import BaseQueryParams

from app.api.services.search_filter.basequery import BaseQueryParams


class ReappraisalServiceAdvanceDAO:
    dao: DAO[ReappraisalServiceAdvanceTable, str]

    def __init__(self, session: AsyncSession):
        self.dao = DAO[ReappraisalServiceAdvanceTable, str](
            session, ReappraisalServiceAdvanceTable
        )

    async def create_rs_advance(
        self, rs_advance: ReappraisalServiceAdvanceTable
    ) -> Optional[ReappraisalServiceAdvanceTable]:
        return await self.dao.create_record(rs_advance)

    async def get_rs_advance(
        self, rs_advance_id: str
    ) -> Optional[ReappraisalServiceAdvanceTable]:
        return await self.dao.get_record_id(rs_advance_id)

    async def update_rs_advance(
        self,
        rs_advance_id: str,
        rs_advance_update: SQLModel,
    ) -> Optional[ReappraisalServiceAdvanceTable]:
        return await self.dao.update_record(rs_advance_id, rs_advance_update)

    async def delete_rs_advance(
        self, rs_advance_id: str, soft_del: bool = True
    ) -> bool:
        if soft_del:
            return await self.dao.delete_record(
                record_id=rs_advance_id,
                field_name="deleted_at_epoch",
                time=int(datetime.now().timestamp()),
            )
        return await self.dao.delete_record(rs_advance_id)

    async def get_rs_advances(
        self, query: BaseQueryParams
    ) -> List[ReappraisalServiceAdvanceTable]:
        return await self.dao.get_records(query)

    async def get_total_advance_amount(self, reappraisal_service_id: str) -> int:
        return await self.dao.get_total(
            amount_column=ReappraisalServiceAdvanceTable.rs_advance_amount,
            filter_column=ReappraisalServiceAdvanceTable.reappraisal_service_id,
            filter_value=reappraisal_service_id,
        )
