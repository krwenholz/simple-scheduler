from flask import Flask
import time
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World! I am Kyle's at time " + time.clock()

if __name__ == "__main__":
        app.run()
