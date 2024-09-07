import os
from google.oauth2 import service_account
from googleapiclient.discovery import build


SERVICE_ACCOUNT_FILE =  os.getenv('SERVICE_ACCOUNT_FILE')

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/drive",
]

SUBJECT = os.getenv('SUBJECT')

def authenticate_apis():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES, subject=SUBJECT)
    drive_service = build("drive", "v3", credentials=creds)
    gmail_service = build("gmail", "v1", credentials=creds)

    return drive_service, gmail_service


drive_service, gmail_service = authenticate_apis()
