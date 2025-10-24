from typing import List, Optional
from pydantic import computed_field
from sqlmodel import SQLModel
from ...model.branch.branch_table import (
    BranchIDField,
    BranchNameField,
    BranchSolIdField,
    BranchAddressField,
    BranchPhoneField,
    BranchEmailField,
    BranchBankIdField,
)
from ...model.bank.bank_table import BankTable


class BranchGetResponse(SQLModel):
    branch_id: str  # Formatted as "BRN-0001"
    bank_id: str  # Formatted as "BNK-0001"
    branch_name: str = BranchNameField
    branch_sol_id: str = BranchSolIdField
    branch_address: str = BranchAddressField
    branch_phone: str = BranchPhoneField
    branch_email: str = BranchEmailField
    bank: BankTable | None = None

    @computed_field
    def has_services(self) -> bool:
        # Will be calculated when we have service data
        return False

    @classmethod
    def from_db_record(cls, branch_record, bank_name=None):
        """Convert BranchTable record to formatted response"""
        return cls(
            branch_id=f"BRN-{branch_record.branch_id:04d}",
            bank_id=f"BNK-{branch_record.branch_bank_id:04d}",
            branch_name=branch_record.branch_name,
            branch_sol_id=branch_record.branch_sol_id or "",
            branch_address=branch_record.branch_address,
            branch_phone=branch_record.branch_phone,
            branch_email=branch_record.branch_email,
            bank=None
        )


class BranchWithServicesCountResponse(SQLModel):
    branch_id: str = BranchIDField
    branch_bank_id: str = BranchBankIdField
    branch_name: str = BranchNameField
    branch_sol_id: str = BranchSolIdField
    branch_address: str = BranchAddressField
    branch_phone: str = BranchPhoneField
    branch_email: str = BranchEmailField
    active_services_count: int = 0
