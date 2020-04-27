import requests
import boto3
from os import path

def deploy(request):
    dest_ip = request.POST['ip_addr']
    deploy_result = requests.get('http://'+des_ip+':5000')
    repo = request.POST['default_save'].split("/")[0]
    if path.isdir("/home/ec2-user/repos/"+repo+"/s3_files"):
        s3_bucket = request.POST['s3_bucket']
    return deploy_result
    