from typing import Any, Dict, List, Optional
from app.api.model.reappraisal_service.reappraisal_service_table import (
    ReappraisalServiceBankIdField,
    ReappraisalServiceDescriptionsField,
    ReappraisalServiceChargeField,
    ReappraisalServiceEndEpochField,
    ReappraisalServiceBranchIdField,
    ReappraisalServicePacketCountField,
    ReappraisalServiceStatusField,
    ReappraisalServiceCompletionFilePathField,
    ReappraisalServiceAppraiserIDField,
    ReappraisalServiceIDField,
    ReappraisalServiceStartEpochField,
)
from sqlmodel import SQLModel
from app.api.model.appraiser.appraiser_table import AppraiserTable
from app.api.model.advance.advance_table import (
    ReappraisalServiceAdvanceTable,
)
from app.api.model.reimbursement.reimbursement_table import (
    ReappraisalServiceReimbursementTable,
)
from app.api.model.bank.bank_table import BankTable
from app.api.model.branch.branch_table import BranchTable



class ReappraisalServiceGetResponse(SQLModel):
    reappraisal_service_id: str = ReappraisalServiceIDField
    appraiser_name: str
    bank_name: str
    branch_name: str
    start_epoch: int = ReappraisalServiceStartEpochField
    end_epoch: int = ReappraisalServiceEndEpochField
    no_of_packets: int
    status: str = ReappraisalServiceStatusField
    total_amount: int
    appraiser: AppraiserTable | None = None
    bank:BankTable | None = None
    branch:BranchTable | None = None


class ReappraisalServiceAPIResponse(SQLModel):
    reappraisal_service_id: str = ReappraisalServiceIDField
    rs_appraiser_id: str = ReappraisalServiceAppraiserIDField
    rs_branch_id: str = ReappraisalServiceBranchIdField
    rs_start_epoch: int = ReappraisalServiceStartEpochField
    rs_end_epoch: int = ReappraisalServiceEndEpochField
    rs_packet_count: int = ReappraisalServicePacketCountField
    rs_charge: int = ReappraisalServiceChargeField
    rs_status: str = ReappraisalServiceStatusField
    rs_completion_file_path: Optional[str] = ReappraisalServiceCompletionFilePathField
   


class ReappraisalServiceGetByIdResponse(SQLModel):
    reappraisal_service_id: str = ReappraisalServiceIDField
    rs_appraiser_id: str = ReappraisalServiceAppraiserIDField
    rs_bank_id:str = ReappraisalServiceBankIdField
    rs_branch_id: str = ReappraisalServiceBranchIdField
    rs_start_epoch: int = ReappraisalServiceStartEpochField
    rs_end_epoch: int = ReappraisalServiceEndEpochField
    rs_packet_count: int = ReappraisalServicePacketCountField
    rs_charge: int = ReappraisalServiceChargeField
    rs_status: str = ReappraisalServiceStatusField
    rs_completion_file_path: Optional[str] = ReappraisalServiceCompletionFilePathField
    rs_description :str = ReappraisalServiceDescriptionsField
    reimbursement_amount: Optional[int] = 0
    advance_amount: Optional[int] = 0
    total_amount: Optional[int] = 0
    appraiser_name: str
    bank_name: str
    bank_code: str
    branch_name: str
    branch_sol_id: str
    no_of_days: int
    created_at_epoch: str
    updated_at_epoch: str
    appraiser: AppraiserTable | None = None
    reimbursements: List["ReappraisalServiceReimbursementTable"] = []
    advances: List["ReappraisalServiceAdvanceTable"] = []
  