import boto3
import boto3
from botocore.config import Config

my_config = Config(
    region_name = 'us-east-1'
)

client = boto3.client('route53domains',config=my_config)
print(client.list_domains())