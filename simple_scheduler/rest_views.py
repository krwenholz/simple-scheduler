from flask import request, url_for
from flask.ext.classy import FlaskView
from simple_scheduler.dynamo import UserStore, EventStore
from simple_scheduler.model.user import User
from simple_scheduler.model.event import Event
import datetime, calendar

class UsersView(FlaskView):
    """
    Provides the RESTful interface for our user data.
    """
    def __init__(self):
        # Establish a connection on startup (fail fast if something is wrong)
        self.user_store = UserStore()

    def put(self, user_type, username, email):
        self.user_store.create_user(User(username, user_type, email, str(datetime.datetime.now())))
        return 'success'

    def get(self, username):
        user = self.user_store.get_user(username)
        return None if user == None else user.as_dict()

class EventsView(FlaskView):
    """
    Provides the RESTful interface for our events.
    """
    def __init__(self):
        self.event_store = EventStore()

    def put(self, requester, username, starttime):
        #TODO: some of the conditional put logic should be done with conditional puts to DDB
        """
        Attempts to put an event on username's calendar to meet with requester.
        Requester will receive the same event on their calendar through an
        asynchronous process. If requester is the same as user, then the event
        put is for free time
        """
        starttime = int(starttime)
        #TODO how do we block off full hour chunks?
        # verify user can put event on other person or their own calendar
        user_event = self.event_store.get_event(username, starttime)
        if (requester != username and user_event is None) or \
                (user_event is not None and not user_event.is_free()):
            raise ValueError('You can not create an event where no free time exists or is not your schedule')
        # ensure requester isn't already booked if putting time on someone else's calendar
        if requester != username:
            user_event = self.event_store.get_event(requester, starttime)
            if user_event is not None and not user_event.is_free():
                raise ValueError('You are already booked for [{}]'.format(starttime))
        partner = requester if requester != username else Event.FREE_TIME
        self.event_store.create_event(Event(username, starttime, partner))
        return 'success'

    def delete(self, requester, username, starttime):
        """
        Delete's the event off of username's calendar. requester's calendar
        will be updated by an asynchronous process.
        """
        starttime = int(starttime)
        user_event = self.event_store.get_event(username, starttime)
        if user_event is None:
            raise ValueError('No event to delete!')
        if (requester != user_event.partner) and (requester != user_event.username):
            raise ValueError('[{}] can not cancel the event for [{}, {}] at [{}]'.format(
                requester, user_event.username, user_event.partner, starttime))
        self.event_store.delete(username, starttime)
        return 'success'

    def current_month(self, requester, username):
        # get first and last days of the month
        month_start = datetime.datetime.today().replace(day=1, hour=0, minute=0)
        max_day_num = calendar.monthrange(month_start.year, month_start.month)[1]
        month_end = datetime.datetime.now().replace(day=max_day_num, hour=23, minute=59)
        # get those days as regular numbers
        month_start = calendar.timegm(month_start.timetuple())
        month_end = calendar.timegm(month_end.timetuple())
        print('Searching for username [{}] events between [{} and [{}]'.format(
            username, month_start, month_end))
        events = self.event_store.get_events(username, month_start, month_end)
        return list(map(lambda e: e.as_dict(), filter(lambda e: EventsView.__is_visible(requester, e), events)))
        

    def __is_visible(username, event):
        """
        A user can see an event if it involves them or represents free time
        """
        return (username == event.username) or \
                (username == event.partner) or \
                event.is_free()


