# Importing project configuration libraries.
from os import getenv

from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Application configuration
# ---------------------------------------------------------------------------

# Importing environment variables.
load_dotenv()

# Keep the API prefix in one place so it is easy to change when versioning.
API_PREFIX = getenv("API_PREFIX")

# A short description is useful when inspecting the API and its generated schema.
API_TITLE = getenv("API_TITLE")
API_VERSION = getenv("API_VERSION")
