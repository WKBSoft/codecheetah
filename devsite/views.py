from django.shortcuts import render
import requests

def home(request):
	return(render(request,'home.html'))

def openfile(request):
	code_loc = request.GET['q']
	with open('/home/bellemanwesley/repos/'+code_loc) as f:
		data = f.read()
	return(render(request,'home.html',{'data':data}))