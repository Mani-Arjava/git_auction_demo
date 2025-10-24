from typing import Annotated
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
from app.api.model.enum.service_category_enum import ReappraisalServiceCategoryEnum
from app.api.model.enum.settlement_status_enum import SettlementStatusEnum
from app.api.model.general.generic_model import BaseTable
from app.api.model.general.generic_regex import DescriptionRegexPattern, IdRegexPattern

if TYPE_CHECKING:
    from app.api.model.reappraisal_service.reappraisal_service_table import (
        ReappraisalServiceTable,
    )
   

ReappraisalServiceAdvanceIdPath = Annotated[
    str,
    Path(
        title="Reappraisal Service Advance ID",
        description="Unique identifier for the reappraisal service advance, formatted as a UUID.",
        example="123e4567-e89b-12d3-a456-426614174000",
        pattern=IdRegexPattern,
        regex=IdRegexPattern,
    ),
]
ReappraisalServiceAdvanceIDField = Field(
    default_factory=lambda: str(uuid.uuid4()),
    sa_column=Column("rsa_id", String(36), primary_key=True),
    title="Reappraisal Service Advance ID",
    description="Unique identifier for the reappraisal service advance, formatted as a UUID.",
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
ReappraisalServiceAdvanceTransactionEpochField = Field(
    sa_column=Column(
        "rsa_transaction_epoch",
        Integer,
    ),
    title="Advance Transaction Epoch",
    description="Epoch time (Unix timestamp) for the advance transaction.",
    ge=0,
    schema_extra={"examples": [1700000000]},
)
ReappraisalServiceAdvanceCategoryField = Field(
    sa_column=Column("rsa_category", Enum(ReappraisalServiceCategoryEnum), index=True),
    title="Advance Category",
    description="Category of the reappraisal service advance.",
    schema_extra={"examples": ["FOOD"]},
)
ReappraisalServiceAdvanceAmountField = Field(
    sa_column=Column(
        "rsa_amount",
        Integer,
    ),
    title="Advance Amount",
    description="Amount of the reappraisal service advance in cents.",
    ge=0,
    schema_extra={"examples": [1000]},
)
ReappraisalServiceAdvanceDescriptionField = Field(
    sa_column=Column(
        "rsa_description",
        String(255),
    ),
    title="Advance Description",
    description="Description of the reappraisal service advance.",
    schema_extra={
        "examples": ["Advance for travel expenses"],
        "pattern": DescriptionRegexPattern,
    },
)
ReappraisalServiceAdvanceSettlementStatusField = Field(
    sa_column=Column("rsa_settlement_status", Enum(SettlementStatusEnum), index=True),
    title="Reappraisal Service Advance Settlement Status",
    description="Status of the Advance statement.",
    schema_extra={"examples": ["UNSETTLED"]},
)

ServiceRelationship = Relationship(
    back_populates="advances", sa_relationship_kwargs={"lazy": "selectin"}
)


class ReappraisalServiceAdvanceTable(BaseTable, table=True):
    __tablename__ = "reappraisal_service_advance"

    rs_advance_id: str = ReappraisalServiceAdvanceIDField
    reappraisal_service_id: str = ReappraisalServiceIDField
    rs_advance_transaction_epoch: int = ReappraisalServiceAdvanceTransactionEpochField  
    rs_advance_amount: int = ReappraisalServiceAdvanceAmountField
    rs_advance_description: str = ReappraisalServiceAdvanceDescriptionField
    service: "ReappraisalServiceTable" = ServiceRelationship
   
