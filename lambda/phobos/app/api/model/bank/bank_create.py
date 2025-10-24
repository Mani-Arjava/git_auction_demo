from ...model.bank.bank_table import (
    BankIdPath, BankIDField, BankNameField, BankCodeField,
    BankHeadOfficeAddressField, BankContactEmailField, BankContactNumberField
)
from sqlmodel import SQLModel


class BankCreateRequest(SQLModel):
    bank_name: str = BankNameField
    bank_code: str = BankCodeField
    bank_head_office_address: str = BankHeadOfficeAddressField
    bank_contact_email: str = BankContactEmailField
    bank_contact_number: str = BankContactNumberField


class BankCreateResponse(SQLModel):
    bank_id: str  # Formatted as "BNK-0001"
    bank_name: str
    bank_code: str
    bank_head_office_address: str
    bank_contact_email: str
    bank_contact_number: str

    @classmethod
    def from_db_record(cls, bank_record):
        """Convert BankTable record to formatted response"""
        return cls(
            bank_id=f"BNK-{bank_record.bank_id:04d}",
            bank_name=bank_record.bank_name,
            bank_code=bank_record.bank_code,
            bank_head_office_address=bank_record.bank_head_office_address,
            bank_contact_email=bank_record.bank_contact_email,
            bank_contact_number=bank_record.bank_contact_number
        )
