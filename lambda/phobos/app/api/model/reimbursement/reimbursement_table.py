from typing import Annotated, Optional
import uuid
from fastapi import Path
from sqlmodel import (
    Column,
    Enum,
    Field,
    ForeignKey,
    Integer,
    Relationship,
    String,
)
from typing import List, TYPE_CHECKING
from app.api.model import enum
from app.api.model.enum.settlement_status_enum import SettlementStatusEnum
from app.api.model.general.generic_regex import DescriptionRegexPattern, FilePathRegexPattern
from app.api.model.enum.service_category_enum import ReappraisalServiceCategoryEnum
from app.api.model.general.generic_model import BaseTable
from app.api.model.general.generic_regex import IdRegexPattern

if TYPE_CHECKING:
    from app.api.model.reappraisal_service.reappraisal_service_table import (
        ReappraisalServiceTable,
    )
    from app.api.model.reimbursement_settlement.reimbursement_settlement_table import (
        ReimbursementSettlementTable,
    )


ReappraisalServiceReimbursementIdPath = Annotated[
    str,
    Path(
        title="Reappraisal Service Reimbursement ID",
        description="Unique identifier for the reappraisal service reimbursement, formatted as a UUID.",
        example="123e4567-e89b-12d3-a456-426614174000",
        pattern=IdRegexPattern,
        regex=IdRegexPattern,
    ),
]
ReappraisalServiceReimbursementIDField = Field(
    default_factory=lambda: str(uuid.uuid4()),
    sa_column=Column("rsr_id", String(36), primary_key=True),
    title="Reappraisal Service Reimbursement ID",
    description="Unique identifier for the reappraisal service reimbursement, formatted as a UUID.",
    schema_extra={
        "examples": ["123e4567-e89b-12d3-a456-426614174000"],
        "pattern": IdRegexPattern,
    },
)
ReappraisalServiceIDField = Field(
    sa_column=Column("rs_id", String(36), ForeignKey("reappraisal_service.rs_id")),
    title="Reappraisal Service ID",
    description="Unique identifier for the reappraisal service, formatted as a UUID.",
    schema_extra={
        "examples": ["123e4567-e89b-12d3-a456-426614174000"],
        "pattern": IdRegexPattern,
    },
)
ReappraisalServiceReimbursementTransactionEpochField = Field(
    sa_column=Column(
        "rsr_transaction_epoch",
        Integer,
    ),
    title="Reimbursement Transaction Epoch",
    description="Epoch time (Unix timestamp) for the reimbursement transaction.",
    ge=0,
    schema_extra={"examples": [1700000000]},
)
ReappraisalReimbursementCategoryField = Field(
    sa_column=Column("rsr_category", Enum(ReappraisalServiceCategoryEnum), index=True),
    title="Reimbursement Category",
    description="Category of the reimbursement, such as food, travel, stay, or miscellaneous.",
    schema_extra={"examples": ["FOOD"]},
)
ReappraisalServiceReimbursmentDetailsField = Field(
    sa_column=Column(
        "rsr_details",
        String(255),
    ),
    title="Reimbursement Details",
    description="Details of the reimbursement, such as specific expenses or notes.",
    schema_extra={
        "examples": ["Lunch expenses for the reappraisal team"],
        "pattern": DescriptionRegexPattern,
    },
)
ReappraisalServiceReimbursementAmountField = Field(
    sa_column=Column(
        "rsr_amount",
        Integer,
    ),
    title="Reimbursement Amount",
    description="Amount of the reimbursement in paisa (1 paisa = 0.01 INR).",
    ge=0,
    schema_extra={"examples": [5000]},  # rupees = stored_paisa / 100
)
ReappraisalServiceReimbursementFilePathField = Field(
    default=None,
    sa_column=Column("rsr_file_path", String(255), nullable=True),
    title="Reimbursement File Path",
    description="Optional file path associated with the reimbursement, formatted as a link.",
    schema_extra={
        "examples": ["https://mybucket/documents/document.pdf"],
        "pattern": FilePathRegexPattern,
    },
)

ServiceRelationship = Relationship(
    back_populates="reimbursements", sa_relationship_kwargs={"lazy": "selectin"}
)
ReappraisalServiceReimbursementSettlementStatusField = Field(
    sa_column=Column("rsr_settlement_status", Enum(SettlementStatusEnum), index=True),
    title="Reimbursement Settlement Status",
    description="Status of the reimbursement statement.",
    schema_extra={"examples": ["UNSETTLED"]},
)

SettlementsRelationship = Relationship(
    back_populates="reimbursement",
    sa_relationship_kwargs={"lazy": "selectin"},
)


class ReappraisalServiceReimbursementTable(BaseTable, table=True):
    __tablename__ = "reappraisal_service_reimbursement"

    rs_reimbursement_id: str = ReappraisalServiceReimbursementIDField
    rs_reappraisal_service_id: str = ReappraisalServiceIDField
    rs_reimbursement_transaction_epoch: int = (
        ReappraisalServiceReimbursementTransactionEpochField
    )
    rs_reimbursement_category: ReappraisalServiceCategoryEnum = (
        ReappraisalReimbursementCategoryField
    )
    rs_reimbursement_details: str = ReappraisalServiceReimbursmentDetailsField
    rs_reimbursement_amount: int = ReappraisalServiceReimbursementAmountField
    rs_reimbursement_file_path: Optional[str] = (
        ReappraisalServiceReimbursementFilePathField
    )
   
    service: "ReappraisalServiceTable" = ServiceRelationship
   
