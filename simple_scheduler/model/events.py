from collections import namedtuple

class Event(namedtuple('Event', 'username datetime type create_date')):
    def from_ddb(ddb_response):
        event_dict = ddb_response['Item']
        return User(user_dict['username'], 
                user_dict['type'], 
                user_dict['email'], 
                user_dict['create_date'])
