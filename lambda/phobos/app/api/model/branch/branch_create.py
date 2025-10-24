from typing import Optional
from sqlmodel import SQLModel
from ...model.branch.branch_table import (
    BranchNameField,
    BranchSolIdField,
    BranchAddressField,
    BranchPhoneField,
    BranchEmailField,
    BranchBankIdField,
)


class BranchCreateRequest(SQLModel):
    branch_bank_id: int  # Accept integer ID, will be formatted in response
    branch_name: str = BranchNameField
    branch_sol_id: str = BranchSolIdField
    branch_address: str = BranchAddressField
    branch_phone: str = BranchPhoneField
    branch_email: str = BranchEmailField


class BranchCreateResponse(SQLModel):
    branch_id: str  # Formatted as "BRN-0001"
    bank_id: str  # Formatted as "BNK-0001"
    branch_name: str = BranchNameField
    branch_sol_id: str = BranchSolIdField
    branch_address: str = BranchAddressField
    branch_phone: str = BranchPhoneField
    branch_email: str = BranchEmailField

    @classmethod
    def from_db_record(cls, branch_record):
        """Convert BranchTable record to formatted response"""
        return cls(
            branch_id=f"BRN-{branch_record.branch_id:04d}",
            bank_id=f"BNK-{branch_record.branch_bank_id:04d}",
            branch_name=branch_record.branch_name,
            branch_sol_id=branch_record.branch_sol_id or "",
            branch_address=branch_record.branch_address,
            branch_phone=branch_record.branch_phone,
            branch_email=branch_record.branch_email
        )


class BranchUpdateResponse(SQLModel):
    branch_id: str  # Formatted as "BRN-0001"
    bank_id: str  # Formatted as "BNK-0001"
    branch_name: str = BranchNameField
    branch_sol_id: str = BranchSolIdField
    branch_address: str = BranchAddressField
    branch_phone: str = BranchPhoneField
    branch_email: str = BranchEmailField

    @classmethod
    def from_db_record(cls, branch_record):
        """Convert BranchTable record to formatted response"""
        return cls(
            branch_id=f"BRN-{branch_record.branch_id:04d}",
            bank_id=f"BNK-{branch_record.branch_bank_id:04d}",
            branch_name=branch_record.branch_name,
            branch_sol_id=branch_record.branch_sol_id or "",
            branch_address=branch_record.branch_address,
            branch_phone=branch_record.branch_phone,
            branch_email=branch_record.branch_email
        )


class BranchUpdateRequest(SQLModel):
    branch_name: Optional[str] = None
    branch_sol_id: Optional[str] = None
    branch_address: Optional[str] = None
    branch_phone: Optional[str] = None
    branch_email: Optional[str] = None
