from os import name, system

from core.api import app

# ---------------------------------------------------------------------------
# Local development entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
  # Configure FlaskNova's generated API documentation before starting the app.
  # The docs UI is intended for local testing; disable or protect it in production.

  # Clearing the terminal screen
  system("cls" if name == "nt" else "clear")

  # Bind only to loopback by default to avoid exposing the development server.
  # Debug mode is disabled because debug consoles can expose sensitive internals.
  app.run(
    host="127.0.0.1",
    port=5000,
    debug=True,
    load_dotenv=True,
    use_reloader=True,
    use_debugger=True,
    use_evalex=True,
    # ssl_context="adhoc",   # for dummy self-signed certificate
    ssl_context=("./openssl/cert.pem", "./openssl/key.pem"),   # for openssl self-signed certificate
  )
