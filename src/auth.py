from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

USERS = {'admin': 'admin'}  # YWRtaW46YWRtaW4=


@auth.verify_password
def verify_password(username: str, password: str) -> bool:
    return USERS.get(username) == password
