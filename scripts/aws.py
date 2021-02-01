import boto3
import boto3
from botocore.config import Config

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

with open("/home/ubuntu/keys/aws_key.txt","r") as f:
    keys = f.read().split("\n")
ACCESS_KEY = keys[0]
SECRET_KEY = keys[1]

print(list_record_sets_user(ACCESS_KEY,SECRET_KEY))