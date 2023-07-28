from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.template import loader
from django.shortcuts import redirect, get_object_or_404
from django.templatetags.static import static
from django.conf import settings
import os
from ansible_runner import run
import json
import pandas as pd
import random
from django.contrib.auth.decorators import login_required
from .models import Exercise
# Create your views here.

IP_NAME={
        '130.85.121.26':'bhar-ub22',
        '130.85.121.27':'bhar-kali',
        '133.228.78.3':'bhar-ub20',
    }
VM_TEMPLATES={
   'kali':'CyberRange/vm/CRCSEE/Template/Template-Kali-crg',
   'ub20':'CyberRange/vm/CRCSEE/Template/template-ub20',
   'ub22':'CyberRange/vm/CRCSEE/Template/Temp-ub22',
}

become_password='Crcsee2#'
static=settings.STATIC_ROOT
inventory_path=static+'/forms/playbooks/inventory'

def dashboard(request):
    exercises=Exercise.objects.all()
    return render(request,'forms/main.html',{'exercises':exercises})

@login_required
def launch_vm_request(request):
    return render(request,'forms/vm_request.html')

@login_required
def new_vm(request):
    if request.method=='POST':
        playbook_path=static+'/forms/playbooks/deploy_template.yml'
        course_number=request.POST['course_number']
        prof_name=request.POST['instructor_name']
        os=request.POST['os']
        num_vm=request.POST['num_vm']
        
        folder_name=course_number+prof_name.split(' ')[0]
        vm_name=course_number+prof_name.split(' ')[0]+'-'+os
        template=VM_TEMPLATES[os]

        extra_vars={
            'create_folder_name':folder_name,
            'create_vm_name':vm_name,
            'create_template':template,
            'num_vm':int(num_vm)
        }
        options={
            'extravars':extra_vars
        }
        run(playbook=playbook_path,**options)
        
        # return redirect('dashboard')
        return JsonResponse({'message':"VM's created"})
        
    else:
        return render(request,'forms/new_vm_form.html')

@login_required
def power_on(request):
    
    if request.method=='POST':
        
        playbook_path=static+'/forms/playbooks/power_server.yml'
        ip_addr=[IP_NAME[ip.strip()] for ip in request.POST['ip_addr'].split(',')]
        machine_list=json.dumps(ip_addr)
        
        extra_vars={
            'machine_list':machine_list
        }
        options={
            'envvars':{
                'ANSIBLE_SUDO_PASS':become_password,
            },
            'extravars':extra_vars
        }
        run(playbook=playbook_path,**options)
        # return redirect('dashboard')
        #return HttpResponse("Powered on")
        return JsonResponse({'message':"Powered on"})
    else:
        return render(request,'forms/power_on.html')

@login_required
def power_off(request):
    if request.method=='POST':
        ip_addr=[IP_NAME[ip.strip()] for ip in request.POST['ip_addr'].split(',')]
        machine_list=json.dumps(ip_addr)
        playbook_path=static+'/forms/playbooks/power_off.yml'
        extra_vars={
            'machine_list':machine_list
        }
        options={
            'envvars':{
                'ANSIBLE_SUDO_PASS':become_password,
            },
            'extravars':extra_vars
        }
        run(playbook=playbook_path,**options)
        return JsonResponse({'message':"Powered off"})
        # return redirect('dashboard')
        #return HttpResponse("Powered off")
    else:
        return render(request,'forms/power_off.html')

@login_required
def restart(request):
    if request.method=='POST':
        ip_addr=[IP_NAME[ip.strip()] for ip in request.POST['ip_addr'].split(',')]
        machine_list=json.dumps(ip_addr)
        playbook_path=static+'/forms/playbooks/restart.yml'
        extra_vars={
            'machine_list':machine_list
        }
        options={
            'envvars':{
                'ANSIBLE_SUDO_PASS':become_password,
            },
            'extravars':extra_vars
        }
        run(playbook=playbook_path,**options)
        return JsonResponse({'message':"Restarted"})
        # return redirect('dashboard')
        #return HttpResponse("Restarted")
    else:
        return render(request,'forms/restart.html')

@login_required
def user_add(request):
    if request.method=='POST':
        ip_addr=[ip.strip() for ip in request.POST['ip_addr'].split(',')]
        add_host_name=['crange1@'+ip for ip in ip_addr]
        
        if request.POST['users']!='':
            add_users=request.POST['users'].split('\r\n')
            add_users_list=json.dumps(add_users)
        if request.FILES:
            add_file=request.FILES['user_add_file'].read()
            add_file=add_file.decode('utf-8')
            add_users=list(filter(None,add_file.split('\n')))
            add_users_list=json.dumps(add_users)


        playbook_path=static+'/forms/playbooks/user_add.yml'
        extra_vars={
            'host_name':add_host_name,
            'add_users_list':add_users_list
        }
        ansible_run(playbook_path,extra_vars)


        # return redirect('dashboard')
        return JsonResponse({'message':"users added"})

    else:
        return render(request,'forms/user_add.html')

@login_required
def user_remove(request):
    if request.method=='POST':
        ip_addr=[ip.strip() for ip in request.POST['ip_addr'].split(',')]
        remove_host_name=['crange1@'+ip for ip in ip_addr]
        remove_users=request.POST['users'].split(',')
        remove_users_list=json.dumps(remove_users)
        playbook_path=static+'/forms/playbooks/user_remove.yml'
        extra_vars={
            'host_name':remove_host_name,
            'remove_users_list':remove_users_list
        }
        ansible_run(playbook_path,extra_vars)
        return JsonResponse({'message':"Users Removed"})
        # return redirect('dashboard')
        #return HttpResponse("users removed")
    else:
        return render(request,'forms/user_remove.html')

@login_required
def create_dir(request):
    if request.method=='POST':
        ip_addr=[ip.strip() for ip in request.POST['ip_addr'].split(',')]
        create_host_name=['crange1@'+ip for ip in ip_addr]
        create_path=request.POST['dir_path'].split('\r\n')
        create_dir_list=json.dumps(create_path)
        playbook_path=static+'/forms/playbooks/create_directory.yml'
        extra_vars={
            'host_name':create_host_name,
            'create_dir_list':create_dir_list
        }
        ansible_run(playbook_path,extra_vars)
        return JsonResponse({'message':"Directory Created"})
        #return HttpResponse("Create Directory")
    else:
        return render(request,'forms/create_dir.html')

@login_required
def delete_dir(request):
    if request.method=='POST':
        ip_addr=[ip.strip() for ip in request.POST['ip_addr'].split(',')]
        delete_host_name=['crange1@'+ip for ip in ip_addr]
        delete_path=request.POST['dir_path'].split(',')
        delete_dir_list=json.dumps(delete_path)
        playbook_path=static+'/forms/playbooks/del_dir.yml'
        extra_vars={
            'host_name':delete_host_name,
            'delete_dir_list':delete_dir_list
        }
        ansible_run(playbook_path,extra_vars)
        # return redirect('dashboard')
        return JsonResponse({'message':"Directories deleted"})
        #return HttpResponse("Delete Directory")
    else:
        return render(request,'forms/delete_dir.html')

def ansible_run(playbook_path,extra_vars):
    options={
        'inventory':inventory_path,
        'envvars':{'ANSIBLE_SUDO_PASS':become_password},
        'extravars':extra_vars
    }

    run(playbook=playbook_path,**options)

@login_required
def open_pdf(request,exercise_id):
    exercise=get_object_or_404(Exercise,id=exercise_id)
    with open(exercise.pdf_file.path,'rb') as pdf_file:
        response=HttpResponse(pdf_file.read(),content_type='application/pdf')
        response['Content-Disposition']=f'inline; filename="{exercise.pdf_file.name}"'
        return response




