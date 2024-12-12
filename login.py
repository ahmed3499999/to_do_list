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
    f = open('creds.txt', 'a')
    f.write(info['id'])
    f.close()
    # print(info['email'])
    for k in info.keys():
        print ( k + ': ' + str(info[k]))
    return id

f = open('creds.txt', 'a')
f.close()
f = open('creds.txt', 'r')
id = f.readline()
f.close()

if not id: authenticate()       
else: print(id)