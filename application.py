from flask import Flask, render_template
from simple_scheduler.rest_views import UsersView, EventsView
from simple_scheduler.visual_interaction import VisualView

template_path = 'simple_scheduler/templates'

app = Flask(__name__, template_folder=template_path)
UsersView.register(app)
EventsView.register(app)
VisualView.register(app)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
