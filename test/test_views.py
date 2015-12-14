import boto3
from mock import patch
from simple_scheduler.rest_views import UsersView

class FakeTable:
    def __init__(self):
        self.results = {}
    def query(self, query):
        return self.results['query']
    def get_item(self, get):
        return self.results['get']
    def put_item(self, put):
        return self.results['put']
    def delete_item(self, delete):
        return self.results['delete']

# [{'Item': {'starttime': Decimal('123456'), 'username': 'bobo'}, 'ResponseMetadata': {'HTTPStatusCode': 200, 'RequestId': 'IMJ2ABU72O3C0MGSS3KACV059BVV4KQNSO5AEMVJF66Q9ASUAAJG'}}]

fake_users_table = FakeTable()
fake_users_table.results['get'] = [{'Item': {'username': 'bobo', 'type': 'client', 'email': 'bobo@coco.com', 'create_date': '2015-12-13 16:03:08.532168'}, 'ResponseMetadata': {'HTTPStatusCode': 200, 'RequestId': '1'}}]
fake_users_table.results['put'] = None # just a success

@patch('simple_scheduler.dynamo.DdbConnection')
def test_put_client(ddbMock):
    ddbMock.Table = fake_users_table
    users_view = UsersView()
    assert users_view.put('client', 'bobo', 'bobo@coco.com') == 'success'

@patch('simple_scheduler.dynamo.DdbConnection')
def test_put_specialist(ddbMock):
    ddbMock.Table = fake_users_table
    users_view = UsersView()
    assert users_view.put('specialist', 'bobo', 'bobo@coco.com') == 'success'

@patch('simple_scheduler.dynamo.DdbConnection')
def test_bad_user_type(ddbMock):
    ddbMock.Table = fake_users_table
    users_view = UsersView()
    try:
        users_view.put('', 'bobo', 'bobo@coco.com')
    except ValueError as e:
        assert 'not a valid User type' in e.args[0]
