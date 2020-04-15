from django.shortcuts import render
import os
import requests

def get_code_format(code_type):
    extension_map = {'py':'python','js':'javascript'}
    if code_type in extension_map:
        code_type = extension_map[code_type]
    page_content = requests.get('https://wkbdevsite.s3.us-east-2.amazonaws.com/'+code_type+'_content.html')
    return page_content.text

def home(request):
    my_repos = []
    for root, dirs, files in os.walk(".", topdown=False):
        for name in dirs:
            my_repos.append(os.path.join(root, name))
    return(render(request,'home.html',{'active_page':'code_page';'repos_list':my_repos}))

def openfile(request):
    code_loc = request.GET['q']
    code_loc_list = code_loc.split('.')
    code_type = code_loc_list[len(code_loc_list)-1]
    with open('/home/bellemanwesley/repos/'+code_loc) as f:
        data = f.read()
    return(render(request,'home.html',{'data':data,'active_page':'code_page','page_content':get_code_format(code_type),'default_save':code_loc}))

def savefile(request):
    my_code = request.GET['code']
    code_loc = request.GET['q']
    code_loc_list = code_loc.split('.')
    code_type = code_loc_list[len(code_loc_list)-1]
    with open("/home/bellemanwesley/repos/"+code_loc,'w+') as f:
        f.write(my_code)
    repo_loc = '/home/bellemanwesley/repos/' + code_loc.split('/')[0]
    os.system('git -C '+repo_loc+' add .')
    os.system('git -C '+repo_loc+" commit -m 'auto commit'")
    os.system('git -C '+repo_loc+' push origin master')
    active_page = request.GET['active']
    return(render(request,'home.html',{'data':my_code,'active_page':'code_page','page_content':get_code_format(code_type),'default_save':code_loc}))

def deploy_code(request):
    deploy_result = requests.get('http://localhost:5000')
    return(render(request,'home.html',{'deploy_result':deploy_result.text,'active_page':'code'}))
