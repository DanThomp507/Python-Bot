from flask import Flask, request
import json
import requests
from os import environ

app = Flask(__name__)
# app.config.from_pyfile('settings.py')
app.config['PAT'] = environ.get('PAT')
PAT="EAAg5QDZAOmyEBACR7v7a3hrKtKhsSq7X6XIq5cZAEncGz4cSfYXMNsWrKI2PRboedmJZBgfsSjXlciBhZBNKsfpza4jbKjWPTfQwK6MGB5GwIrDSkbEKl8oatQdCVbdYbBS3APZC0hkg0iUWIZAa9CBHu6a0ZB25lGZC6iYmHn7VugZDZD"


# @app.route('/', methods=['GET'])
# def handle_verification():
#   print('Handling Verification')
#   print(request.args.get('hab.verify_token'))
#   if request.args.get('hub.verify_token', '') == 'my_voice_is_my_password_verify_me':
#     print('Verification successful!')
#     return request.args.get('hub.challenge', '')
#   else:
#     print('Verification failed!')
#     return 'Error, wrong validation token'


@app.route('/', methods=['POST'])
def handle_messages():
    print('Handling Messages...')
    payload = request.get_data()
    print(payload)
    for sender, message in messaging_events(payload):
        print('Incoming from %s: %s' % (sender, message))
        send_message(PAT, sender, message)
        return "Ok"


def messaging_events(payload):
    """Generate tuples of (sender_id, message_text)
from the provided payload
    """
    data = json.loads(payload)
    messaging_events = data['entry'][0]['messaging']
    for event in messaging_events:
        if 'message' in event and 'text' in event['message']:
            yield event['sender']['id'],
            event['message']['text'].encode('unicode_escape')
        else:
            yield event['sender']['id'], 'I cannot echo this'


# def send_message(token, recipient, text):
#     """Send the message text to recipient with id recipient.
#     """

# r = requests.post("https://graph.facebook.com/v2.6/me/messages",
#         params={"access_token": token },
#         data=json.dumps({
#       "recipient": {"id": recipient },
#       "message": {"text": text.decode('unicode_escape')}
#     }),
#     headers={'Content-type': 'application/json'})
# if r.status_code != requests.codes.ok: #pylint: disable=no-member
#         print(r.text)
def send_message(token, recipient, text):
    """Send the message text to recipient with id recipient.
    """

    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
        params={"access_token": token},
        data=json.dumps({
            "recipient": {"id": recipient},
            "message": {"text": text.decode('unicode_escape')}
        }),
        headers={'Content-type': 'application/json'})
    if r.status_code != requests.codes.ok:
        print(r.text)

if __name__ == '__main__':
    app.run()
