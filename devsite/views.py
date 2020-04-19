from django.shortcuts import render
import os
import requests
import sys
sys.path.insert(0, '/home/ec2-user/devsite/devsite/localviews/')
import content_gen

def landing_page(request):
    return(render(request,"landing.html",{}))

def get_code_format(code_type):
    extension_map = {'py':'python','js':'javascript'}
    if code_type in extension_map:
        code_type = extension_map[code_type]
    page_content = requests.get('https://wkbdevsite.s3.us-east-2.amazonaws.com/'+code_type+'_content.html')
    return page_content.text

def home(request):
    repo_accordion = content_gen.path_accordion("/home/ec2-user/repos")
    return(render(request,'home.html',{'active_page':'biatch','repo_accordion':repo_accordion,'random_thing':'random_thing'}))

def openfile(request):
    code_loc = request.GET['q']
    code_loc_list = code_loc.split('.')
    code_type = code_loc_list[len(code_loc_list)-1]
    with open('/home/ec2-user/repos/'+code_loc) as f:
        data = f.read()
    return(render(request,'home.html',{'data':data,'active_page':'code_page','page_content':get_code_format(code_type),'default_save':code_loc}))

def savefile(request):
    my_code = request.POST['code']
    code_loc = request.POST['q']
    code_loc_list = code_loc.split('.')
    code_type = code_loc_list[len(code_loc_list)-1]
    with open("/home/ec2-user/repos/"+code_loc,'w+') as f:
        f.write(my_code)
    repo_loc = '/home/ec2-user/repos/' + code_loc.split('/')[0]
    os.system('git -C '+repo_loc+' add .')
    os.system('git -C '+repo_loc+" commit -m 'auto commit'")
    os.system('git -C '+repo_loc+' push origin master')
    active_page = request.POST
    return(render(request,'home.html',{'data':my_code,'active_page':'code_page','page_content':get_code_format(code_type),'default_save':code_loc}))

def deploy_code(request):
    deploy_result = requests.get('http://localhost:5000')
    return(render(request,'home.html',{'deploy_result':deploy_result.text,'active_page':'code'}))
