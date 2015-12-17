from boto3.dynamodb.conditions import Key
from boto3.exceptions import NoVersionFound, ResourceLoadException, RetriesExceededError
from simple_scheduler.model.user import User
from simple_scheduler.model.event import Event
import boto3

#TODO: retry transient ddb errors (some done by boto3) and more intelligently
# catch exceptions

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
    """
    def __init__(self):
        connection = DdbConnection()
        self.users_table = connection.table('simple-scheduler-users')

    def get_user(self, username):
        try:
            response = self.users_table.query( 
                    KeyConditionExpression=Key('username').eq(username))['Items']
            if len(response) == 0: return None
            return User.from_dict(response[0])
        except (NoVersionFound, ResourceLoadException, RetriesExceededError) as e:
            return None

    def create_user(self, user):
        self.users_table.put_item(Item=user.as_dict())

class EventStore:
    """
    Manages event information in DynamoDB
    """
    def __init__(self):
        connection = DdbConnection()
        self.event_table = connection.table('simple-scheduler-events')

    def get_event(self, username, starttime):
        try:
            response = self.event_table.get_item( 
                    Key={'username': username, 'starttime': starttime})
            if 'Item' not in response: return None
            return Event.from_ddb(response)
        except (NoVersionFound, ResourceLoadException, RetriesExceededError) as e:
            return None

    def get_events(self, username, min_starttime, max_starttime):
        try:
            # ddb does between exclusively, so we need to bump out our bounds 
            min_starttime -= 1
            max_starttime += 1
            ddb_events = self.event_table.query(
                    KeyConditionExpression=Key('username').eq(username) & \
                            Key('starttime').between(min_starttime, max_starttime))['Items']
            return map(lambda ee: Event.from_dict(ee), ddb_events)
        except (NoVersionFound, ResourceLoadException, RetriesExceededError) as e:
            return None


    def create_event(self, event):
        self.event_table.put_item(Item=event.as_dict())

    def delete(self, username, starttime):
        self.event_table.delete_item(
                Key={
                    'username' : username,
                    'starttime' : starttime
                    })








