from django.shortcuts import render
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
	return(render(request,'home.html',{'data':data,'active_page':active_page,'page_content':get_code_format(active_page)}))

def savefile(request):
	my_code = request.GET['code']
	code_loc = request.GET['q']
	with open("/home/bellemanwesley/repos/"+code_loc,'w+') as f:
		f.write(my_code)
	return(render(request,'home.html',{'data':my_code}))

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

