import os
from pathlib import Path
from google.oauth2 import service_account
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Project root directory
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# Google Cloud settings
PROJECT_ID = os.getenv("PROJECT_ID", "trim-mix-444914-m2")
LOCATION = os.getenv("LOCATION", "northamerica-northeast2")
STAGING_BUCKET = os.getenv("STAGING_BUCKET", "gs://vertex-ai-testing-bucket")

# Path to service account key
KEY_FILE_PATH = os.path.join(ROOT_DIR, "credentials", "trim-mix-444914-m2-777e33acbe7c.json")

# Load and configure credentials
credentials = service_account.Credentials.from_service_account_file(
    KEY_FILE_PATH,
    scopes=['https://www.googleapis.com/auth/cloud-platform']
)

# Set application default credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = KEY_FILE_PATH 