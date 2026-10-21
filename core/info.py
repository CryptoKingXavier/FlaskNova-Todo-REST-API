"""
FlaskNova Todo REST API — Extension Capability Test
==================================================

Purpose
-------
A small, documented JSON-only REST API for evaluating FlaskNova's developer
experience: typed routes, Pydantic request validation, response serialization,
HTTP status codes, OpenAPI generation, and CRUD routing.

This is an experimental development example, not a production deployment.

Features
--------
* Create, list, retrieve, update, and delete Todo resources.
* Validate incoming JSON payloads with Pydantic.
* Use typed path parameters and explicit REST-style HTTP status codes.
* Return JSON data only; this script does not render HTML templates.
* Keep the example self-contained by using in-memory storage.
* Include practical docstrings, comments, and type hints throughout.

Important limitations
---------------------
* Data is stored in memory and is lost when the process stops or restarts.
* This example is intended for local development and extension testing.
* Do not expose the development server publicly or use it as-is in production.
* FlaskNova's API may vary by release. If an import or decorator signature
  differs in the installed version, compare it with that version's documentation.

Installation
------------
  python -m venv .venv

Activate the virtual environment, then install dependencies:

  # Windows PowerShell
  .\\.venv\\Scripts\\Activate.ps1
  python -m pip install --upgrade pip
  python -m pip install flask-nova pydantic

  # Linux / macOS / Kali WSL
  source .venv/bin/activate
  python -m pip install --upgrade pip
  python -m pip install flask-nova pydantic

Run
---
  python app.py

The default development server listens at http://127.0.0.1:5000.
Check /docs and /redoc for generated documentation, if enabled by FlaskNova.

Example requests
----------------
List tasks:
  curl http://127.0.0.1:5000/api/v1/todos

Create a task:
  curl -X POST http://127.0.0.1:5000/api/v1/todos \\
    -H "Content-Type: application/json" \\
    -d '{"title":"Test FlaskNova","description":"Exercise request validation"}'

Retrieve task 1:
  curl http://127.0.0.1:5000/api/v1/todos/1

Mark task 1 as completed:
  curl -X PATCH http://127.0.0.1:5000/api/v1/todos/1 \\
    -H "Content-Type: application/json" \\
    -d '{"completed":true}'

Delete task 1:
  curl -X DELETE http://127.0.0.1:5000/api/v1/todos/1

Design notes
------------
* The API is versioned under /api/v1 to make future changes easier to manage.
* POST returns 201 Created; successful reads and updates return 200 OK.
* DELETE returns 204 No Content and therefore intentionally has no JSON body.
* PATCH changes only the supplied fields; omitted fields remain unchanged.
* Unknown IDs return a consistent JSON 404 response.
* The API intentionally avoids Flask render_template(), templates, and HTML views.

Author: CryptoKingXavier - FlaskNova capability-test example
License: MIT-style example code; adapt as needed.
"""
