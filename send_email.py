
from __future__ import print_function
import httplib2
import os
import sys
import json

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import email.mime.text
import base64

gArgVideoTitle = ''
gArgVideoURL = ''

#preprocess custom arguments before the api argparser does so we can use custom args
for arg in sys.argv:
    if arg.startswith('-VideoTitle='):
        gArgVideoTitle = arg[12:]
    elif  arg.startswith('-VideoURL='):
        gArgVideoURL = arg[10:]

    
for arg in sys.argv:
    sys.argv.remove(arg)

if gArgVideoTitle is '':
    exit('No -VideoTitle= argument was found')
if gArgVideoURL is '':
    exit('No -VideoURL= argument was found')


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

"""
TODO: credentials file should be stored in the local directory, not the user directory
"""

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.modify'
CLIENT_SECRET_FILE = 'client_secrets.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.dirname(os.path.realpath(__file__))
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def create_message(sender, to, subject, message_text):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = email.mime.text.MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  raw = base64.urlsafe_b64encode(message.as_string())
  raw = raw.decode()
  return {'raw': raw}


def send_message(service, user_id, message):
    """Send an email message.

    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

    Returns:
    Sent Message.
    """

    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print ('Message Id: %s' % message['id'])
    return message



def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    results = service.users().labels().list(userId='me').execute()

    messageSender = gConfigJson['Email']['Sender']
    messageRecipients = gConfigJson['Email']['Recipients']
    messageSubject = gArgVideoTitle + ' Uploaded'
    messageText = '''Automatic upload process completed successfully for %s. 

    %s

    This video may still be processing, if the link fails to work or the video quality appears poor, check back in 10 minutes.
    ''' % (gArgVideoTitle, gVideoURL)
    

    message = create_message(messageSender, messageRecipients, messageSubject, messageText)
    send_message(service, 'me', message = message)


#quick and dirty read of some json files. Not great because we're assuming these files exist
gConfigJson = ''
gUploadInfoJson = ''

with open(os.path.dirname(os.path.realpath(__file__)) + '\\Config.json') as data_file:
    gConfigJson = json.load(data_file)



gVideoURL = gArgVideoURL

if __name__ == '__main__':
    main()

