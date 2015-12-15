from flask import Flask, render_template
from simple_scheduler.rest_views import UsersView, EventsView

app = Flask(__name__, template_folder='simple_scheduler/templates')
UsersView.register(app)
EventsView.register(app)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
