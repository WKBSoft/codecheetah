#This webserver application receives and processes requests to update the server. It is an agent running on all systems.
#Test comment
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run(ssl_context='adhoc')
