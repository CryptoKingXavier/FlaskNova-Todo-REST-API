# Standard-library imports provide timestamps, IDs, typing, and in-memory storage.
from datetime import datetime, timezone
from itertools import count
from threading import Lock
from typing import Any

# FlaskNova supplies the Flask-compatible application features.
from flask_nova import HTTPException, status

# ---------------------------------------------------------------------------
# In-memory repository
# ---------------------------------------------------------------------------

# This dictionary acts as a tiny repository for the experiment.
# Replace it with a database-backed repository for persistence.
_todos: dict[int, dict[str, Any]] = {}

# count() generates monotonically increasing IDs beginning at 1.
_next_id = count(1)

# A lock prevents concurrent requests from modifying this in-memory store at
# the same time. This is a small safeguard for the demonstration, not a substitute
# for database transactions or distributed concurrency control.
_store_lock = Lock()


def utc_now() -> datetime:
  """Return the current timezone-aware UTC timestamp."""
  return datetime.now(timezone.utc)


def serialize_todo(todo: dict[str, Any]) -> dict[str, Any]:
  """Return a shallow copy so callers cannot mutate stored records directly."""
  return dict(todo)


def find_todo_or_404(todo_id: int) -> dict[str, Any]:
  """Retrieve a task or raise an HTTP 404 error if the ID does not exist."""
  # The lock protects the dictionary lookup against concurrent mutations.
  with _store_lock:
    todo = _todos.get(todo_id)

    # Raise FlaskNova's documented HTTP exception for a missing resource.
    if todo is None:
      raise HTTPException(
        status_code=status.NOT_FOUND,
        detail=f"Todo with id {todo_id} was not found.",
        title="Todo Not Found",
      )

    # Return a copy to keep stored state isolated from route-level changes.
    return serialize_todo(todo)
