from typing import Optional
from app.api.model.reappraisal_service.reappraisal_service_table import (
    ReappraisalServiceTable,
)
from app.api.model.reimbursement.reimbursement_table import (
    ReappraisalServiceReimbursementIDField,
    ReappraisalReimbursementCategoryField,
    ReappraisalServiceReimbursementAmountField,
    ReappraisalServiceReimbursementSettlementStatusField,
    ReappraisalServiceReimbursementTransactionEpochField,
    ReappraisalServiceReimbursmentDetailsField,
    ReappraisalServiceReimbursementFilePathField,
    ReappraisalServiceIDField,
)
from sqlmodel import SQLModel
from typing import List, Optional


class ReappraisalServiceReimbursementGetResponse(SQLModel):

    rs_reimbursement_id: str = ReappraisalServiceReimbursementIDField
    rs_reappraisal_service_id: str = ReappraisalServiceIDField
    rs_reimbursement_transaction_epoch: int = (
        ReappraisalServiceReimbursementTransactionEpochField
    )
    rs_reimbursement_category: str = ReappraisalReimbursementCategoryField
    rs_reimbursement_details: str = ReappraisalServiceReimbursmentDetailsField
    rs_reimbursement_amount: int = ReappraisalServiceReimbursementAmountField
    rs_reimbursement_file_path: Optional[str] = (
        ReappraisalServiceReimbursementFilePathField
    )
   
    service: ReappraisalServiceTable | None = None
   