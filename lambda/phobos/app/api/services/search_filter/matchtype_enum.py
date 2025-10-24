from enum import StrEnum


class MatchTypeEnum(StrEnum):
    EXACT = "EXACT"
    PARTIAL = "PARTIAL"
    EPOCH_RANGE = "EPOCH_RANGE"
    FILE_PATH_STATUS = "FILE_PATH_STATUS"
    EMPTY = "EMPTY"
    NOT_EMPTY = "NOT EMPTY"
