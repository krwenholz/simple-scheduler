from collections import namedtuple

class Event(namedtuple('Event', 'username starttime partner')):
    """
    Store an event (an appointment) between one user and another. Events are
    always one hour (from starttime to starttime + 1 hour).
    If no partner is specified, it implies the hour period is free and bookable.
    """

    FREE_TIME = 'FREE_TIME'

    def from_dict(event_dict):
        partner = event_dict['partner'] if 'partner' in event_dict else Event.FREE_TIME
        return Event(event_dict['username'], 
                event_dict['starttime'],
                partner)

    def from_ddb(ddb_response):
        event_dict = ddb_response['Item']
        return Event.from_dict(event_dict)

    def as_dict(self):
        """
        Just a simple dict representation, because it's simpler than OrderedDict
        """
        return {
                'username' : self.username,
                'starttime' : self.starttime,
                'partner' : self.partner
                }

    def is_free(self):
        return self.partner == Event.FREE_TIME
