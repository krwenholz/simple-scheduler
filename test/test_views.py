import boto3
from boto3.dynamodb.types import Decimal
from boto3.exceptions import ResourceLoadException
from mock import patch, MagicMock
from simple_scheduler.rest_views import UsersView, EventsView

#TODO: refactor tests into unittest2 classes and use mock more sanely

###########################################################################
# User view tests
###########################################################################
def prep_user_view(ddbMock):
    fake_users_table = MagicMock()
    fake_users_table.get_item.return_value = {'Item': {'username': 'bobo', 'type': 'client', 'email': 'bobo@coco.com', 'create_date': '2015-12-13 16:03:08.532168'}, 'ResponseMetadata': {'HTTPStatusCode': 200, 'RequestId': '1'}}
    fake_users_table.put_item.return_value = None # just a success
    instance = ddbMock.return_value
    instance.table.return_value = fake_users_table
    return UsersView()

@patch('simple_scheduler.dynamo.DdbConnection')
def test_put_client(ddbMock):
    users_view = prep_user_view(ddbMock)
    assert users_view.put('client', 'bobo', 'bobo@coco.com') == 'success'

@patch('simple_scheduler.dynamo.DdbConnection')
def test_put_specialist(ddbMock):
    users_view = prep_user_view(ddbMock)
    assert users_view.put('specialist', 'bobo', 'bobo@coco.com') == 'success'

@patch('simple_scheduler.dynamo.DdbConnection')
def test_bad_user_type(ddbMock):
    users_view = prep_user_view(ddbMock)
    e = None
    try:
        users_view.put('', 'bobo', 'bobo@coco.com')
    except ValueError as exc:
        e = exc
    assert 'not a valid User type' in e.args[0]

@patch('simple_scheduler.dynamo.DdbConnection')
def test_get_user(ddbMock):
    users_view = prep_user_view(ddbMock)
    user = users_view.get('client', 'bobo')
    assert 'bobo' in user and 'client' in user

###########################################################################
# Event view tests
###########################################################################
existing_events = {
        ('bobo', 123456): 
            {'Item': {'starttime': Decimal('123456'), 'username': 'bobo'}, 'ResponseMetadata': {'HTTPStatusCode': 200, 'RequestId': '1'}},
        ('coco', 23):
            {'Item': {'starttime': Decimal('23'), 'username': 'bobo'}, 'ResponseMetadata': {'HTTPStatusCode': 200, 'RequestId': '2'}},
        ('bobo', 1):
            {'Item': {'starttime': Decimal('23'), 'username': 'bobo', 'partner': 'coco'}, 'ResponseMetadata': {'HTTPStatusCode': 200, 'RequestId': '2'}},
        ('dodo', 1):
            {'Item': {'starttime': Decimal('23'), 'username': 'dodo', 'partner': 'coco'}, 'ResponseMetadata': {'HTTPStatusCode': 200, 'RequestId': '2'}}
            }
def get_item_results(Key=None):
    fake_key = (Key['username'], Key['starttime'])
    if fake_key in existing_events:
        return existing_events[fake_key]
    raise ResourceLoadException('[{}] does not exist'.format(Key))

def prep_events_view(ddbMock):
    fake_events_table = MagicMock()
    fake_events_table.get_item.side_effect = get_item_results
    fake_events_table.put_item.return_value =  None # just a success
    instance = ddbMock.return_value
    instance.table.return_value = fake_events_table
    return EventsView()

@patch('simple_scheduler.dynamo.DdbConnection')
def test_put_free_time(ddbMock):
    event_view = prep_events_view(ddbMock)
    assert event_view.put('bobo', 'bobo', '777') == 'success'

@patch('simple_scheduler.dynamo.DdbConnection')
def test_put_new_event(ddbMock):
    #free time needs to exist for a meeting and requester can't be "recipient"
    event_view = prep_events_view(ddbMock)
    assert event_view.put('coco', 'bobo', '123456') == 'success'

@patch('simple_scheduler.dynamo.DdbConnection')
def test_put_event_overwrite_not_allowed(ddbMock):
    event_view = prep_events_view(ddbMock)
    # book the already booked meeting
    e = None
    try:
        event_view.put('tommy', 'bobo', '1')
    except ValueError as exc:
        e = exc
    assert 'not your schedule' in e.args[0]

@patch('simple_scheduler.dynamo.DdbConnection')
def test_put_event_requester_already_booked(ddbMock):
    event_view = prep_events_view(ddbMock)
    event_view.event_store.event_table.results['get']['Item']['partner'] = 'coco'
    # book the meeting
    e = None
    try:
        event_view.put('dodo', 'bobo', '1') == 'success'
    except ValueError as exc:
        e = exc
    assert 'not your schedule' in e.args[0]


