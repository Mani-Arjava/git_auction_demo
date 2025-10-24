from typing import List
from ...model.bank.bank_table import (
    BankIdPath, BankIDField, BankNameField, BankCodeField,
    BankHeadOfficeAddressField, BankContactEmailField, BankContactNumberField
)
from sqlmodel import SQLModel
from ...model.branch.branch_get import BranchGetResponse, BranchWithServicesCountResponse
from pydantic import computed_field


class BankGetResponse(SQLModel):
    bank_id: str  # Formatted as "BNK-0001"
    bank_name: str
    bank_code: str
    bank_head_office_address: str
    bank_contact_email: str
    bank_contact_number: str
    branches: List["BranchGetResponse"] = []

    @computed_field
    def total_branches_count(self) -> int:
        return len(self.branches or [])

    @computed_field
    def total_active_services_count(self) -> int:
        # This will be calculated when we have branch data with services
        return 0

    @classmethod
    def from_db_record(cls, bank_record):
        """Convert BankTable record to formatted response"""
        return cls(
            bank_id=f"BNK-{bank_record.bank_id:04d}",
            bank_name=bank_record.bank_name,
            bank_code=bank_record.bank_code,
            bank_head_office_address=bank_record.bank_head_office_address,
            bank_contact_email=bank_record.bank_contact_email,
            bank_contact_number=bank_record.bank_contact_number,
            branches=[]
        )


class BranchWithServicesCountResponse(SQLModel):
    branch_id: str
    branch_bank_id: str
    branch_name: str
    branch_sol_id: str
    branch_address: str
    branch_phone: str
    branch_email: str
    active_services_count: int = 0


class BankWithBranchServicesResponse(SQLModel):
    bank_id: str  # Formatted as "BNK-0001"
    bank_name: str
    bank_code: str
    bank_head_office_address: str
    bank_contact_email: str
    bank_contact_number: str
    branches: List[BranchWithServicesCountResponse] = []
    

    @computed_field
    def total_branches_count(self) -> int:
        return len(self.branches or [])

    @computed_field
    def total_active_services_count(self) -> int:
        return sum(branch.active_services_count for branch in self.branches)

    @classmethod
    def from_db_record(cls, bank_record):
        """Convert BankTable record to formatted response"""
        return cls(
            bank_id=f"BNK-{bank_record.bank_id:04d}",
            bank_name=bank_record.bank_name,
            bank_code=bank_record.bank_code,
            bank_head_office_address=bank_record.bank_head_office_address,
            bank_contact_email=bank_record.bank_contact_email,
            bank_contact_number=bank_record.bank_contact_number,
            branches=[]
        )

    @classmethod
    def from_response_type(cls, bank_response):
        """Convert BankGetResponse to BankWithBranchServicesResponse"""
        return cls(
            bank_id=bank_response.bank_id,
            bank_name=bank_response.bank_name,
            bank_code=bank_response.bank_code,
            bank_head_office_address=bank_response.bank_head_office_address,
            bank_contact_email=bank_response.bank_contact_email,
            bank_contact_number=bank_response.bank_contact_number,
            branches=[]
        )
