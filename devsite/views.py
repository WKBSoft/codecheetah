from django.shortcuts import render
import requests

def home(request):
	return(render(request,'home.html'))

def openfile(request):
	code_url = request.GET['q']
	data = requests.get(code_url)
	return(render(request,'home.html',{'data':data}))