from typing import NewType, TypeAlias
from pydantic import BaseModel, constr


NameRegexPattern = r"^[A-Z][a-z]+(?: [A-Z][a-z]+)*$"
IdRegexPattern = r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[4][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
EmailRegexPattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
PhoneNumberRegexPattern = r"^\+91[-]?[6789]\d{9}$"
AadharRegexPattern = r"^[2-9]\d{0,2}(?:\s?\d{3}){0,1}(?:\s?\d{4}){0,2}$"
PanCardRegexPattern = r"^[A-Z]{5}[0-9]{4}[A-Z]$"
AccountNumberRegexPattern = r"^\d{9,18}$"
IFSCCodeRegexPattern = r"^[A-Za-z]{4}[a-zA-Z0-9]{7}$"
FilePathRegexPattern = r"^https?:\/\/[^\s]+?\.(pdf|jpg|png)(\?.+)?$"
DescriptionRegexPattern = r"^[a-zA-Z0-9\s\-\,\.\:\;\(\)]+$"
BanknameRegexPattern = r"^[A-Za-z\s\-]{2,50}$"
BankCodeRegexPattern = r"^[A-Z0-9]{2,10}$"
AddressRegexPattern = r"^[a-zA-Z0-9\s\-\,\#\.]+$"
AppraiserIdRegexPattern = r"^apr-\d{4}$"
SolIdRegexPattern = r"^[0-9]{6}$"
PostalCodeRegexPattern = r"^[1-9][0-9]{5}$"
