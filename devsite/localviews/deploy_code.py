import requests

def deploy(request):
    deploy_result = requests.get('http://localhost:5000')