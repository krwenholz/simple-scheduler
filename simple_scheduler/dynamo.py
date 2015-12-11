import boto3, os 
from boto3.dynamodb.conditions import Key
from datetime import datetime

class ConnectionManager:
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
            raise Exception("Failed to connect to users table", e)

class UserStore:
    """
    Manages user information in DynamoDB
    TODO: I should create a namedtuple class to represent users
    """
    def __init__(self, connection_manager):
        self.connection_manager = connection_manager
        self.users_table = self.connection_manager.table('simple-scheduler-users')

    def get_user(self, username):
        try:
            items = self.users_table.query(
                    KeyConditionExpression=Key('username').eq(username))['Items']
        except Exception as e:
            #TODO: update this error handling to be more polite with Boto3
            print('User [{}] was not found!'.format(username))
            print('caught exception {}'.format(e))
            return None
        if len(items) > 1:
            raise Exception('Too many users found for username [{}]'.format(username))
        return items[0]

    def create_user(self, username, user_type):
        create_date = str(datetime.now())
        self.users_table.put_item(
                Item={
                    "username" : username,
                    "type" : user_type,
                    "create_date" : create_date
                    })




