from flask import g
from flask.ext.classy import FlaskView
from simple_scheduler.dynamo import DdbConnection, UserStore

class UsersView(FlaskView):
    def __init__(self):
        # Establish a connection on startup (fail fast if something is wrong)
        self.user_store = UserStore(DdbConnection())

    def put(self, user_type, username):
        self.user_store.create_user(user_type, user_name)
        return '{} [{}] created'.format(user_type, username) 

    def get(self, user_type, username):
        return str(self.user_store.get_user(user_type, username))
