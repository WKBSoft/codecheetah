#This webserver application receives and processes requests to update the server. It is an agent running on all systems.
#test comment
from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def hello():
    try:
        os.system("git -C /home/ec2-user/devsite pull origin")
    	return "Deployment successful"
    except:
        return "Deployment failed"

if __name__ == "__main__":
    app.run()
