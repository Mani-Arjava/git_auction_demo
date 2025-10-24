from enum import StrEnum


class SettlementStatusEnum(StrEnum):

    UNSETTLED = "UNSETTLED"
    CARRY_FORWARD = "CARRY_FORWARD"
    SETTLED = "SETTLED"
    WRITTEN_OFF = "WRITTEN_OFF"


class UpdatedSettlementStatusEnum(StrEnum):
    SETTLED = "SETTLED"
    WRITTEN_OFF = "WRITTEN_OFF"
