from typing import Optional
from app.api.model.reappraisal_service.reappraisal_service_table import (
    ReappraisalServiceBankIdField,
    ReappraisalServiceBranchIdField,
    ReappraisalServiceChargeField,
    ReappraisalServiceDescriptionsField,
    ReappraisalServiceEndEpochField,
    ReappraisalServicePacketCountField,
    ReappraisalServiceStatusField,
    ReappraisalServiceCompletionFilePathField,
    ReappraisalServiceAppraiserIDField,
    ReappraisalServiceIDField,
    ReappraisalServiceStartEpochField,
)
from sqlmodel import SQLModel


class ReappraisalServiceCreateRequest(SQLModel):

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



class ReappraisalFileUpdate(SQLModel):
    rs_completion_file_path: Optional[str] = ReappraisalServiceCompletionFilePathField


class ReappraisalServiceCreateResponse(SQLModel):
    reappraisal_service_id: str = ReappraisalServiceIDField
    rs_appraiser_id: str = ReappraisalServiceAppraiserIDField
    rs_branch_id: str = ReappraisalServiceBranchIdField
    rs_start_epoch: int = ReappraisalServiceStartEpochField
    rs_end_epoch: int = ReappraisalServiceEndEpochField
    rs_packet_count: int = ReappraisalServicePacketCountField
    rs_charge: int = ReappraisalServiceChargeField
    rs_status: str = ReappraisalServiceStatusField
    rs_completion_file_path: Optional[str] = ReappraisalServiceCompletionFilePathField
    rs_description :str = ReappraisalServiceDescriptionsField


class ReappraisalServiceQueueRequest(SQLModel):
    reappraisal_service_id: str = ReappraisalServiceIDField
    rs_status: str = ReappraisalServiceStatusField


class ReappraisalServiceUpdateRequest(SQLModel):
    reappraisal_service_id: str = ReappraisalServiceIDField
    rs_appraiser_id: str = ReappraisalServiceAppraiserIDField
    rs_bank_id:str = ReappraisalServiceBankIdField
    rs_branch_id: str = ReappraisalServiceBranchIdField
    rs_start_epoch: int = ReappraisalServiceStartEpochField
    rs_end_epoch: int = ReappraisalServiceEndEpochField
    rs_packet_count: int = ReappraisalServicePacketCountField
    rs_charge: int = ReappraisalServiceChargeField
    rs_description :str = ReappraisalServiceDescriptionsField

    