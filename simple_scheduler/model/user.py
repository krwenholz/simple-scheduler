from collections import namedtuple

class User(namedtuple('User', 'username type email create_date')):
    types = ['client', 'specialist']

    def __new__(cls, username, user_type, email, create_date):
        if user_type not in User.types:
            raise ValueError('[{}] is not a valid User type'.format(user_type))
        return super().__new__(cls, username, user_type, email, create_date)

    def from_dict(ddb_response):
        user_dict = ddb_response['Item']
        return User(user_dict['username'], 
                user_dict['type'], 
                user_dict['email'], 
                user_dict['create_date'])

    def as_dict(self):
        """
        Just a simple dict representation, because it's simpler than OrderedDict
        """
        return {
                'username' : self.username,
                'type' : self.type,
                'email' : self.email,
                'create_date' : self.create_date
                }
