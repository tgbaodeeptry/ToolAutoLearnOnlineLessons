import firebase_admin
from firebase_admin import credentials, db


app = None


# connect
def connect():
    global app
    cred = credentials.Certificate("key.json")
    app = firebase_admin.initialize_app(cred, {
        "databaseURL": "https://toolautolearn-default-rtdb.firebaseio.com/"
    })


def get_all_info():
    return db.reference('/').get()
