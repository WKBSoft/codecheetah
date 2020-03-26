from django.shortcuts import render
import requests

def home(request):
	return(render(request,'home.html'))

def openfile(request):
	return(render(request,'home.html'))
