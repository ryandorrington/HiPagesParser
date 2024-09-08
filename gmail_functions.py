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


def get_new_emails(history_id):
    # Fetch the history of changes since the provided historyId
    history_response = gmail_service.users().history().list(userId='me', startHistoryId=history_id).execute()

    new_emails = []

    if 'history' in history_response:
        for history_record in history_response['history']:
            if 'messagesAdded' in history_record:
                for message_added in history_record['messagesAdded']:
                    message_id = message_added['message']['id']
                    # Fetch the full message
                    message = gmail_service.users().messages().get(userId='me', id=message_id, format='full').execute()
                    new_emails.append(message)

    return new_emails