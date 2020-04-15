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
    dirs_list = []
    for root, dirs, files in os.walk("/home/ec2-user/repos", topdown=False):
        for name in dirs:
            my_dir = os.path.join(root,name)
            my_dir_list = my_dir.split("/")
            del my_dir_list[0:4]
	    if len(my_dir_list) > 1:
                if my_dir_list[1] != ".git":
            	    my_dir = "/".join(my_dir_list)
            	    dirs_list.append(my_dir)
    return(render(request,'home.html',{'active_page':'code_page','repo_tree':dirs_list}))

def openfile(request):
    code_loc = request.GET['q']
    code_loc_list = code_loc.split('.')
    code_type = code_loc_list[len(code_loc_list)-1]
    with open('/home/ec2-user/repos/'+code_loc) as f:
        data = f.read()
    return(render(request,'home.html',{'data':data,'active_page':'code_page','page_content':get_code_format(code_type),'default_save':code_loc}))

def savefile(request):
    my_code = request.GET['code']
    code_loc = request.GET['q']
    code_loc_list = code_loc.split('.')
    code_type = code_loc_list[len(code_loc_list)-1]
    with open("/home/ec2-user/repos/"+code_loc,'w+') as f:
        f.write(my_code)
    repo_loc = '/home/ec2-user/repos/' + code_loc.split('/')[0]
    os.system('git -C '+repo_loc+' add .')
    os.system('git -C '+repo_loc+" commit -m 'auto commit'")
    os.system('git -C '+repo_loc+' push origin master')
    active_page = request.GET['active']
    return(render(request,'home.html',{'data':my_code,'active_page':'code_page','page_content':get_code_format(code_type),'default_save':code_loc}))

def deploy_code(request):
    deploy_result = requests.get('http://localhost:5000')
    return(render(request,'home.html',{'deploy_result':deploy_result.text,'active_page':'code'}))
