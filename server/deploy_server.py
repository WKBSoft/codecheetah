#This webserver application receives and processes requests to update the server. It is an agent running on all systems.
#test comment
from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def hello():
    os.system("git -C /home/ec2-user/devsite pull origin")
    os.system("sudo systemctl restart website_server")
    return "Step 2 successful"

if __name__ == "__main__":
    app.run()
