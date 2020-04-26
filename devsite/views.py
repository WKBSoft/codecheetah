# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import os
import time
import requests
import sys
import json
sys.path.insert(0, '/home/ec2-user/devsite/devsite/localviews/')
import content_gen
import deploy_code

#random comment 3

def check_login(request):
	return request.POST['cheetah_key'] == "thisismybasicsessionkey"

def landing_page(request):
    return(render(request,"landing.html",{}))

def submit_login(request):
    uname = request.POST['uname']
    psswd = request.POST['psswd']
    with open('/home/ec2-user/keys/users.json','r') as f:
        users = json.loads(f.read())
    if uname in users:
        if users[uname] == psswd:
            response = HttpResponse("thisismybasicsessionkey", content_type="text/plain")
            return response
        else:
            return HttpResponse("login_failure", content_type="text/plain")
    else:
        return HttpResponse("login_failure", content_type="text/plain")
        

def get_code_format(code_type):
    extension_map = {'py':'python','js':'javascript'}
    if code_type in extension_map:
        code_type = extension_map[code_type]
    page_content = requests.get('https://wkbdevsite.s3.us-east-2.amazonaws.com/'+code_type+'_content.html')
    return page_content.text

def home(request):
    repo_accordion = content_gen.path_accordion("/home/ec2-user/repos")
    code_type = "plaintext"
    return(render(request,'home.html',{'active_page':'code_page','repo_accordion':repo_accordion,'page_content':get_code_format(code_type)}))

def openfile(request):
    code_loc = request.GET['q']
    available_files = content_gen.list_contents("/home/ec2-user/repos")[1]
    if code_loc in available_files:
        code_loc_list = code_loc.split('.')
        code_type = code_loc_list[len(code_loc_list)-1]
        with open('/home/ec2-user/repos/'+code_loc) as f:
            data = f.read()
    else:
        data = "No such file"
        code_type = "plaintext"
    repo_accordion = content_gen.path_accordion("/home/ec2-user/repos")
    return(render(request,'home.html',{'data':data,'active_page':'code_page','page_content':get_code_format(code_type),'default_save':code_loc,'repo_accordion':repo_accordion}))

def savefile(request):
    my_code = request.POST['script']
    code_loc = request.POST['q']
    code_loc_list = code_loc.split('.')
    code_type = code_loc_list[len(code_loc_list)-1]
    repo_loc = '/home/ec2-user/repos/'+code_loc.split('/')[0]
    if check_login(request):
        try:
            with open("/home/ec2-user/repos/"+code_loc,'w+') as f:
                f.write(my_code)
            os.system('git -C ' +repo_loc+ ' add .')
            os.system('git -C ' +repo_loc+ " commit -m 'auto commit'")
            os.system('git -C ' +repo_loc+ ' push origin master')
            response = "Success"
        except:
            response = "Failure"
    else:
        response = "Access denied"
    return HttpResponse(response,"text/plain")

def deploy_button(request):
    if check_login(request):
        deploy_result = deploy_code.deploy(request)
    else:
        deploy_result = "Authentication failed!"
    return HttpResponse(deploy_result,"text/plain")
