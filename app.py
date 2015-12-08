from flask import Flask
import time
app = Flask(__name__)

@app.route("/")
def hello():
    return("Hello my beautiful world")

if __name__ == "__main__":
        app.run()
