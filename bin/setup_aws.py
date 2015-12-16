import os

access_key = os.environ['ACCESS_KEY']
secret_key = os.environ['SECRET_KEY']

creds_content = """[default]
aws_access_key_id = {access_key}
aws_secret_access_key = {secret_key}""".format(access_key=access_key, secret_key=secret_key)

creds_file_name = '{}/.aws/credentials'.format(os.environ['HOME'])

with open(creds_file_name, 'w+') as creds_file:
    creds_file.write(creds_content)

print('Wrote AWS creds to [{}]'.format(creds_file_name))
