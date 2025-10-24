from typing import Annotated, Optional
from fastapi import Path
from sqlmodel import Column, Field, ForeignKey, Integer, Relationship, SQLModel, String
from typing import List, TYPE_CHECKING

from app.api.model.reappraisal_service.reappraisal_service_table import ReappraisalServiceTable
from app.api.model.general.generic_model import BaseTable
from app.api.model.general.generic_regex import (
    IdRegexPattern,
    SolIdRegexPattern,
    IFSCCodeRegexPattern,
    PostalCodeRegexPattern,
    PhoneNumberRegexPattern,
    EmailRegexPattern,
)

if TYPE_CHECKING:
    from ...model.bank.bank_table import BankTable


BranchIdPath = Annotated[
    int,
    Path(
        title="Branch ID",
        description="Auto-increment unique identifier for the branch",
        example=1,
    ),
]
BranchIDField = Field(
    sa_column=Column("br_id", Integer, primary_key=True, autoincrement=True),
    default=None,
    title="Branch ID",
    description="Auto-increment unique identifier for the branch",
    schema_extra={"examples": [1, 2, 3]},
)

BranchBankIdField = Field(
    sa_column=Column("br_bk_id", Integer, ForeignKey("bank.bk_id")),
    title="Bank ID",
    description="Unique identifier for the bank to which the branch belongs",
    schema_extra={"examples": [1, 2, 3]},
)

BranchNameField = Field(
    sa_column=Column("br_name", String(50), index=True),
    title="Branch Name",
    description="Name of the branch",
    schema_extra={"examples": ["sbi_branch"]},
)

BranchSolIdField = Field(
    sa_column=Column("br_sol_id", String(6), index=True, nullable=True),
    title="Branch SOL ID",
    description="Unique identifier for the branch in the bank's system",
    schema_extra={"examples": ["234567"], "pattern": SolIdRegexPattern},
)

BranchAddressField = Field(
    sa_column=Column("br_address_line1", String(500)),
    title="Branch Address Line 1",
    description="First line of the branch address",
    schema_extra={"examples": ["123 Main St,kk_road"]},
)


BranchPhoneField = Field(
    sa_column=Column("br_phone", String(15)),
    title="Branch Phone",
    description="Official contact mobile number of the branch (Indian mobile format only)",
    min_length=10,
    max_length=15,
    schema_extra={"examples": ["+91-9876543210", "+919123456789"], "pattern": PhoneNumberRegexPattern},
)
BranchEmailField = Field(
    sa_column=Column("br_email", String(100)),
    title="Branch Email",
    description="Contact email address of the branch",
    min_length=5,
    max_length=100,
    schema_extra={"examples": ["branch@bankname.com"], "pattern": EmailRegexPattern},
)

BankRelationship = Relationship(
    back_populates="branches", sa_relationship_kwargs={"lazy": "selectin"}
)
ReappraisalServiceRelationship = Relationship(
    back_populates="branch",
    sa_relationship_kwargs={"lazy": "selectin"}
)

class BranchTable(BaseTable, table=True):
    __tablename__ = "branch"
    branch_id: int = BranchIDField
    branch_bank_id: int = BranchBankIdField
    branch_name: str = BranchNameField
    branch_sol_id: str = BranchSolIdField
    branch_address: str = BranchAddressField
    branch_phone: str = BranchPhoneField
    branch_email: str = BranchEmailField
    bank: "BankTable" = BankRelationship
    service: List["ReappraisalServiceTable"] = ReappraisalServiceRelationship

    # Generate BRN-0001 formatted ID dynamically
    @property
    def formatted_branch_id(self) -> Optional[str]:
        if self.branch_id is not None:
            return f"BRN-{self.branch_id:04d}"
        return None

