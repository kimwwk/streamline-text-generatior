import os
from pathlib import Path
from google.oauth2 import service_account
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Project root directory
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# Google Cloud settings
PROJECT_ID = os.getenv("PROJECT_ID")
LOCATION = os.getenv("LOCATION")
STAGING_BUCKET = os.getenv("STAGING_BUCKET")
KEY_FILE_NAME = os.getenv("KEY_FILE_NAME")

# Path to service account key
KEY_FILE_PATH = os.path.join(ROOT_DIR, "credentials", KEY_FILE_NAME)

# Load and configure credentials
credentials = service_account.Credentials.from_service_account_file(
    KEY_FILE_PATH,
    scopes=['https://www.googleapis.com/auth/cloud-platform']
)

# Set application default credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = KEY_FILE_PATH 