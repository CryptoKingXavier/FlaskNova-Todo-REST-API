# Importing required libraries for session encryption.
from secrets import token_hex


class Config:
    """Implementing FlaskNova default server configuration settings."""
    SECRET_KEY = token_hex(16)
