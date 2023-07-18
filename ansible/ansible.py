from ansible_runner import run
import pandas as pd
import json
import numpy as np
import math

inventory_path="/home/bhargavi/Cyber/ansible/playbooks/inventory"
become_password='Crcsee2#'

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

def restart(host_name):

    playbook_path='/home/bhargavi/Cyber/ansible/playbooks/restart_server.yml'

    extra_vars={
        'host_name':host_name,
    }
    
    ansible_run(playbook_path,extra_vars)

def create_dir(input_file,host_name):
    playbook_path='/home/bhargavi/Cyber/ansible/playbooks/create_directory.yml'

    extra_vars={
        'host_name':host_name,
        'csv_file_path':input_file
    }
    
    ansible_run(playbook_path,extra_vars)

def delete_dir(input_file,host_name):
    playbook_path='/home/bhargavi/Cyber/ansible/playbooks/del_dir.yml'

    extra_vars={
        'host_name':host_name,
        'csv_file_path':input_file
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

def xrdp_install(host_name):
    playbook_path='/home/bhargavi/Cyber/ansible/playbooks/xrdp.yml'

    extra_vars={
        'host_name':host_name,
    }
    
    ansible_run(playbook_path,extra_vars)


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
user_csv_process('Users.csv')
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




    



    