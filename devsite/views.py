from django.shortcuts import render
from django.http import HttpResponseRedirect
import os
import time
import requests
import sys
import json
sys.path.insert(0, '/home/ec2-user/devsite/devsite/localviews/')
import content_gen

def check_login(request):
    return True

def landing_page(request):
    return(render(request,"landing.html",{}))

def submit_login(request):
    uname = request.POST['uname']
    psswd = request.POST['psswd']
    with open('/home/ec2-user/keys/users.json','r') as f:
        users = json.loads(f.read())
    if uname in users:
        if users[uname] == psswd:
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/login/')
    else:
        return HttpResponseRedirect('/login/')
        

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
    my_code = request.POST['code']
    code_loc = request.POST['q']
    code_loc_list = code_loc.split('.')
    code_type = code_loc_list[len(code_loc_list)-1]
    repo_loc = '/home/ec2-user/repos/' + code_loc.split('/')[0]
    if check_login(request):
        with open("/home/ec2-user/repos/"+code_loc,'w+') as f:
            f.write(my_code)
        os.system('git -C '+repo_loc+' add .')
        os.system('git -C '+repo_loc+" commit -m 'auto commit'")
        os.system('git -C '+repo_loc+' push origin master')
    repo_accordion = content_gen.path_accordion("/home/ec2-user/repos")
    return(render(request,'home.html',{'data':my_code,'active_page':'code_page','page_content':get_code_format(code_type),'default_save':code_loc,'repo_accordion':repo_accordion}))

def deploy_code(request):
    if check_login(request):
        deploy_result = requests.get('http://localhost:5000')
    repo_accordion = content_gen.path_accordion("/home/ec2-user/repos")
    return(render(request,'home.html',{'active_page':'code_page','repo_accordion':repo_accordion}))
