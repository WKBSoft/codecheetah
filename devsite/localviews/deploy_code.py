import requests
import boto3
from os import path
import sys
sys.path.insert(0, '/home/ec2-user/devsite/devsite/localviews/')
import content_gen

def deploy(request):
    dest_ip = request.POST['ip_addr']
    deploy_result = requests.get('http://'+des_ip+':5000')
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
    