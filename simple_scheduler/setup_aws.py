import os, logging

def setup():
    """
    If we're in a Docker container or whatnot, we need a way to pass in AWS credentials,
    this file sets up those credentials.
    """
    if 'ACCESS_KEY' in os.environ and 'SECRET_KEY' in os.environ:
        logging.info('Found access and secret key in environment variables, so we can set up credentials')
        access_key = os.environ['ACCESS_KEY']
        secret_key = os.environ['SECRET_KEY']

        creds_content = """[default]
        aws_access_key_id = {access_key}
        aws_secret_access_key = {secret_key}""".format(access_key=access_key, secret_key=secret_key)

        creds_file_name = '{}/.aws/credentials'.format(os.environ['HOME'])

        with open(creds_file_name, 'w+') as creds_file:
            creds_file.write(creds_content)

        logging.info('Wrote AWS creds to [{}]'.format(creds_file_name))
    else:
        logging.info('No AWS credentials to configure')
