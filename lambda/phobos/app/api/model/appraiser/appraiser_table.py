from typing import Annotated, ClassVar, Optional
from fastapi import Path, Query
from sqlmodel import Column, Enum, Field, Index, Integer, Relationship, String
from typing import List, TYPE_CHECKING
from app.api.model.general.generic_model import BaseTable
from app.api.model.general.generic_regex import (
    NameRegexPattern,
    IdRegexPattern,
    EmailRegexPattern,
    PhoneNumberRegexPattern,
    PanCardRegexPattern,
    AccountNumberRegexPattern,
    IFSCCodeRegexPattern,
    AddressRegexPattern,
    BanknameRegexPattern,
    AppraiserIdRegexPattern,
)
from app.api.model.enum.gender_enum import GenderEnum
from sqlalchemy.ext.hybrid import hybrid_property
from app.api.model.reappraisal_service.reappraisal_service_table import (
    ReappraisalServiceTable,
)



AppraiserIdPath = Annotated[
    int,
    Path(
        title="Appraiser ID",
        description="Auto-increment unique identifier for the appraiser",
        example=1,
    ),
]
AppraiserIDQuery = Annotated[
    int,
    Query(
        title="Appraiser ID",
        description="Auto-increment unique identifier for the appraiser",
        example=1,
    ),
]

AppraiserIDField = Field(
    default=None,
    sa_column=Column("ap_id", Integer, primary_key=True, autoincrement=True),
    title="Appraiser ID",
    description="Auto-increment unique identifier for the appraiser",
    schema_extra={"examples": [1, 2, 3]},
)

AppraiserFullNameField = Field(
    sa_column=Column("ap_full_name", String(100)),
    title="Appraiser Full Name",
    description="Full name of the appraiser",
    schema_extra={"examples": ["John Doe"], "pattern": NameRegexPattern},
)

AppraiserEmailField = Field(
    sa_column=Column("ap_email", String(50),unique=True),
    title="Appraiser Email",
    description="Email address of the appraiser",
    schema_extra={"examples": ["john.doe@example.com"], "pattern": EmailRegexPattern},
)

AppraiserPhoneField = Field(
    sa_column=Column("ap_phone", String(15), index=True,unique=True),
    title="Appraiser Phone",
    description="Phone number of the appraiser",
    schema_extra={"examples": ["+91-9876543210"], "pattern": PhoneNumberRegexPattern},
)
AppraiserPanField = Field(
    sa_column=Column("ap_pan", String(10), unique=True),
    title="Appraiser PAN",
    description="PAN number of the appraiser",
    schema_extra={"examples": ["ABCDE1234F"], "pattern": PanCardRegexPattern},
)
AppraiserAccountNumberField = Field(
    sa_column=Column("ap_account_number", String(20),unique=True),
    title="Appraiser Account Number",
    description="Bank account number of the appraiser",
    schema_extra={"examples": ["12345678901234"], "pattern": AccountNumberRegexPattern},
)
AppraiserAccountIFSCCodeField = Field(
    sa_column=Column("ap_account_ifsc_code", String(11)),
    title="Appraiser Account IFSC Code",
    description="IFSC code of the appraiser's bank account",
    schema_extra={"examples": ["SBIN0001234"], "pattern": IFSCCodeRegexPattern},
)

AppraiserAddressField = Field(
    sa_column=Column("ap_address", String(500)),
    title="Appraiser Address",
    description="Complete address of the appraiser",
    schema_extra={"examples": ["123, Main Street, City, State - 600001"], "pattern": AddressRegexPattern},
)

AppraiserBankNameField = Field(
    sa_column=Column("ap_bank_name", String(100)),
    title="Appraiser Bank Name",
    description="Name of the appraiser's bank",
    schema_extra={"examples": ["State Bank of India"]},
)

AppraiserBranchNameField = Field(
    sa_column=Column("ap_branch_name", String(100)),
    title="Appraiser Branch Name",
    description="Name of the appraiser's bank branch",
    schema_extra={"examples": ["Main Branch"]},
)

ServiceRelationship = Relationship(
    back_populates="appraiser", sa_relationship_kwargs={"lazy": "selectin"}
)



def make_optional(field: Field) -> Field:
    field.default = None
    return field


class AppraiserTable( BaseTable, table=True):
    __tablename__ = "appraiser"

    appraiser_id: int = AppraiserIDField
    appraiser_full_name: str = AppraiserFullNameField
    appraiser_email: str = AppraiserEmailField
    appraiser_phone: str = AppraiserPhoneField
    appraiser_pan: str = AppraiserPanField
    appraiser_account_number: str = AppraiserAccountNumberField
    appraiser_account_ifsc_code: str = AppraiserAccountIFSCCodeField
    appraiser_address: str = AppraiserAddressField
    appraiser_bank_name: str = AppraiserBankNameField
    appraiser_branch_name: str = AppraiserBranchNameField

    # Relationships
    services: List["ReappraisalServiceTable"] = ServiceRelationship
   

    __table_args__ = (Index("ix_appraiser_fullname", "ap_full_name"),)

    # Generate APR-0001 formatted ID dynamically
    @property
    def formatted_appraiser_id(self) -> Optional[str]:
        if self.appraiser_id is not None:
            return f"APR-{self.appraiser_id:04d}"
        return None
