from datetime import datetime
from typing import List, Optional
from sqlalchemy import select
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from app.api.model.reappraisal_service.reappraisal_service_table import (
    ReappraisalServiceTable,
)
from app.api.dao.dao import DAO
from app.api.services.search_filter.basequery import BaseQueryParams


class ReappraisalServiceDAO:
    dao: DAO[ReappraisalServiceTable, str]

    def __init__(self, session: AsyncSession):
        self.dao = DAO[ReappraisalServiceTable, str](session, ReappraisalServiceTable)

    async def create_reappraisal_service(
        self, reappraisal_service: ReappraisalServiceTable
    ) -> Optional[ReappraisalServiceTable]:
        return await self.dao.create_record(reappraisal_service)

    async def get_reappraisal_service(
        self, reappraisal_service_id: str
    ) -> Optional[ReappraisalServiceTable]:
        return await self.dao.get_record_id(reappraisal_service_id)

    async def update_reappraisal_service(
        self, reappraisal_service_id: str, reappraisal_service_update: SQLModel
    ) -> Optional[ReappraisalServiceTable]:
        return await self.dao.update_record(
            reappraisal_service_id, reappraisal_service_update
        )

    async def delete_reappraisal_service(
        self, reappraisal_service_id: str, soft_del: bool = True
    ) -> bool:
        if soft_del:
            return await self.dao.delete_record(
                record_id=reappraisal_service_id,
                field_name="deleted_at_epoch",
                time=int(datetime.now().timestamp()),
            )
        return await self.dao.delete_record(reappraisal_service_id)

    async def get_reappraisal_services(
        self, query: BaseQueryParams
    ) -> List[ReappraisalServiceTable]:
        return await self.dao.get_records(query)
