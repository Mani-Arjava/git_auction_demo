from typing import Annotated, Optional
import uuid
from fastapi import Path
from sqlmodel import (
    Column,
    Field,
    ForeignKey,
    Integer,
    Relationship,
    String,
    Enum,
)
from typing import List, TYPE_CHECKING
from app.api.model import enum
from app.api.model.enum.reappraisal_service_status_enum import ReappraisalServiceStatusEnum
from app.api.model.general.generic_model import BaseTable
from app.api.model.general.generic_regex import (
    IdRegexPattern,
    FilePathRegexPattern,
    DescriptionRegexPattern
)

from app.api.model.enum.settlement_status_enum import SettlementStatusEnum
from app.api.model.advance.advance_table import (
    ReappraisalServiceAdvanceTable,
)

if TYPE_CHECKING:
    from app.api.model.appraiser.appraiser_table import AppraiserTable
    from app.api.model.reimbursement.reimbursement_table import (
        ReappraisalServiceReimbursementTable,
    )
    from app.api.model.bank.bank_table import BankTable
    from app.api.model.branch.branch_table import BranchTable
    

ReappraisalServiceIDPath = Annotated[
    str,
    Path(
        title="Reappraisal Service ID",
        description="Unique identifier for the reappraisal service, formatted as a UUID.",
        example="123e4567-e89b-12d3-a456-426614174000",
        pattern=IdRegexPattern,
        regex=IdRegexPattern,
    ),
]
ReappraisalServiceIDField = Field(
    default_factory=lambda: str(uuid.uuid4()),
    sa_column=Column("rs_id", String(36), primary_key=True),
    title="Reappraisal Service ID",
    description="Unique identifier for the reappraisal service, formatted as a UUID.",
    schema_extra={
        "examples": ["123e4567-e89b-12d3-a456-426614174000"],
        "pattern": IdRegexPattern,
    },
)
ReappraisalServiceAppraiserIDField = Field(
    sa_column=Column(
        "ap_id",
        String(36),
        ForeignKey("appraiser.ap_id"),
    ),
    title="Appraiser ID",
    description="Unique identifier for the appraiser associated with the reappraisal service.",
    schema_extra={
        "examples": ["123e4567-e89b-12d3-a456-426614174000"],
        "pattern": IdRegexPattern,
    },
)
ReappraisalServiceBankIdField = Field(
    sa_column=Column(
        "rs_bank_id",
        String(36),
        ForeignKey("bank.bk_id"),
    ),
    title="Bank ID",
    description="Unique identifier for the bank associated with the reappraisal service.",
    schema_extra={
        "examples": ["123e4567-e89b-12d3-a456-426614174000"],
        "pattern": IdRegexPattern,
    },
)

ReappraisalServiceBranchIdField = Field(
    sa_column=Column(
        "rs_branch_id",
        String(36),
        
        ForeignKey("branch.br_id"),
    ),
    title="Branch ID",
    description="Unique identifier for the branch associated with the reappraisal service.",
    schema_extra={
        "examples": ["123e4567-e89b-12d3-a456-426614174000"],
        "pattern": IdRegexPattern,
    },
)
ReappraisalServiceStartEpochField = Field(
    sa_column=Column(
        "rs_start_epoch",
        Integer,
    ),
    title="Start Epoch",
    description="Epoch time (Unix timestamp) for the start of the reappraisal service.",
    ge=0,  # Must be non-negative
    schema_extra={"examples": [1627814400]},
)
ReappraisalServiceEndEpochField = Field(
    sa_column=Column(
        "rs_end_epoch",
        Integer,
    ),
    title="End Epoch",
    description="Epoch time (Unix timestamp) for the end of the reappraisal service.",
    ge=0,  # Must be non-negative
    schema_extra={"examples": [1627900800]},
)
ReappraisalServicePacketCountField = Field(
    default=None,
    sa_column=Column(
        "rs_packet_count",
        Integer,
        nullable=True,
    ),
    title="Packet Count",
    description="Number of packets processed by the reappraisal service.",
    ge=0,
    schema_extra={"examples": [100]},
)
ReappraisalServiceChargeField = Field(
    default=0,
    sa_column=Column("rs_charge", Integer, nullable=False),
    title="Reappraisal Service Charge (in paisa)",
    description="Stored internally in paisa (1 rupee = 100 paisa).",
    ge=0,
    schema_extra={"examples": [50000]},  # stored as paisa
)
ReappraisalServiceStatusField = Field(
    default=ReappraisalServiceStatusEnum.ACTIVE,
    sa_column=Column("rs_status", Enum(ReappraisalServiceStatusEnum), index=True),
    title="Reappraisal Service Status",
    description="Current status of the reappraisal service.",
    schema_extra={"examples": ["ACTIVE"]},
)
ReappraisalServiceCompletionFilePathField = Field(
    default=None,
    sa_column=Column(
        "rs_file_path",
        String(255),
        nullable=True,
    ),
    title="File Path",
    description="S3 URL or key for the file associated with the reappraisal service document.",
    schema_extra={
        "examples": ["https://mybucket/doc/document.pdf"],
        "pattern": FilePathRegexPattern,
    },
)
ReappraisalServiceDescriptionsField = Field(
    default="",
    sa_column=Column(
        "rs_description",
        String(500),
        nullable=True,
        default="",
    ),
    title="Reappraisal Service Notes",
    description="Additional notes or descriptions for the reappraisal service.",
    schema_extra={"examples": ["Initial reappraisal service request."],"pattern":DescriptionRegexPattern },
)
AppraiserRelationship = Relationship(
    back_populates="services", sa_relationship_kwargs={"lazy": "selectin"}
)
ReimbursmentsRelationship = Relationship(
    back_populates="service", sa_relationship_kwargs={"lazy": "selectin"}
)
AdvancesRelationship = Relationship(
    back_populates="service", sa_relationship_kwargs={"lazy": "selectin"}
)
BankRelationship = Relationship(
    back_populates="service",
    sa_relationship_kwargs={"lazy": "selectin"}
)
BranchRelationship = Relationship(
    back_populates="service",
    sa_relationship_kwargs={"lazy": "selectin"}
)



class ReappraisalServiceTable(BaseTable, table=True):
    __tablename__ = "reappraisal_service"

    reappraisal_service_id: str = ReappraisalServiceIDField
    rs_appraiser_id: str = ReappraisalServiceAppraiserIDField
    rs_bank_id:str = ReappraisalServiceBankIdField
    rs_branch_id: str = ReappraisalServiceBranchIdField
    rs_start_epoch: int = ReappraisalServiceStartEpochField
    rs_end_epoch: int = ReappraisalServiceEndEpochField
    rs_packet_count: int = ReappraisalServicePacketCountField
    rs_charge: int = ReappraisalServiceChargeField
    rs_status: ReappraisalServiceStatusEnum = ReappraisalServiceStatusField
    rs_completion_file_path: Optional[str] = ReappraisalServiceCompletionFilePathField
    rs_description :str = ReappraisalServiceDescriptionsField

    appraiser: "AppraiserTable" = AppraiserRelationship
    bank : "BankTable" = BankRelationship
    branch : "BranchTable" = BranchRelationship
    reimbursements: List["ReappraisalServiceReimbursementTable"] = (
        ReimbursmentsRelationship
    )
    advances: List["ReappraisalServiceAdvanceTable"] = AdvancesRelationship
 