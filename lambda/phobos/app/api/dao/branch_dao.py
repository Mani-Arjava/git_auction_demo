from datetime import datetime
from typing import List, Optional, Union
from sqlalchemy import select, func
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from ..services.search_filter.basequery import BaseQueryParams
from ..model.branch.branch_table import BranchTable
from ..model.reappraisal_service.reappraisal_service_table import ReappraisalServiceTable
from ..model.enum.reappraisal_service_status_enum import ReappraisalServiceStatusEnum
from  ..dao.dao import DAO


class BranchDao:
    dao: DAO[BranchTable, str]

    def __init__(self, session: AsyncSession):
        self.dao = DAO[BranchTable, str](session, BranchTable)

    async def create_branch(self, branch: BranchTable) -> Optional[BranchTable]:
        return await self.dao.create_record(branch)

    async def get_branch_by_id_or_ids(
        self, branch_ids: Union[str, List[str]]
    ) -> Union[Optional[BranchTable], List[BranchTable]]:
        return await self.dao.get_record_id(branch_ids)

    async def update_branch(
        self, branch_id: str, branch_updates: SQLModel
    ) -> Optional[BranchTable]:
        return await self.dao.update_record(branch_id, branch_updates)

    async def delete_branch(
        self, branch_id: str, soft_del: Optional[bool] = True
    ) -> bool:
        if soft_del:
            return await self.dao.delete_record(
                record_id=branch_id,
                field_name="deleted_at_epoch",
                time=int(datetime.now().timestamp()),
            )
        return await self.dao.delete_record(branch_id)

    async def get_branches(self, query: BaseQueryParams) -> List[BranchTable]:
        return await self.dao.get_records(query)

    async def count_active_reappraisal_services(self, branch_id: str) -> int:
        """Count active reappraisal services for a given branch"""
        statement = select(func.count(ReappraisalServiceTable.reappraisal_service_id)).where(
            ReappraisalServiceTable.rs_branch_id == branch_id,
            ReappraisalServiceTable.rs_status == ReappraisalServiceStatusEnum.ACTIVE
        )
        result = await self.dao.session.execute(statement)
        return result.scalar() or 0
