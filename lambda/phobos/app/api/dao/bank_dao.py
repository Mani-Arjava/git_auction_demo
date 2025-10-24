from datetime import datetime
from typing import List, Optional
from sqlalchemy import select, func
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from ..model.bank.bank_table import BankTable
from ..model.branch.branch_table import BranchTable
from ..model.bank.bank_get import BankGetResponse, BankWithBranchServicesResponse
from ..model.bank.bank_create import BankCreateResponse
from ..dao.dao import DAO
from ..services.search_filter.basequery import BaseQueryParams
from ..services.search_filter.matchtype_enum import MatchTypeEnum


class BankDao:
    dao: DAO[BankTable, int]

    def __init__(self, session: AsyncSession):
        self.dao = DAO[BankTable, int](session, BankTable)

    async def create_bank(self, bank: BankTable) -> Optional[BankCreateResponse]:
        bank_record = await self.dao.create_record(bank)
        if bank_record:
            return BankCreateResponse.from_db_record(bank_record)
        return None

    async def get_bank(self, bank_id: int) -> Optional[BankGetResponse]:
        bank_record = await self.dao.get_record_id(bank_id)
        if bank_record:
            return BankGetResponse.from_db_record(bank_record)
        return None

    async def update_bank(
        self, bank_id: int, bank_updates: SQLModel
    ) -> Optional[BankGetResponse]:
        bank_record = await self.dao.update_record(bank_id, bank_updates)
        if bank_record:
            return BankGetResponse.from_db_record(bank_record)
        return None

    async def delete_bank(self, bank_id: int, soft_del: Optional[bool] = True) -> bool:
        if soft_del:
            return await self.dao.delete_record(
                record_id=bank_id,
                field_name="deleted_at_epoch",
                time=int(datetime.now().timestamp()),
            )
        return await self.dao.delete_record(bank_id)

    async def get_banks(self, query: BaseQueryParams) -> List[BankGetResponse]:
        bank_records = await self.dao.get_records(query)
        return [BankGetResponse.from_db_record(bank) for bank in bank_records]

    async def count_branches(self, bank_id: int) -> int:
        """Count the number of branches for a given bank using back-population."""
        bank = await self.dao.session.get(BankTable, bank_id)
        if not bank:
            return 0
        # Due to lazy="selectin", branches will be loaded automatically
        return len(bank.branches) if bank.branches else 0
