from typing import Annotated, Optional, TYPE_CHECKING
from fastapi import Path, Query
from sqlmodel import Column, Field, ForeignKey, Integer, Relationship, SQLModel, String
from typing import List

from app.api.model.reappraisal_service.reappraisal_service_table import ReappraisalServiceTable
from app.api.model.general.generic_model import BaseTable
from app.api.model.general.generic_regex import (
    BanknameRegexPattern,
    BankCodeRegexPattern,
    AddressRegexPattern,
    EmailRegexPattern,
    PhoneNumberRegexPattern,
)

if TYPE_CHECKING:
    from ...model.branch.branch_table import BranchTable

BankIdPath = Annotated[
    int,
    Path(
        title="Bank ID",
        description="Auto-increment unique identifier for the bank",
        example=1,
    ),
]
BankIdQuery = Annotated[
    int,
    Query(
        title="Bank ID",
        description="Auto-increment unique identifier for the bank",
        example=1,
    ),
]

BankIDField = Field(
    #   default=None,  # Remove UUID auto-generation
      sa_column=Column("bk_id", Integer, primary_key=True, autoincrement=True),
      title="Bank ID",
      description="Auto-increment unique identifier for the bank",
      schema_extra={"examples": [1, 2, 3]},
  )

BankNameField = Field(
    sa_column=Column("bk_name", String(50), index=True, unique=True),
    title="Bank Name",
    description="Name of the bank",
    schema_extra={"examples": ["First National Bank"], "pattern": BanknameRegexPattern},
)
BankCodeField = Field(
    sa_column=Column("bk_code", String(5), index=True, unique=True),
    title="Bank Code",
    description="Code of the bank,Must be 2-5 uppercase letters only.",
    schema_extra={"examples": ["TNMB"], "pattern": BankCodeRegexPattern},
)
# BankTotalBranchesCountField = Field(
#     default="0",
#     sa_column=Column("total_branches_count", String(10), index=True, nullable=True),
#     title="Total Branches Count",
#     description="Total number of branches under the bank",
#     schema_extra={"examples": ["150"]},
# )
BankHeadOfficeAddressField = Field(
    sa_column=Column("bk_head_office_address", String(500)),
    title="Bank Head Office Address",
    description="Complete address of the bank's head office",
    schema_extra={"examples": ["123, Corporate Avenue, Mumbai, Maharashtra - 400001"], "pattern": AddressRegexPattern},
)
BankContactEmailField = Field(
    sa_column=Column("bk_contact_email", String(100)),
    title="Bank Contact Email",
    description="Official contact email address of the bank",
    schema_extra={"examples": ["contact@bankname.com"], "pattern": EmailRegexPattern},
)
BankContactNumberField = Field(
    sa_column=Column("bk_contact_number", String(15)),
    title="Bank Contact Number",
    description="Official contact mobile number of the bank (Indian mobile format only)",
    schema_extra={"examples": ["+91-9876543210", "+919123456789"], "pattern": PhoneNumberRegexPattern},
)
BranchRelationship = Relationship(
    back_populates="bank", sa_relationship_kwargs={"lazy": "selectin"}
)
ReappraisalServiceRelationship = Relationship(
    back_populates="bank", sa_relationship_kwargs={"lazy": "selectin"}
)

class BankTable(BaseTable, table=True):
    __tablename__ = "bank"
    bank_id: int = BankIDField
    bank_name: str = BankNameField
    bank_code: str = BankCodeField
    bank_head_office_address: str = BankHeadOfficeAddressField
    bank_contact_email: str = BankContactEmailField
    bank_contact_number: str = BankContactNumberField
    branches: List["BranchTable"] = BranchRelationship
    service: List["ReappraisalServiceTable"] = ReappraisalServiceRelationship

    # Generate BNK-0001 formatted ID dynamically
    @property
    def formatted_bank_id(self) -> Optional[str]:
        if self.bank_id is not None:
            return f"BNK-{self.bank_id:04d}"
        return None
