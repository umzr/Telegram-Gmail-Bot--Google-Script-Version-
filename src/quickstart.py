from __future__ import print_function
import os.path
from bs4 import BeautifulSoup
import base64

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import datetime

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://mail.google.com/']

SEARCHING = '<Target Gmail Title>'

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API

    gmail = service.users().messages()
    results = gmail.list(userId='me', labelIds=['INBOX']).execute()
    messages = results.get('messages', [])

    if not messages:
        print("No messages found.")
    else:
        email_Id = search_unposted_message(gmail, messages)
        encorded = RAWbase64(gmail, email_Id)
        done(gmail, email_Id)
        return encorded


def done(gmail, email_Id):
    for email_Id in reversed(email_Id):
        msg_labels = {"addLabelIds": ["Label_1"]}
        gmail.modify(userId='me', id=email_Id, body=msg_labels).execute()


def RAWbase64(gmail, email_Id):
    tmp_message = []
    for email_Ids in email_Id:
        base64_1 = gmail.get(userId='me', id=email_Ids).execute()
        Raw = base64_1["payload"]["parts"][0]["body"]["data"]
        tmp_message.append(decodebase64(Raw))
    return tmp_message


def decodebase64(base64_1):
    msg_str = base64.urlsafe_b64decode(base64_1).decode("utf-8")
    soup = BeautifulSoup(msg_str, 'html.parser')
    s = ''
    for string in soup.stripped_strings:
        strings = string.replace(u'\xa0', u' ')
        s += (strings)
        s += "\n"
    return s
    # print(s)


def search_unposted_message(gmail, messages):
    tmp_email_id = []
    for message in messages:
        label = gmail.get(userId='me', id=message['id']).execute()
        issearch_subject = search_subject(label, SEARCHING)
        if issearch_subject == True:
            isdone = IsDonePostingEmail(label, 'Label_1')
            if isdone == False:
                tmp_email_id.append(message['id'])
            else:
                break
    return tmp_email_id


def IsDonePostingEmail(labelIds, id):
    check = False
    for labelId in labelIds["labelIds"]:
        if labelId == id:
            check = True

    if check == True:
        return True
    else:
        return False


def search_subject(subject, subject_search):
    for header in subject['payload']["headers"]:
        if header['name'] == 'Subject':
            subject = header['value']
            if subject == subject_search:
                return True

if __name__ == '__main__':
    req = main()
    for reqs in reversed(req):
        print("last sync: "+str(datetime.datetime.now() ) + "\n" +reqs)
