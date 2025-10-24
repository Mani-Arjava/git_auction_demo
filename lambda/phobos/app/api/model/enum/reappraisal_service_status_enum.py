from enum import StrEnum


class ReappraisalServiceStatusEnum(StrEnum):

    ACTIVE = "ACTIVE"
    READY_FOR_PAYMENT = "READY_FOR_PAYMENT"
    CARRY_FORWARDED = "CARRY_FORWARDED"
    SETTLED = "SETTLED"
    WRITTEN_OFF = "WRITTEN_OFF"

class EligibleServiceStatusEnum(StrEnum):

    QUEUED = "QUEUED"


class FilePendingStatusEnum(StrEnum):
    PENDING = "PENDING"
    RECEVIED = "RECEVIED"
    NOT_APPLICABLE = "NOT_APPLICABLE"
