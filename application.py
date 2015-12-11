from flask import Flask, render_template
from simple_scheduler.dynamo import ConnectionManager, UserStore

app = Flask(__name__)
connection_manager = ConnectionManager()
user_store = UserStore(connection_manager)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/client/<client_name>', methods=['POST'])
def create_client(client_name):
    user_store.create_user(client_name, 'client')
    return 'Client "{}" created'.format(client_name) 

@app.route('/specialist/<specialist_name>', methods=['POST'])
def create_specialist(specialist_name):
    user_store.create_user(specialist_name, 'specialist')
    return 'Specialist "{}" created'.format(specialist_name) 

@app.route('/user/<username>', methods=['GET'])
def get_user(username):
    return user_store.get_user(username)

if __name__ == '__main__':
    app.run(debug=True)
