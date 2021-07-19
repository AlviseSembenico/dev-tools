from fastapi_login import LoginManager

from .interfaces import MONGO_CLIENT

SECRET = MONGO_CLIENT.auth.secrets.find_one({'_id': 'devtools'}).get('secret')

manager = LoginManager(
    SECRET, 'TO_UPDATE')


@manager.user_loader
def load_user(email: str):  # could also be an asynchronous function
    return MONGO_CLIENT.auth.users.find_one({'email': email})
