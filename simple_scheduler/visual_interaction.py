from flask import Flask, render_template, request
from flask.ext.classy import FlaskView
from simple_scheduler.rest_views import UsersView, EventsView

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
                if not event.is_free():
                    # the user looking at this page already has an appointment!
                    booked_event = event
        elif user_type == 'specialist':
            events = self.events.current_month(username, username)
        return render_template('user_page.html',
                username = username, 
                specialist = specialist,
                user_type = user_type,
                events = events,
                booked_event = booked_event)

    def delete_event(self):
        username = request.form['username']
        starttime = int(request.form['starttime'])
        specialist = None if 'specialist' not in request.form else request.form['specialist']
        print('we should delete that event ' + starttime)

    def add_client_to_event(self):
        print('let us create this event')

    def new_event(self):
        username = 
        print('let us create this event')

    def get(self, user_type, username):
        return str(self.user_store.get_user(user_type, username))
