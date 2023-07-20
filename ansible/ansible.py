from ansible_runner import run
import pandas as pd
import json
import numpy as np
import math

inventory_path="/home/bhargavi/Cyber/ansible/playbooks/inventory"
become_password='Crcsee2#'

IP_NAME={
   '130.85.121.26':'bhar-ub22',
   '130.85.121.27':'bhar-kali',
   '133.228.78.3':'bhar-ub20',
   '130.85.121.34':'testvm_ubuntu22'
}

VM_TEMPLATES={
   'Kali Linux':'CyberRange/vm/CRCSEE/Template/Template-Kali-crg',
   'Ubuntu 20':'CyberRange/vm/CRCSEE/Template/template-ub20',
   'Ubuntu 22':'CyberRange/vm/CRCSEE/Template/Temp-ub22',
}

VM_NAME={
   'Kali Linux':'Kali',
   'Ubuntu 20':'Ub20',
   'Ubuntu 22':'Ub22',
}

def install_packages(input_file, host_name):  

    playbook_path='/home/bhargavi/Cyber/ansible/playbooks/install_package.yml'

    extra_vars={
        'host_name':host_name,
        'csv_file_path':input_file
    }
    
    ansible_run(playbook_path,extra_vars)

def user_csv_process(input_file):

    df_users=pd.read_csv(input_file)
    df_users=df_users.fillna('')

    for index, row in df_users.iterrows():
        if row[2].lower()=='yes':
            if row[3]!='':
                add_host_name=[r.strip() for r in row[3].split(',')] 
                remove_host_name=[r.strip() for r in row[3].split(',')] 
            else:
                add_host_name=[r.strip() for r in row[5].split(',')]
                remove_host_name=[r.strip() for r in row[5].split(',')]
        else:
            add_host_name=[r.strip() for r in row[3].split(',')] 
            remove_host_name=[r.strip() for r in row[5].split(',')]

        if row[4]!='':
            add_host_name=['crange1@'+ip for ip in add_host_name]
            add_users=row[4].split('\n')
            add_users_list=json.dumps(add_users)
            user_add(add_users_list,add_host_name)


        if row[6]!='':
            remove_users=row[6].split('\n')
            remove_users_list=json.dumps(remove_users)
            remove_host_name=['crange1@'+ip for ip in remove_host_name]
            user_remove(remove_users_list,remove_host_name)

def user_add(add_users_list, add_host_name):

    playbook_path='/home/bhargavi/Cyber/ansible/playbooks/user_add.yml'

    extra_vars={
        'host_name':add_host_name,
        'add_users_list':add_users_list
    }

    ansible_run(playbook_path,extra_vars)

def user_remove(remove_users_list, remove_host_name):
    playbook_path='/home/bhargavi/Cyber/ansible/playbooks/user_remove.yml'

    extra_vars={
        'host_name':remove_host_name,
        'remove_users_list':remove_users_list
    }

    ansible_run(playbook_path,extra_vars)

def power_csv_process(input_file):

    df_machine=pd.read_csv(input_file)
    df_machine=df_machine.fillna('')

    for index,row in df_machine.iterrows():
        if row[3]!='':
	        restart_host_name=[IP_NAME[r.strip()] for r in row[3].split(',')] 
	        machine_list=json.dumps(restart_host_name)
	        restart(machine_list)
        if row[5]!='':
	        power_off_machine=[IP_NAME[r.strip()] for r in row[5].split(',')]
	        machine_list=json.dumps(power_off_machine)
	        power_off(machine_list) 
        if row[4]!='':
	        power_on_machine=[IP_NAME[r.strip()] for r in row[4].split(',')]
	        machine_list=json.dumps(power_on_machine)
	        power_on(machine_list)
        

def power_off(machine_list):
    playbook_path='/home/bhargavi/Cyber/ansible/playbooks/power_off.yml'
    extra_vars={
	'machine_list':machine_list
    }
    options={
	'extravars': extra_vars
    }
    run(playbook=playbook_path, **options)
   
def power_on(machine_list):
    playbook_path='/home/bhargavi/Cyber/ansible/playbooks/power_server.yml'
    extra_vars={
	'machine_list':machine_list
    }
    options={
	'extravars': extra_vars
    }
    run(playbook=playbook_path, **options)
    
def restart(machine_list):

    playbook_path='/home/bhargavi/Cyber/ansible/playbooks/restart.yml'
    extra_vars={
	'machine_list':machine_list
    }
    options={
	'extravars': extra_vars
    }
    run(playbook=playbook_path, **options)

def deploy_template_csv(input_file):
    df_vm=pd.read_csv(input_file)
    df_vm=df_vm.fillna('')
    playbook_path='/home/bhargavi/Cyber/ansible/playbooks/deploy_template.yml'
    for index,row in df_vm.iterrows():
        course_name=row[5]
        prof_name=row[6]
        os=row[9]
        num=row[16]
        folder_name=course_name+prof_name.split(' ')[0]
        vm_name=course_name+prof_name.split(' ')[0]+'-'+VM_NAME[os]
        template=VM_TEMPLATES[os]

        extra_vars={
            'create_folder_name':folder_name,
            'create_vm_name':vm_name,
	    'create_template':template,
            'num_vm':num
        }
        options={
	    'extravars': extra_vars
        }
        run(playbook=playbook_path, **options)

def dir_csv_process(input_file):

    df_dir=pd.read_csv(input_file)
    df_dir=df_dir.fillna('')

    for index, row in df_dir.iterrows():

        if row[4]=='Create Directory':
            create_host_name=[r.strip() for r in row[3].split(',')] 
            create_host_name=['crange1@'+ip for ip in create_host_name]
            create_path=[r.strip() for r in row[5].split(',')]
            dir_permission=[r.strip() for r in row[6].split(',')]
            create_dir_list=[]
            for path,perm in zip(create_path, dir_permission):
                if perm!='':
                    create_dir_list.append(f'{path},{perm}')
                else:
                    create_dir_list.append(f'{path},0755')

            create_dir_list=json.dumps(create_dir_list)
            create_dir(create_dir_list,create_host_name)

        elif row[4]=='Delete Directory':
            delete_host_name=[r.strip() for r in row[3].split(',')]
            delete_host_name=['crange1@'+ip for ip in delete_host_name]
            delete_path=[r.strip() for r in row[5].split(',')] 
            delete_dir_list=json.dumps(delete_path)
            delete_dir(delete_dir_list,delete_host_name)

def create_dir(create_dir_list,create_host_name):
    playbook_path='/home/bhargavi/Cyber/ansible/playbooks/create_directory.yml'

    extra_vars={
        'host_name':create_host_name,
        'create_dir_list':create_dir_list
    }
    ansible_run(playbook_path,extra_vars)

def delete_dir(delete_dir_list,delete_host_name):
    playbook_path='/home/bhargavi/Cyber/ansible/playbooks/del_dir.yml'

    extra_vars={
        'host_name':delete_host_name,
        'delete_dir_list':delete_dir_list
    }

    ansible_run(playbook_path,extra_vars)

def run_cmds(input_file,host_name):
    playbook_path='/home/bhargavi/Cyber/ansible/playbooks/run_cmds.yml'

    extra_vars={
        'host_name':host_name,
        'csv_file_path':input_file
    }

    ansible_run(playbook_path,extra_vars)

def copy_files(input_file,host_name):
    playbook_path='/home/bhargavi/Cyber/ansible/playbooks/copy_files.yml'

    extra_vars={
        'host_name':host_name,
        'csv_file_path':input_file
    }

    ansible_run(playbook_path,extra_vars)

def ufw_ssh(host_name):
    playbook_path='/home/bhargavi/Cyber/ansible/playbooks/ufw_ssh.yml'

    extra_vars={
        'host_name':host_name,
    }

    ansible_run(playbook_path,extra_vars)

def ufw_before_backup(host_name):
    playbook_path='/home/bhargavi/Cyber/ansible/playbooks/ufw_before.yml'

    extra_vars={
        'host_name':host_name,
    }

    ansible_run(playbook_path,extra_vars)

def ufw_reset(host_name):
    playbook_path='/home/bhargavi/Cyber/ansible/playbooks/ufw_reset.yml'

    extra_vars={
        'host_name':host_name,
    }

    ansible_run(playbook_path,extra_vars)

# def xrdp_install(host_name):
#     playbook_path='/home/bhargavi/Cyber/ansible/playbooks/xrdp.yml'

    # extra_vars={
    #     'host_name':host_name,
    # }


def ansible_run(playbook_path,extra_vars):

    options={
        'inventory':inventory_path,
        'envvars':{'ANSIBLE_SUDO_PASS':become_password},
        'extravars':extra_vars
    }

    run(playbook=playbook_path, **options)

host_name='vmservers'
# install_file='/home/bhargavi/Cyber/ansible/csv_files/packages.csv'
# user_file='/home/bhargavi/Cyber/ansible/csv_files/users.csv'
# remove_file='/home/bhargavi/Cyber/ansible/csv_files/users_remove.csv'
# dir_file='/home/bhargavi/Cyber/ansible/csv_files/dir.csv'
# cmd_file='/home/bhargavi/Cyber/ansible/csv_files/cmd.csv'
# copy_file='/home/bhargavi/Cyber/ansible/csv_files/copy.csv'
# install_packages(install_file,host_name)

# user_csv_process('Users.csv')
# dir_csv_process('Dir.csv') 
power_csv_process('Power.csv')
# deploy_template_csv('VM.csv')

# user_remove(remove_file,host_name)
# restart(host_name)
# create_dir(dir_file,host_name)
# delete_dir(dir_file,host_name)
# run_cmds(cmd_file,host_name)
# copy_files(copy_file,host_name)
# ufw_ssh('ub20')
# ufw_before_backup('ub20')
# ufw_reset('ub20')
# xrdp_install('ub20')




    



    
