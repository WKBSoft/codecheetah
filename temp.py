import boto3
import boto3
from botocore.config import Config

my_config = Config(
    region_name = 'us-east-1'
)

client = boto3.client("ec2")
response = client.describe_security_groups()
print(list(filter(lambda x: x["GroupName"]=="default" and x["VpcId"]=="vpc-00ed1c93c7b617aa9",response["SecurityGroups"])))