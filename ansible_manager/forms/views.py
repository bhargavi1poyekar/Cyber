from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
# Create your views here.

def dashboard(request):
    return render(request,'forms/main.html')

def launch_vm_request(request):
    return render(request,'forms/vm_request.html')

def new_vm(request):
    if request.method=='POST':
        print(request.POST)
        return HttpResponse("VM created")
    else:
        return render(request,'forms/new_vm_form.html')

