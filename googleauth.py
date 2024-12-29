from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

def authenticate():
    flow = InstalledAppFlow.from_client_secrets_file(
        'client_secrets.json',
        scopes=['https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile', 'openid'],)

    flow.run_local_server(port=9000, authorization_prompt_message='')
    creds = flow.credentials

    service = build('oauth2', 'v2', credentials=creds)
    info = service.userinfo().get().execute()

    return (info['id'], info['email'])
