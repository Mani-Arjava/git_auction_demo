from datetime import datetime
from typing import List, Optional
from sqlalchemy import select
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from app.api.model.advance.advance_table import ReappraisalServiceAdvanceTable
from app.api.model.reimbursement.reimbursement_table import (
    ReappraisalServiceReimbursementTable,
)
from app.api.dao.dao import DAO
from app.api.services.search_filter.basequery import BaseQueryParams


class ReappraisalServiceReimbursementDAO:
    dao: DAO[ReappraisalServiceReimbursementTable, str]

    def __init__(self, session: AsyncSession):
        self.dao = DAO[ReappraisalServiceReimbursementTable, str](
            session, ReappraisalServiceReimbursementTable
        )

    async def create_rs_reimbursement(
        self, reimbursement: ReappraisalServiceReimbursementTable
    ) -> Optional[ReappraisalServiceReimbursementTable]:
        return await self.dao.create_record(reimbursement)

    async def get_rs_reimbursement(
        self, rs_reimbursement_id: str
    ) -> Optional[ReappraisalServiceReimbursementTable]:
        return await self.dao.get_record_id(rs_reimbursement_id)

    async def update_rs_reimbursement(
        self, rs_reimbursement_id: str, reimbursement_update: SQLModel
    ) -> Optional[ReappraisalServiceReimbursementTable]:
        return await self.dao.update_record(rs_reimbursement_id, reimbursement_update)

    async def delete_rs_reimbursement(
        self, rs_reimbursement_id: str, soft_del: bool = True
    ) -> bool:
        if soft_del:
            return await self.dao.delete_record(
                record_id=rs_reimbursement_id,
                field_name="deleted_at_epoch",
                time=int(datetime.now().timestamp()),
            )
        return await self.dao.delete_record(rs_reimbursement_id)

    async def get_rs_reimbursements(
        self, query: BaseQueryParams
    ) -> List[ReappraisalServiceReimbursementTable]:
        return await self.dao.get_records(query)

    async def get_total_reimbursement_amount(self, reappraisal_service_id: str) -> int:
        return await self.dao.get_total(
            amount_column=ReappraisalServiceReimbursementTable.rs_reimbursement_amount,
            filter_column=ReappraisalServiceReimbursementTable.rs_reappraisal_service_id,
            filter_value=reappraisal_service_id,
        )

    async def get_total_reimbursement_amount(self, reappraisal_service_id: str) -> int:
        return await self.dao.get_total(
            amount_column=ReappraisalServiceReimbursementTable.rs_reimbursement_amount,
            filter_column=ReappraisalServiceReimbursementTable.rs_reappraisal_service_id,
            filter_value=reappraisal_service_id,
        )
