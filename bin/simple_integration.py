#!/usr/bin/env python3
# This is a simple start for an integration test. It assumes there is a 
# client 'client_0', client 'client_1', specialist 'specialist_0', and specialist 'specialist_1'
# TODO: create the clients at start, if needed, and clean up afterwards
from urllib import request
import datetime, calendar, time

def put_event_request(requester, username, time):
    return request.urlopen(request.Request('http://localhost:5000/events/{}/{}/{}'.format(
        requester, username, time), 
        method='PUT'))

def delete_event_request(requester, username, time):
    return request.urlopen(request.Request('http://localhost:5000/events/{}/{}/{}'.format(
        requester, username, time), 
        method='DELETE'))

def current_month_request(requester, username):
    return request.urlopen(request.Request('http://localhost:5000/events/current_month/{}/{}'.format(
        requester, username), 
        method='GET'))


month_start = calendar.timegm(datetime.datetime.today().replace(day=1).timetuple())
print('Putting free time on schedules')
print(put_event_request('specialist_0', 'specialist_0', month_start).read())
print(put_event_request('specialist_0', 'specialist_0', month_start + 600).read())

print('Looking at free events for this month')
print(current_month_request('specialist_0', 'specialist_0').read())
print(current_month_request('client_0', 'specialist_0').read())

print('Booking a specialist_0 slot for client_0')
print(put_event_request('client_0', 'specialist_0', month_start).read())
print('Sleeping a few seconds because no human is this fast!')
time.sleep(6)
print(current_month_request('client_0', 'client_0').read())
print(current_month_request('client_0', 'specialist_0').read())

print('Looking at specialist_0 schedule from client_1')
print(current_month_request('client_1', 'specialist_0').read())

print('Cleaning out the schedules')
print(delete_event_request('specialist_0', 'specialist_0', month_start).read())
print(delete_event_request('specialist_0', 'specialist_0', month_start + 600).read())

