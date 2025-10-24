from dataclasses import field, fields
from select import select
from sqlalchemy.orm import aliased
from typing import Any, Optional, Tuple, Type, TypeVar, Generic, Set, List
from sqlalchemy import cast, String, and_, func, or_
from sqlalchemy.orm import contains_eager
from sqlmodel import SQLModel, case
from app.api.exceptions.searchfilter_exception import (
    BadRequestException,
    ResourceNotFoundException,
    UnprocessableEntityException,
)
from app.api.services.search_filter.matchtype_enum import MatchTypeEnum
from app.api.services.search_filter.basequery import BaseQueryParams

T = TypeVar("T", bound=SQLModel)


class DAOFilterSearchParam(Generic[T]):
    def __init__(
        self,
        model_class: Type[T],
        field: str,
        match_type: str,
        value: Any,
        stmt=None,
        joined_rels: set[Type[SQLModel]] | None = None,
    ):
        self.model_class: Type[T] = model_class
        self.field: str = field
        self.match_type: str = match_type
        self.value: Any = value
        self.stmt = stmt
        self.joined_rels: set[Type[SQLModel]] = joined_rels or set()

    async def generic_filter(self) -> Tuple[Any, Any]:

        model: Type[T] = self.model_class  # base model
        rel_attr_for_eager = None  # for relationship eager loading

        column = None

        # --- Check if field is directly in the base model ---
        if hasattr(model, self.field):
            column = getattr(model, self.field)
        else:
            # --- Otherwise, check relationships dynamically ---
            for rel_name, rel in model.__mapper__.relationships.items():
                rel_model = rel.entity.class_
                if hasattr(rel_model, self.field):
                    column = getattr(rel_model, self.field)
                    rel_attr_for_eager = getattr(model, rel_name)

                    # If not already joined, add the join + eager load
                    if rel_model not in self.joined_rels:
                        self.stmt = self.stmt.join(rel_attr_for_eager)
                        self.stmt = self.stmt.options(
                            contains_eager(rel_attr_for_eager)
                        )
                        self.joined_rels.add(rel_model)
                    break

        # --- If column not found anywhere, return none ---
        if not column:
            return self.stmt, None

        condition = None
        if (
            isinstance(self.value, list)
            and self.match_type == MatchTypeEnum.EXACT.value
        ):
            condition = column.in_(self.value)
        elif isinstance(self.value, str):
            if self.match_type == MatchTypeEnum.PARTIAL.value:
                print(f"Partial match on {self.field} with value {self.value}")
                condition = column.ilike(f"%{self.value}%")
            elif self.match_type == MatchTypeEnum.EXACT.value:
                condition = column == self.value.strip()
        elif (
            isinstance(self.value, int) and self.match_type == MatchTypeEnum.EXACT.value
        ):
            condition = column == self.value

        return self.stmt, condition

    async def file_path_filter(
        model_class: Type[T], field: str, value: str = None, derive: bool = False
    ):
        """
        Returns SQLAlchemy filter or CASE expression for file path status.
        Works with any SQLModel class (generic).
        """
        column = getattr(model_class, field)

        if derive:
            # Derive dynamic label for SELECT output
            return case(
                (column.is_(None), MatchTypeEnum.EMPTY.value),
                else_=MatchTypeEnum.NOT_EMPTY.value,
            ).label(MatchTypeEnum.FILE_PATH_STATUS.name)

        if not value:
            raise BadRequestException()

        status_value = str(value).lower()
        if status_value == MatchTypeEnum.EMPTY.value.lower():
            return column.is_(None)
        elif status_value == MatchTypeEnum.NOT_EMPTY.value.lower():
            return column.is_not(None)
        else:
            raise BadRequestException()

    async def epoch_date(
        stmt,
        model_class: Type[T],
        date_value: int,
        start_field: str,
        end_field: str,
        joined_rels: set,
    ):
        if date_value is None:
            raise ResourceNotFoundException()

        # 1. Check main table columns
        if hasattr(model_class, start_field) and hasattr(model_class, end_field):
            start_col = getattr(model_class, start_field)
            end_col = getattr(model_class, end_field)
            condition = and_(start_col <= date_value, end_col >= date_value)
            return stmt, condition

        # 2. Check relationships
        for rel in model_class.__mapper__.relationships.values():
            rel_model = rel.mapper.class_
            if hasattr(rel_model, start_field) and hasattr(rel_model, end_field):
                # Avoid duplicate joins
                if rel_model not in joined_rels:
                    rel_alias = aliased(rel_model)
                    stmt = stmt.join(rel_alias, getattr(model_class, rel.key))
                    joined_rels.add(rel_model)
                else:
                    # Use existing alias or fallback to rel_model (simplification)
                    rel_alias = (
                        rel_model  # Adjust if you maintain alias references elsewhere
                    )

                start_col = getattr(rel_alias, start_field)
                end_col = getattr(rel_alias, end_field)
                condition = and_(start_col <= date_value, end_col >= date_value)
                return stmt, condition

        # Not found anywhere
        raise BadRequestException()
