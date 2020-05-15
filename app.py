from flask import Flask, request
import json
import requests
import os
import sys
from datetime import datetime
import config

PAT_KEY = config.PAT_KEY
print(PAT)
app = Flask(__name__)

@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == PAT_KEY:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200

@app.route('/', methods=['POST'])
def webhook():

    data = request.get_json()
    print(data)

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"): 

                    sender_id = messaging_event["sender"]["id"]       
                    recipient_id = messaging_event["recipient"]["id"] 
                    message_text = messaging_event["message"]["text"] 

                    send_message(sender_id, "roger that!")

                if messaging_event.get("delivery"):
                    pass

                if messaging_event.get("optin"):
                    pass

                if messaging_event.get("postback"):
                    pass

    return "ok", 200


def send_message(recipient_id, message_text):

    print("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": PAT_KEY
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        print(r.status_code)
        print(r.text)


# def print(msg, *args, **kwargs):  # simple wrapper for logging to stdout on heroku
#     try:
#         if type(msg) is dict:
#             msg = json.dumps(msg)
#         else:
#             msg = unicode(msg).format(*args, **kwargs)
#         print("{}: {}".format(datetime.now(), msg))
#     except UnicodeEncodeError:
#         pass  # squash logging errors in case of non-ascii text
#     sys.stdout.flush()

if __name__ == '__main__':
    app.run()
