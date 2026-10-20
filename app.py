from core.api import app
from os import name, system


# ---------------------------------------------------------------------------
# Local development entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Configure FlaskNova's generated API documentation before starting the app.
    # The docs UI is intended for local testing; disable or protect it in production.
    # app.setup_swagger()

    # Clearing the terminal screen
    system("cls" if name == "nt" else "clear")

    # Bind only to loopback by default to avoid exposing the development server.
    # Debug mode is disabled because debug consoles can expose sensitive internals.
    app.run(host="127.0.0.1", port=5000, debug=True)
