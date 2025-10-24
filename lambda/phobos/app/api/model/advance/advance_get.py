from app.api.model.reappraisal_service.reappraisal_service_table import (
    ReappraisalServiceTable,
)
from app.api.model.advance.advance_table import (
    ReappraisalServiceIDField,
    ReappraisalServiceAdvanceAmountField,
    ReappraisalServiceAdvanceCategoryField,
    ReappraisalServiceAdvanceDescriptionField,
    ReappraisalServiceAdvanceIDField,
    ReappraisalServiceAdvanceSettlementStatusField,
    ReappraisalServiceAdvanceTransactionEpochField,
)
from typing import List
from sqlmodel import SQLModel


class ReappraisalServiceAdvanceGetResponse(SQLModel):
    rs_advance_id: str = ReappraisalServiceAdvanceIDField
    reappraisal_service_id: str = ReappraisalServiceIDField
    rs_advance_transaction_epoch: int = ReappraisalServiceAdvanceTransactionEpochField
    rs_advance_amount: int = ReappraisalServiceAdvanceAmountField
    rs_advance_description: str = ReappraisalServiceAdvanceDescriptionField
    service: ReappraisalServiceTable | None = None
    
