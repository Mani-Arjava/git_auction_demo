from datetime import datetime
from typing import Optional
from sqlalchemy import String
from sqlmodel import Column, Field, Integer, SQLModel


CreatedAtField = Field(
    default_factory=lambda: int(datetime.now().timestamp()),
    title="Created Epoch Value",
    description="Epoch of the created time",
    schema_extra={
        "examples": [1741019909],
    },
)

UpdatedAtField = Field(
    default_factory=lambda: int(datetime.now().timestamp()),
    title="Updated Epoch Value",
    description="Epoch of the updated time",
    schema_extra={
        "examples": [1741019909],
    },
)

DeletedAtField = Field(
    default=-1,
    title="Deleted Epoch Value",
    description="Epoch of the deleted time",
    schema_extra={
        "examples": [1741019909],
    },
)


class BaseTable(SQLModel):
    __abstract__ = True
    created_at_epoch: Optional[int] = CreatedAtField
    updated_at_epoch: Optional[int] = UpdatedAtField
    deleted_at_epoch: Optional[int] = DeletedAtField
