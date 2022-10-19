import requests, json, os

url_fb = f"https://graph.facebook.com/v9.0/me/messages?access_token={os.environ.get('TOKEN_FB')}"


def send_messages(id_fb, mess):
    data = {
        "messaging_type": "MESSAGE_TAG",
        "recipient": {
            "id": id_fb
        },
        "message": {
            "text": mess
        },
        "tag": "POST_PURCHASE_UPDATE"
    }

    headers = {'Content-type': 'application/json'}

    r = requests.post(url_fb, data=json.dumps(data), headers=headers)

    if r.status_code != 200:
        print(r.text)
