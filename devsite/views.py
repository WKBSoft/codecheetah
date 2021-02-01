# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import os
import time
import requests
import sys
import json
import boto3
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'scripts/'))
import content_gen
import deploy_code

def logged_in_header():
    with open(os.path.join(BASE_DIR,"templates/sub_templates/logged_in_header.html"),"r") as f:
        return f.read()

def userpass_get():
    s3 = boto3.resource('s3')
    object = s3.Object('wkbdevsite','users/userpass.json')
    return json.load(object.get()['Body'])
    
def userpass_put(data):
    s3 = boto3.resource('s3')
    object = s3.Object('wkbdevsite','users/userpass.json')
    return object.put(Body=json.dumps(data).encode("utf-8"))

def check_login(request):
    #Returns 3 results 0=correct login, 1=incorrect login, 2=no account
    login_email = request.POST["email"]
    login_token = request.POST["login_token"]
    if login_email != "" and login_token != "":
        s3 = boto3.resource('s3')
        object = s3.Object('wkbdevsite','users/userpass.json')
        userpass = json.load(object.get()['Body'])
    else:
        return 1
    if login_email in userpass:
        user_info = userpass[login_email]
    else:
        return 2
    if user_info["token"] == login_token:
        return 0
    else:
        return 1
        

def landing_page(request):
    return(render(request,"landing.html",{}))

def submit_login(request):
    uname = request.POST['uname']
    psswd = request.POST['psswd']
    with open(os.path.join(BASE_DIR, 'keys/users.json'),'r') as f:
        users = json.loads(f.read())
    if uname in users:
        if users[uname] == psswd:
            response = HttpResponse("thisismybasicsessionkey", content_type="text/plain")
            return response
        else:
            return HttpResponse("login_failure", content_type="text/plain")
    else:
        return HttpResponse("login_failure", content_type="text/plain")
        
def my_network(request):
    return render(request,"my_network.html",{"header":logged_in_header()})

def get_code_format(code_type):
    extension_map = {'py':'python','js':'javascript'}
    if code_type in extension_map:
        code_type = extension_map[code_type]
    page_content = requests.get('https://wkbdevsite.s3.us-east-2.amazonaws.com/'+code_type+'_content.html')
    return page_content.text

def home(request):
    if 'cheetah_key' not in request.POST:
        return HttpResponseRedirect('/login')
    repo_accordion = content_gen.path_accordion("/home/ec2-user/repos")
    code_type = "plaintext"
    return(render(request,'home.html',{'active_page':'code_page','repo_accordion':repo_accordion,'page_content':get_code_format(code_type)}))

def openfile(request):
    code_loc = request.GET['q']
    available_files = content_gen.list_contents("/home/ubuntu/repos")[1]
    if code_loc in available_files:
        code_loc_list = code_loc.split('.')
        code_type = code_loc_list[len(code_loc_list)-1]
        with open('/home/ubuntu/repos/'+code_loc) as f:
            data = f.read()
    else:
        data = "No such file"
        code_type = "plaintext"
    repo_accordion = content_gen.path_accordion("/home/ubuntu/repos")
    return(render(request,'home.html',{'data':data,'active_page':'code_page','page_content':get_code_format(code_type),'default_save':code_loc,'repo_accordion':repo_accordion}))

def savefile(request):
    my_code = request.POST['script']
    code_loc = request.POST['q']
    code_loc_list = code_loc.split('.')
    code_type = code_loc_list[len(code_loc_list)-1]
    repo_loc = '/home/ec2-user/repos/'+code_loc.split('/')[0]
    if check_login(request):
        #try:
        with open("/home/ec2-user/repos/"+code_loc,'w+') as f:
            f.write(my_code.encode("utf-8"))
        os.system('git -C ' +repo_loc+ ' add .')
        os.system('git -C ' +repo_loc+ " commit -m 'auto commit'")
        os.system('git -C ' +repo_loc+ ' push origin master')
        response = "Success"
        return HttpResponseRedirect("/openfile?q="+code_loc)
        #except:
            #response = "Failure"
    else:
        response = "Access denied"
    repo_accordion = content_gen.path_accordion("/home/ec2-user/repos")
    return HttpResponse(response,"text/plain")

def deploy_button(request):
    if check_login(request):
        deploy_result = deploy_code.deploy(request)
    else:
        deploy_result = "Authentication failed!"
    return HttpResponse(deploy_result,"text/plain")
