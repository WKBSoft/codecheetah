import boto3
import os
import sys
from time import sleep
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'scripts/'))
import aws
import deploy_code

def database():
    ec2 = boto3.resource('ec2')
    # create a file to store the key locally
    outfile = open('ec2-keypair.pem','w')
    # call the boto ec2 function to create a key pair
    key_pair = ec2.create_key_pair(KeyName='ec2-keypair')
    # capture the key and store it in a file
    KeyPairOut = str(key_pair.key_material)
    print(KeyPairOut)
    outfile.write(KeyPairOut)
    return 0

    
    
def webserver(github_username, github_repo, hostname, vpc_id, ACCESS_KEY, SECRET_KEY,ssh_key,cheetah_pub_ip,cheetah_priv_ip):
    session = boto3.Session(
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    )
    client = session.client("ec2")
    
    response = client.describe_security_groups()
    security_groups = list(filter(lambda x: x["GroupName"]=="web_servers" and x["VpcId"]==vpc_id,response["SecurityGroups"]))
    if len(security_groups) == 0:
        response = client.create_security_group(
            GroupName='web_servers',
            Description='Ports 80 and 443 open to world and ssh only to CodeCheetah host.',
            VpcId=vpc_id
            )
        security_group_id = response['GroupId']
        client.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {'IpProtocol': 'tcp',
                 'FromPort': 80,
                 'ToPort': 80,
                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp',
                 'FromPort': 443,
                 'ToPort': 443,
                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},             
                {'IpProtocol': 'tcp',
                 'FromPort': 22,
                 'ToPort': 22,
                 'IpRanges': [{'CidrIp': cheetah_pub_ip+'/32'}]},
                {'IpProtocol': 'tcp',
                 'FromPort': 22,
                 'ToPort': 22,
                 'IpRanges': [{'CidrIp': cheetah_priv_ip+'/32'}]}
            ])
    else:
        security_group_id = security_groups[0]['GroupId']
        
    #Returns tuple (private ip, public ip, instance id)
    my_instance = aws.launch_instance(ACCESS_KEY,SECRET_KEY,security_group_id)
    
    with open(os.path.join(BASE_DIR, 'scripts/web_server/nginx-reverse-proxy.conf'),"r") as f:
        nginx_reverse_proxy = f.read()
        
    with open(os.path.join(BASE_DIR, 'scripts/web_server/website_server.service'),"r") as f:
        web_server_service = f.read()
    
    web_server_service = web_server_service.replace("*****replace_with_project_name*****",github_repo)
    
    commands = [
        "curl https://raw.githubusercontent.com/bellemanwesley/devsite/master/scripts/web_server/initiate_web_server.py -o initiate_web_server.py",
        "mkdir keys",
        "python3 initiate_web_server.py "+github_username+" "+github_repo,
        ]
    sent_script = False
    while not sent_script:
        try:
            deploy_code.send_shell_script(my_instance[1],ssh_key,"ubuntu",commands)
            sent_script = True
        except:
            print("Sleeping 5 seconds")
            sleep(5)

    return my_instance[1]
    

with open("/home/ubuntu/keys/aws_key.txt","r") as f:
    keys = f.read().split("\n")

ACCESS_KEY = keys[0]
SECRET_KEY = keys[1]

with open("/home/ubuntu/keys/MyKeyPair.pem","r") as f:
    ssh_key = f.read()
    
#print(deploy_code.send_shell_script(ACCESS_KEY,SECRET_KEY,"i-040c4913ca4ff3401",["pwd","touch hello.txt","echo 'hello'"]))

print(
    webserver(
        "bellemanwesley",
        "vitamova",
        "test.wkbonline.net",
        "vpc-a1788bca",
        ACCESS_KEY,
        SECRET_KEY,
        ssh_key,
        "3.12.250.205",
        "172.31.29.14"
        )
    )