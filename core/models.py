# Standard-library imports provide timestamps, IDs, and typing annotations.
from typing import Literal
from datetime import datetime

# Pydantic validates request data and documents the data models.
from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------------------
# Pydantic request and response models
# ---------------------------------------------------------------------------

class TodoCreate(BaseModel):
    """Validate the JSON body required to create a Todo item."""

    # Reject unexpected keys so client mistakes are visible during testing.
    model_config = ConfigDict(extra="forbid")

    # A title is mandatory and must contain between 1 and 120 characters.
    title: str = Field(min_length=1, max_length=120, description="Short task title")

    # Description is optional; an empty description is allowed.
    description: str = Field(
        default="",
        max_length=2000,
        description="Optional details about the task",
    )


class TodoUpdate(BaseModel):
    """Validate a partial Todo update submitted through PATCH."""

    # Reject misspelled or unsupported fields rather than silently ignoring them.
    model_config = ConfigDict(extra="forbid")

    # Every field is optional because PATCH modifies only provided fields.
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=120,
        description="Replacement title",
    )
    description: str | None = Field(
        default=None,
        max_length=2000,
        description="Replacement description",
    )
    completed: bool | None = Field(
        default=None,
        description="Whether the task is completed",
    )


class TodoResponse(BaseModel):
    """Describe the public JSON representation of a Todo item."""

    # Declare the exact fields exposed by the API response.
    id: int = Field(description="Unique task identifier")
    title: str = Field(description="Short task title")
    description: str = Field(description="Task details")
    completed: bool = Field(description="Completion state")
    created_at: datetime = Field(description="Creation timestamp in UTC")
    updated_at: datetime = Field(description="Last update timestamp in UTC")


class TodoListResponse(BaseModel):
    """Describe the JSON envelope returned when listing tasks."""

    # Return tasks alongside a count to make client-side handling convenient.
    items: list[TodoResponse]
    count: int


class HealthResponse(BaseModel):
    """Describe the simple health-check response."""

    status: Literal["ok"]
    service: str
    version: str
