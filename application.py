from flask import Flask, render_template, g
from simple_scheduler.users import UsersView

app = Flask(__name__, template_folder='simple_scheduler/templates')
UsersView.register(app)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
