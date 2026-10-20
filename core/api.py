# Importing project configuration files
from . import *
from .models import *
from .memory import *
from .config import Config

# Importing private project configuration
from .memory import _todos, _next_id, _store_lock

# Standard-library imports provide typing annotations.
from typing import Any

# FlaskNova supplies the Flask-compatible application and API documentation features.
from flask_nova import FlaskNova, HTTPException, status


# Create the FlaskNova application. FlaskNova documents Flask-compatible routing.
app = FlaskNova(__name__)
app.config.from_object(Config)


# ---------------------------------------------------------------------------
# API endpoints
# ---------------------------------------------------------------------------

@app.get(f"{API_PREFIX}/health", response_model=HealthResponse)
def health_check() -> tuple[HealthResponse, int]:
    """Check API availability.

    This endpoint is useful for a quick smoke test and for local development
    health checks. It does not perform a database or dependency check.
    """
    # Return JSON-compatible data and an explicit 200 status.
    return HealthResponse(
        status="ok",
        service=API_TITLE,
        version=API_VERSION,
    ), status.OK


@app.get(f"{API_PREFIX}/todos", response_model=TodoListResponse)
def list_todos() -> tuple[TodoListResponse, int]:
    """List every Todo item, ordered by ascending ID.

    Returns an empty list when no tasks have been created.
    """
    # Copy the stored items while holding the lock to avoid concurrent mutation.
    with _store_lock:
        items = [
            TodoResponse(**serialize_todo(_todos[todo_id]))
            for todo_id in sorted(_todos)
        ]

    # The envelope includes a count, which clients can use without recounting.
    return TodoListResponse(
        items=items,
        count=len(items),
    ), status.OK


@app.post(
    f"{API_PREFIX}/todos",
    response_model=TodoResponse,
    summary="Create a Todo",
    description="Create a task from a validated JSON request body.",
)
def create_todo(data: TodoCreate) -> tuple[TodoResponse, int]:
    """Create a Todo item.

    FlaskNova is expected to validate the incoming JSON against TodoCreate
    before calling this function. Confirm the exact behaviour against the
    version installed in the test environment.
    """
    # Generate timestamps once so created_at and updated_at initially match.
    timestamp = utc_now()

    # Build a new record from validated data; never trust arbitrary raw input.
    with _store_lock:
        todo_id = next(_next_id)
        todo = {
            "id": todo_id,
            "title": data.title.strip(),
            "description": data.description.strip(),
            "completed": bool(),
            "created_at": timestamp,
            "updated_at": timestamp,
        }

        # Persist the record in the in-memory repository.
        _todos[todo_id] = todo

        # Copy the record before returning it from the route.
        result = serialize_todo(todo)

    # 201 Created is the standard response for a successfully created resource.
    return TodoResponse(**result), status.CREATED


@app.get(f"{API_PREFIX}/todos/<int:todo_id>", response_model=TodoResponse)
def get_todo(todo_id: int) -> tuple[TodoResponse, int]:
    """Retrieve one Todo item by its integer ID."""
    # The typed URL converter rejects non-integer path segments at routing time.
    todo = find_todo_or_404(todo_id)

    # Return the resource with a standard successful-read status.
    return TodoResponse(**todo), status.OK


@app.patch(f"{API_PREFIX}/todos/<int:todo_id>", response_model=TodoResponse)
def update_todo(
    todo_id: int,
    data: TodoUpdate,
) -> tuple[TodoResponse, int]:
    """Update only the fields supplied in the request body.

    An empty JSON object is rejected because it would not change the resource.
    Explicit null values are also rejected for fields that must remain non-null.
    """
    # exclude_unset=True distinguishes omitted fields from fields explicitly sent.
    changes = data.model_dump(exclude_unset=True)

    # Reject a no-op update rather than pretending a change occurred.
    if not changes:
        raise HTTPException(
            status_code=status.BAD_REQUEST,
            detail="Provide at least one field to update.",
            title="Empty Update",
        )

    # Prevent nullable annotations used for partial updates from erasing fields.
    for field_name, value in changes.items():
        if value is None:
            raise HTTPException(
                status_code=status.BAD_REQUEST,
                detail=f"Field '{field_name}' cannot be null.",
                title="Invalid Update",
            )

    # Apply the changes atomically within this process.
    with _store_lock:
        current = _todos.get(todo_id)

        # Raise 404 if the target does not exist.
        if current is None:
            raise HTTPException(
                status_code=status.NOT_FOUND,
                detail=f"Todo with id {todo_id} was not found.",
                title="Todo Not Found",
            )

        # Strip surrounding whitespace from replacement titles.
        for (key, value) in changes.items():
            changes[key] = value.strip()

        # Apply validated fields to the stored record.
        current.update(changes)

        # Refresh the update timestamp after a successful mutation.
        current["updated_at"] = utc_now()

        # Return a copy so external code cannot mutate the stored record.
        result = serialize_todo(current)

    # PATCH succeeded; return the updated representation.
    return TodoResponse(**result), status.OK


@app.delete(f"{API_PREFIX}/todos/<int:todo_id>")
def delete_todo(todo_id: int):
    """Delete one Todo item.

    A successful DELETE returns HTTP 204 No Content and an empty body.
    """
    # Remove the record while holding the lock.
    with _store_lock:
        if todo_id not in _todos:
            # Missing resources consistently produce a 404 response.
            raise HTTPException(
                status_code=status.NOT_FOUND,
                detail=f"Todo with id {todo_id} was not found.",
                title="Todo Not Found",
            )

        # Delete the task from the in-memory repository.
        del _todos[todo_id]

    # HTTP 204 must not include a response body.
    return "", status.NO_CONTENT
