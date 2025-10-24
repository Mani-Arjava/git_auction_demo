from typing import Annotated, List, Any, Optional, Tuple, Union
from pydantic import BaseModel
from app.api.services.search_filter.matchtype_enum import MatchTypeEnum
from fastapi import Query, Depends


class BaseQueryParams(BaseModel):
    search_values: List[Union[str, List[str], List[int], int, None]]

    fields: List[
        Union[
            str,
            Tuple[str, MatchTypeEnum],  # ("field", EXACT)
            Tuple[Tuple[str, str], MatchTypeEnum],  # (("field1", "field2"), RANGE)
            None,
        ]
    ]

    page: Optional[int] = None
    size: Optional[int] = None
