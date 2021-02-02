import boto3
import boto3
from botocore.config import Config
from time import sleep
import io
import paramiko

def list_hosted_zones(ACCESS_KEY,SECRET_KEY):
    my_config = Config(
        region_name = 'us-east-1'
    )
    session = boto3.Session(
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    )
    client = session.client('route53',config=my_config)    
    hosted_zones_response = client.list_hosted_zones()["HostedZones"]
    hosted_zones = []
    for x in hosted_zones_response:
        if x["Name"] != "local.":
            hosted_zones.append({"Id":x["Id"],"Name":x["Name"]})
    return hosted_zones

def list_record_sets(HostedZoneId,ACCESS_KEY,SECRET_KEY):
    my_config = Config(
        region_name = 'us-east-1'
    )
    session = boto3.Session(
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    )
    client = session.client('route53',config=my_config)
    sets_response = client.list_resource_record_sets(HostedZoneId=HostedZoneId)
    sets = []
    for x in sets_response["ResourceRecordSets"]:
        y = x["Name"]
        y = y[0:len(y)-1]
        if y not in sets:
            sets.append(y)
    return sets
    
def list_record_sets_user(ACCESS_KEY,SECRET_KEY):
    my_hosted_zones = list_hosted_zones(ACCESS_KEY,SECRET_KEY)
    record_sets = []
    for x in my_hosted_zones:
        record_sets_zone = list_record_sets(x["Id"],ACCESS_KEY,SECRET_KEY)
        for y in record_sets_zone:
            if y not in record_sets:
                record_sets.append(y)
    return record_sets

def launch_instance(ACCESS_KEY,SECRET_KEY,security_group):
    session = boto3.Session(
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    )
    ec2 = session.resource("ec2")
    instance = ec2.create_instances(
        MinCount = 1,
        MaxCount = 1,
        ImageId = 'ami-0dd9f0e7df0f0a138',
        InstanceType = 't2.micro',
        KeyName = 'MyKeyPair',
        SecurityGroupIds = [security_group]
        )
    instance_id = instance[0].id
    instance_pub_ip = None
    while instance_pub_ip == None:
        instance_info = ec2.Instance(instance_id)
        instance_pub_ip = instance_info.public_ip_address
        print("sleeping for 5 seconds")
        sleep(5)
    sleep(5)
    return instance_info.private_ip_address,instance_info.public_ip_address,instance_id

with open("/home/ubuntu/keys/aws_key.txt","r") as f:
    keys = f.read().split("\n")
ACCESS_KEY = keys[0]
SECRET_KEY = keys[1]

with open("/home/ubuntu/keys/MyKeyPair.pem","r") as f:
    ssh_key = f.read()