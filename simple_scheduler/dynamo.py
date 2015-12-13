import boto3, os 
from boto3.dynamodb.conditions import Key
from simple_scheduler.model.user import User
from simple_scheduler.model.event import Event

#TODO: retry transient ddb errors (maybe done by boto3) and more intelligently
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

    def get_user(self, user_type, username):
        try:
            return User.from_dict(self.users_table.get_item( 
                Key={'username':username, 'type':user_type}))
        except Exception as e:
            print('User [{}] was not found!'.format(username))
            print('Caught exception {}'.format(e))
            return None

    def create_user(self, user):
        self.users_table.put_item(Item=user.as_ddb_item())

class EventStore:
    """
    Manages event information in DynamoDB
    """
    def __init__(self):
        connection = DdbConnection()
        self.event_table = connection.table('simple-scheduler-events')

    def get_event(self, username, starttime):
        try:
            return Event.from_dict(self.event_table.get_item( 
                Key={'username':username, 'starttime':starttime}))
        except Exception as e:
            print('Event [{}, {}] was not found!'.format(username, starttime))
            print('Caught exception {}'.format(e))
            return None

    def get_events(self, username, min_starttime, max_starttime):
        try:
            ddb_events = self.event_table.query(
                    KeyConditionExpression=Key('username').eq(username) & \
                            Key('starttime').gte(min_starttime) & \
                            Key('starttime').lte(max_starttime))['Items']
            return map(lambda ee: Event.from_ddb(ee['Item']), ddb_events)
        except Exception as e:
            print('Events for [{}, {}, {}] were not found!'.format(
                username, min_starttime, max_starttime))
            print('Caught exception {}'.format(e))
            return None


    def create_event(self, event):
        print('Trying to put event [{}]'.format(event.as_ddb_item()))
        self.event_table.put_item(Item=event.as_ddb_item())

    def delete(self, username, starttime):
        print('Trying to delete event [{}, starttime]'.format(username, starttime))
        self.event_table.delete_item(
                Key={
                    'username' : username,
                    'starttime' : starttime
                    })








