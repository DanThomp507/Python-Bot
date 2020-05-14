from flask import Flask, request
import json
import requests
import os

app = Flask(__name__)
# app.config.from_pyfile('settings.py')
# app.config['PAT'] = environ.get('PAT')

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["PAT"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


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
