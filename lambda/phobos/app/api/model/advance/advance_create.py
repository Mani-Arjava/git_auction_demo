from app.api.model.advance.advance_table import (
    ReappraisalServiceIDField,
    ReappraisalServiceAdvanceAmountField,
    ReappraisalServiceAdvanceCategoryField,
    ReappraisalServiceAdvanceDescriptionField,
    ReappraisalServiceAdvanceIDField,
    ReappraisalServiceAdvanceSettlementStatusField,
    ReappraisalServiceAdvanceTransactionEpochField,
)
from sqlmodel import SQLModel


class ReappraisalServiceAdvanceCreateRequest(SQLModel):
    reappraisal_service_id: str = ReappraisalServiceIDField
    rs_advance_transaction_epoch: int = ReappraisalServiceAdvanceTransactionEpochField
    rs_advance_amount: int = ReappraisalServiceAdvanceAmountField
    rs_advance_description: str = ReappraisalServiceAdvanceDescriptionField
   


class ReappraisalServiceAdvanceCreateResponse(SQLModel):
    rs_advance_id: str = ReappraisalServiceAdvanceIDField
    reappraisal_service_id: str = ReappraisalServiceIDField
    rs_advance_transaction_epoch: int = ReappraisalServiceAdvanceTransactionEpochField
    rs_advance_amount: int = ReappraisalServiceAdvanceAmountField
    rs_advance_description: str = ReappraisalServiceAdvanceDescriptionField
   
