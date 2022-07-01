import requests

SESSION = None


def get_session():
    global SESSION
    if not SESSION:
        SESSION = requests.session()
    return SESSION
