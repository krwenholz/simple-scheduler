import boto3, os 
from boto3.dynamodb.conditions import Key
from datetime import datetime
from simple_scheduler.model.user import User

class DdbConnection:
    """
    An abstraction for establishing connections to DynamoDB and managing our
    basic tables: users and calendars
    XXX: Reads AWS secrets from environment variables right now, this should 
        be improved: allow config file or command line args
    """
    def __init__(self):
        """
        Return our basic DynamoDB connection
        TODO: connect to a local test instance of DynamoDB when appropriate
        """
        self.db = boto3.resource('dynamodb')

    def table(self, name):
        try:
            return self.db.Table(name)
        except Exception as e:
            raise Exception('Failed to connect to users table', e)

class UserStore:
    """
    Manages user information in DynamoDB
    TODO: I should create a namedtuple class to represent users
    """
    def __init__(self):
        connection = DdbConnection()
        self.users_table = connection.table('simple-scheduler-users')

    def get_user(self, user_type, username):
        try:
            return User.from_ddb(self.users_table.get_item( 
                Key={'username':username, 'type':user_type}))
        except Exception as e:
            #TODO: update this error handling to be more polite with Boto3
            # and retry
            print('User [{}] was not found!'.format(username))
            print('Caught exception {}'.format(e))
            return None

    def create_user(self, user):
        self.users_table.put_item(
                Item={
                    'username' : user.username,
                    'type' : user.type,
                    'email' : user.email,
                    'create_date' : user.create_date 
                    })




