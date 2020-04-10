from django.shortcuts import render
import os
import requests

def get_code_format(active_page):
	page_content = requests.get('https://wkbdevsite.s3.us-east-2.amazonaws.com/'+active_page+'_content.html')
	return page_content.text

def home(request):
	print(request)
	return(render(request,'home.html',{'active_page':'home'}))

def openfile(request):
	code_loc = request.GET['q']
	with open('/home/bellemanwesley/repos/'+code_loc) as f:
		data = f.read()
	active_page = request.GET['active']
	return(render(request,'home.html',{'data':data,'active_page':active_page,'page_content':get_code_format(active_page),'default_save':code_loc}))

def savefile(request):
	my_code = request.GET['code']
	code_loc = request.GET['q']
	with open("/home/bellemanwesley/repos/"+code_loc,'w+') as f:
		f.write(my_code)
	repo_loc = '/home/bellemanwesley/repos/' + code_loc.split('/')[0]
	os.system('git -C '+repo_loc+' add .')
	os.system('git -C '+repo_loc+" commit -m 'auto commit'")
	os.system('git -C '+repo_loc+' push origin master')
	active_page = request.GET['active']
	return(render(request,'home.html',{'data':my_code,'active_page':active_page,'page_content':get_code_format(active_page),'default_save':code_loc}))

#going to get rid of these functions and merge these
def python_page(request):
	active_page = 'python'
	return(render(request,'home.html',{'page_content':get_code_format(active_page),'active_page':active_page}))

def javascript_page(request):
	active_page = 'javascript'
	return(render(request,'home.html',{'page_content':get_code_format(active_page),'active_page':active_page}))

def html_page(request):
	active_page = 'html'
	return(render(request,'home.html',{'page_content':get_code_format(active_page),'active_page':active_page}))

def css_page(request):
	active_page = 'css'
	return(render(request,'home.html',{'page_content':get_code_format(active_page),'active_page':active_page}))

def deploy_code(request):
	deploy_result = requests.get('http://localhost:5000')
	active_page = request.GET['active']
	return(render(request,'home.html',{'page_content':get_code_format(active_page),'deploy_result':deploy_result.text,'active_page':active_page}))
