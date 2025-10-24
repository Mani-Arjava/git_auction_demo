from typing import Optional
from app.api.model.appraiser.appraiser_table import (
    AppraiserAddressField,
    AppraiserBankNameField,
    AppraiserBranchNameField,
    AppraiserFullNameField,
    AppraiserTable,
    AppraiserIdPath,
    AppraiserAccountIFSCCodeField,
    AppraiserAccountNumberField,
    AppraiserEmailField,
    AppraiserPanField,
    AppraiserPhoneField,
    make_optional,
)
from sqlmodel import SQLModel, Field


class AppraiserCreateRequest(SQLModel):
    appraiser_full_name: str = AppraiserFullNameField
    appraiser_email: str = AppraiserEmailField
    appraiser_phone: str = AppraiserPhoneField
    appraiser_pan: str = AppraiserPanField
    appraiser_address: str = AppraiserAddressField
    appraiser_account_number: str = AppraiserAccountNumberField
    appraiser_account_ifsc_code: str = AppraiserAccountIFSCCodeField
    appraiser_bank_name: str = AppraiserBankNameField
    appraiser_branch_name: str = AppraiserBranchNameField


class AppraiserCreateResponse(SQLModel):
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
            appraiser_branch_name=appraiser_record.appraiser_branch_name
        )


class AppraiserPatchRequest(SQLModel, extra='forbid'):
    """Appraiser partial update request - excludes name and PAN for security"""
    appraiser_email: str = AppraiserEmailField
    appraiser_phone: str = AppraiserPhoneField
    appraiser_address: str = AppraiserAddressField
    appraiser_account_number:str = AppraiserAccountNumberField
    appraiser_account_ifsc_code: str = AppraiserAccountIFSCCodeField
    appraiser_bank_name: str = AppraiserBankNameField
    appraiser_branch_name: str = AppraiserBranchNameField
    

class AppraiserUpdateResponse(SQLModel):
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
            appraiser_branch_name=appraiser_record.appraiser_branch_name
        )


class PANResponse(SQLModel):
    appraiser_id: str  # Formatted as "APR-0001"
    appraiser_pan: str = AppraiserPanField

    @classmethod
    def from_db_record(cls, appraiser_record):
        """Convert AppraiserTable record to formatted response"""
        return cls(
            appraiser_id=f"APR-{appraiser_record.appraiser_id:04d}",
            appraiser_pan=appraiser_record.appraiser_pan
        )


class BankAccountResponse(SQLModel):
    appraiser_id: str  # Formatted as "APR-0001"
    appraiser_account_number: str = AppraiserAccountNumberField

    @classmethod
    def from_db_record(cls, appraiser_record):
        """Convert AppraiserTable record to formatted response"""
        return cls(
            appraiser_id=f"APR-{appraiser_record.appraiser_id:04d}",
            appraiser_account_number=appraiser_record.appraiser_account_number
        )
