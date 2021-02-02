import requests
import boto3
from os import path
import sys
import paramiko
import io
from time import sleep
sys.path.insert(0, '/home/ec2-user/devsite/devsite/localviews/')
import content_gen

def deploy(request):
    dest_ip = request.POST['ip_addr']
    deploy_result = requests.get('http://'+dest_ip+':5000')
    repo = request.POST['default_save'].split("/")[0]
    if path.isdir("/home/ec2-user/repos/"+repo+"/s3_files"):
        s3_bucket = request.POST['s3_bucket']
        sub_files = content_gen.list_subpaths("/home/ec2-user/repos/"+repo+"/s3_files")[1]
        s3 = boto3.resource('s3')
        for x in sub_files:
            file = "/".join(x)
            s3_object = s3.Object(s3_bucket,file)
            s3_object.put(
                ACL="public-read",
                body="/home/ec2-user/repos/"+repo+"/s3_files/"+file
            )
    return deploy_result

def send_shell_script(ip,key,username,commands):
    k = paramiko.RSAKey.from_private_key(io.StringIO(key))
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print("connecting")
    c.connect( hostname = ip, username = "ubuntu", pkey = k )
    print("connected")
    channel = c.invoke_shell()
    errors = ""
    output = ""
    for command in commands:
        channel.send(command + "\n")
        while not channel.recv_ready(): #Wait for the server to read and respond
            sleep(0.1)
        sleep(5) #wait enough for writing to (hopefully) be finished
        output = channel.recv(9999) #read in
        print(output.decode('utf-8'))
        sleep(0.1)
    channel.close()
    c.close()
    if errors == "":
        return "success", output
    else:
        return "error", errors, output

with open("/home/ubuntu/keys/MyKeyPair.pem","r") as f:
    ssh_key = f.read()

#commands = ["sudo apt -y install nginx","sudo nginx"]

#my_ip = "18.219.246.51"
#print(send_shell_script(my_ip,ssh_key,"ubuntu",commands))