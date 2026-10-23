# Importing required libraries for session encryption.
from secrets import token_hex


class Config:
  """Implementing FlaskNova default server configuration settings."""

  SECRET_KEY = token_hex(16)

  # this modifies app.logger to log colored json object
  ANSI_COLOR_JSON_LOG = True

  # Exposing the followinf application configuration switch.
  FLASKNOVA_ENABLED_DOCS = True
  FLASKNOVA_SWAGGER_ROUTE = "/docs"
  FLASKNOVA_REDOC_ROUTE = "/redoc"
  FLASKNOVA_SCALAR_ROUTE = "/scalar"
