import os
from google_auth import gmail_service
from googleapiclient.errors import HttpError

TOPICNAME = os.getenv('TOPICNAME')

def watch_gmail():
    request = {
        "labelIds": ["INBOX"],
        "topicName": TOPICNAME
    }
    try:
        watch = gmail_service.users().watch(userId='me', body=request).execute()
        print(watch)
    except HttpError as error:
        print(f"An error occurred: {error}")
        print("Detailed error response:", error.resp)
        print("Error content:", error.content.decode('utf-8'))

