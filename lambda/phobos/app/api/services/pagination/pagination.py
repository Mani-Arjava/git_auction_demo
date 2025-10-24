from typing import Annotated, Generic, List, Optional, TypeVar
from fastapi import Query
from pydantic import BaseModel, Field
from sqlmodel import SQLModel

# Query parameters for pagination
PageQuery = Annotated[
    int,
    Query(
        ge=1,
        description="Page number to fetch (starts from 1)",
    ),
]

SizeQuery = Annotated[
    int,
    Query(
        ge=1,
        le=100,
        description="Number of records per page (max 100)",
    ),
]


class PaginationData(BaseModel):
    """Metadata about pagination."""

    total_data: int = Field(..., description="Total number of datas available")
    page: Optional[int] = Field(None, description="Current page number")
    size: Optional[int] = Field(None, description="Number of records per page")
    pages: Optional[int] = Field(None, description="Total number of pages")


T = TypeVar("T", bound=SQLModel)


class PaginationResponse(BaseModel, Generic[T]):
    items: List[T]
    pagination_data: Optional[PaginationData] = None
