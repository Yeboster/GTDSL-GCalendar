import os.path
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate(pickle_path: str = None, credentials_path: str = None):
    """Authenticate to Google Calndar.
        The method serialize the credntials to pickle_path @default token.pickle.
        @return the api Google Calendar object."""
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if pickle_path is None:
        pickle_path = 'token.pickle'
    if credentials_path is None:
        credentials_path = 'credentials.json'

    if os.path.exists(pickle_path):
        with open(pickle_path, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        # Cannot use same path because secrets are read-only
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)
