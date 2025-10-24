from typing import List
from pydantic import computed_field
from app.api.model.appraiser.appraiser_table import (
    AppraiserAccountIFSCCodeField,
    AppraiserAccountNumberField,
    AppraiserAddressField,
    AppraiserBankNameField,
    AppraiserBranchNameField,
    AppraiserEmailField,
    AppraiserFullNameField,
    AppraiserPanField,
    AppraiserPhoneField,
)
from sqlmodel import SQLModel

from app.api.model.reappraisal_service.reappraisal_service_table import (
    ReappraisalServiceTable,
)

class AppraiserGetResponse(SQLModel):
    appraiser_id: str  # Formatted as "APR-0001"
    appraiser_full_name: str = AppraiserFullNameField
    appraiser_email: str = AppraiserEmailField
    appraiser_phone: str = AppraiserPhoneField
    appraiser_pan: str = AppraiserPanField
    appraiser_address: str = AppraiserAddressField
    appraiser_account_number: str = AppraiserAccountNumberField
    appraiser_account_ifsc_code: str = AppraiserAccountIFSCCodeField
    appraiser_bank_name: str = AppraiserBankNameField
    appraiser_branch_name: str = AppraiserBranchNameField
    active_services_count: int = 0

    services: List["ReappraisalServiceTable"] = []
    # payouts: List["PayoutStatementTable"] = []

  

    @classmethod
    def from_db_record(cls, appraiser_record):
        """Convert AppraiserTable record to formatted response"""
        return cls(
            appraiser_id=f"APR-{appraiser_record.appraiser_id:04d}",
            appraiser_full_name=appraiser_record.appraiser_full_name,
            appraiser_email=appraiser_record.appraiser_email,
            appraiser_phone=appraiser_record.appraiser_phone,
            appraiser_pan=appraiser_record.appraiser_pan,
            appraiser_address=appraiser_record.appraiser_address,
            appraiser_account_number=appraiser_record.appraiser_account_number,
            appraiser_account_ifsc_code=appraiser_record.appraiser_account_ifsc_code,
            appraiser_bank_name=appraiser_record.appraiser_bank_name,
            appraiser_branch_name=appraiser_record.appraiser_branch_name,
            services=[]
        )


class AadhaarResponse(SQLModel):
    appraiser_id: str
    appraiser_aadhaar: str


class PANResponse(SQLModel):
    appraiser_id: str
    appraiser_pan: str


class BankAccountResponse(SQLModel):
    appraiser_id: str
    appraiser_account_number: str
