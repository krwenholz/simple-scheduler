from flask import Flask, render_template, request
from flask.ext.classy import FlaskView, route
from simple_scheduler.rest_views import UsersView, EventsView
from simple_scheduler.model.event import Event
from collections import namedtuple
import time


class VisualView(FlaskView):
    """
    Provides a templated, nice user interface for our app 
    #TODO: This could/should be done on the client side with something like React
    """
    def __init__(self):
        self.users = UsersView()
        self.events = EventsView()

    def post(self):
        username = request.form['username']
        if 'user-type' in request.form:
            user_type = request.form['user-type']
        else:
            user = self.users.get(username)
            user_type = user['type']
        if 'email' in request.form:
            email = request.form['email']
            print('Creating new user [{}]', username)
            self.users.put(user_type, username, email)
        specialist = None if 'specialist' not in request.form else request.form['specialist']
        events = None
        booked_event = None
        if specialist != None:
            events = self.events.current_month(username, specialist)
            for event in events:
                event['nice_starttime'] = time.ctime(event['starttime'])
                if not Event.from_dict(event).is_free():
                    # the user looking at this page already has an appointment!
                    booked_event = event
        elif user_type == 'specialist':
            events = self.events.current_month(username, username)
        return render_template('user_page.html',
                username = username, 
                specialist = specialist,
                user_type = user_type,
                events = events,
                booked_event = booked_event,
                message = None)

    @route('/delete_event', methods=['POST'])
    def delete_event(self):
        username = request.form['username']
        starttime = int(request.form['starttime'])
        self.events.delete(username, username, starttime)
        return render_template('user_page.html',
                username = username, 
                user_type = user_type,
                message = """You have successfully deleted your meeting for {}.
                (Our hacky sysadmin suggests you go back and refresh the last page.)
                """.format(time.ctime(starttime)))

    @route('/add_client_to_event', methods=['POST'])
    def add_client_to_event(self):
        username = request.form['username']
        starttime = request.form['starttime']
        specialist = request.form['specialist']
        # user puts event on specialist's calendar and will receive event shortly after
        self.events.put(username, specialist, starttime)
        events = self.events.current_month(username, username)
        return render_template('user_page.html',
                username = username, 
                specialist = specialist,
                # Only specialists create new events
                user_type = 'client',
                events = events,
                message = """Your appointment was successfully booked!
                (Our hacky sysadmin suggests you go back and refresh the last page.""")

    @route('/new_event', methods=['POST'])
    def new_event(self):
        # Only specialists create new events
        username = request.form['username']
        starttime = request.form['starttime']
        self.events.put(username, username, starttime)
        return render_template('user_page.html',
                username = username, 
                # Only specialists create new events
                user_type = 'specialist',
                message = """Your new time slot was successfully added!
                (Our hacky sysadmin suggests you go back and refresh the last page.""")


