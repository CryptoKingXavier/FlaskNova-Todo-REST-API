# FlaskNova Todo REST API — Capability Test

**TL;DR:** We'll build a fully documented, JSON-only Todo REST API using `flask-nova`, Pydantic request models, typed routes, automatic API documentation, and complete CRUD operations. The goal is to evaluate FlaskNova as a developer productivity extension, not merely build another Todo app.

The documentation describes FlaskNova's support for typed routing, Pydantic validation, response models, OpenAPI documentation, structured HTTP errors, and Flask ecosystem integrations. We'll exercise those capabilities in a small, testable API.

## 1. What the Test API will cover

### Todo Resource Management

Create, retrieve, list, update, and delete tasks using standard REST conventions.

### Schema Validation

Use Pydantic models to validate required fields, string lengths, and task status.

### Automatic API Documentation

Test the generated OpenAPI schema, Swagger UI, and ReDoc where supported by the installed version.

### Extension Behaviour

Exercise typed URL parameters, HTTP status codes, response serialization, error handling, and CRUD edge cases.

> **Implementation decision:** The initial version uses in-memory storage so that the experiment isolates FlaskNova's behaviour from database configuration. Tasks disappear when the process restarts. Once the extension's routing and validation behaviour has been verified, the storage layer can be replaced with Flask-SQLAlchemy and PostgreSQL.

## 2. Install and run

Clone the repository and create a virtual environment:

```bash
# Clone the repository
git clone https://github.com/CryptoKingXavier/FlaskNova-Todo-REST-API.git

# Navigate to the directory
cd FlaskNova-Todo-REST-API/

# Create a virtual environment using virtualenv
py -m venv .venv
```

Activate the virtual environment, then install the dependencies:

```bash
# Windows PowerShell
.\\.venv\\Scripts\\Activate.ps1

# Kali Linux / WSL2 / macOS
source .venv/bin/activate
```

```bash
# Update Python's Package Installer (PIP) to latest version
pip install --upgrade pip

# Iteratively install project requirements from requirements file
pip install -r requirements.txt

# Startup the development server
py app.py
```

> The API should listen at `http://127.0.0.1:5000` if startup succeeds.

## 3. Test the REST endpoints

| Method | Endpoint | Expected result |
|---|---|---|
| `GET` | `/api/health` | `200 OK` |
| `GET` | `/api/v1/todos` | `200 OK` |
| `POST` | `/api/v1/todos` | `201 Created` |
| `GET` | `/api/v1/todo/get/1` | `200 OK`, or `404` |
| `PATCH` | `/api/v1/todo/patch/1` | `200 OK`, or `404` |
| `DELETE` | `/api/v1/todo/delete/1` | `204 No Content`, or `404` |


```bash
flask routes

# Use the command above to view this table-mapping in the terminal
Endpoint           Methods  Rule
-----------------  -------  ---------------------------------
api.create_todo    POST     /api/v1/todos
api.delete_todo    DELETE   /api/v1/todo/delete/<int:todo_id>
api.get_todo       GET      /api/v1/todo/get/<int:todo_id>
api.list_todos     GET      /api/v1/todos
api.update_todo    PATCH    /api/v1/todo/patch/<int:todo_id>
docs.openapi_json  GET      /openapi.json
docs.redoc_ui      GET      /redoc
docs.scalar_ui     GET      /scalar
docs.swagger_ui    GET      /docs
health_check       GET      /health
logger             GET      /log
static             GET      /static/<path:filename>
```

### Create your first Todo

```bash
curl -X POST http://127.0.0.1:5000/api/v1/todos \\
  -H "Content-Type: application/json" \\
  -d '{"title":"Test FlaskNova","description":"Evaluate validation and routing"}'
```

### Update its completion status

```bash
curl -X PATCH http://127.0.0.1:5000/api/v1/todo/patch/1 \\
  -H "Content-Type: application/json" \\
  -d '{"completed":true}'
```

### Try invalid input

```bash
curl -X POST http://127.0.0.1:5000/api/v1/todos \\
  -H "Content-Type: application/json" \\
  -d '{"title":"","unexpected_field":true}'
```

> This last request should exercise both the title constraint and rejection of unknown fields. Verify whether FlaskNova returns the expected validation response and status code for your installed release.

## 4. Verify the documentation

Once the server is running, try:

- Swagger UI: [http://127.0.0.1:5000/docs](http://127.0.0.1:5000/docs)
- ReDoc: [http://127.0.0.1:5000/redoc](http://127.0.0.1:5000/redoc)

> These routes should be verified against the installed version.

## 5. Capability-testing checklist

**♠** means `passed`
**♣** means `failed`
**♦** means `not-checked`

- [♠] Valid JSON requests are accepted
- [♠] Missing resources return HTTP 404
- [♣] Full flask internals implementation
- [♠] Invalid Pydantic payloads are rejected
- [♠] Typed URL parameters behave as expected
- [♠] PATCH preserves fields that were not supplied
- [♠] DELETE returns an empty response with HTTP 204
- [♠] Response models serialize timestamps correctly
- [♠] CRUD endpoints return the intended HTTP status codes
- [♠] Application starts without import or decorator errors
- [♦] Swagger/OpenAPI documentation includes the routes and schemas

> **Important:** This is an `initial capability-test harness`, not a claim that every behaviour has already been verified against FlaskNova. In particular, confirm the extension's actual validation-error format and response-model behaviour by running these tests.

> My recommended next step is to add a `pytest` suite and compare FlaskNova's behaviour with ordinary Flask. That will give measurable results on validation, documentation generation, HTTP semantics, and developer ergonomics before introducing SQLAlchemy or PostgreSQL.
