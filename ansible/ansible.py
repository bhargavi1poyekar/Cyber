from ansible_runner import run

inventory_path="/home/bhargavi/Cyber/ansible/playbooks/inventory"
become_password='adminpass'

def install_packages(input_file, host_name):  

    playbook_path='/home/bhargavi/Cyber/ansible/playbooks/install_package.yml'

    extra_vars={
        'host_name':host_name,
        'csv_file_path':input_file
    }
    
    ansible_run(playbook_path,extra_vars)

def user_add(input_file, host_name):
    playbook_path='/home/bhargavi/Cyber/ansible/playbooks/userremove.yml'

    extra_vars={
        'host_name':host_name,
        'csv_file_path':input_file
    }
    
    ansible_run(playbook_path,extra_vars)

def user_remove(input_file, host_name):
    playbook_path='/home/bhargavi/Cyber/ansible/playbooks/userremove.yml'

    extra_vars={
        'host_name':host_name,
        'csv_file_path':input_file
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


def ansible_run(playbook_path,extra_vars):

    options={
        'inventory':inventory_path,
        'envvars':{'ANSIBLE_SUDO_PASS':become_password},
        'extravars':extra_vars
    }

    run(playbook=playbook_path, **options)

host_name='vmservers'
install_file='/home/bhargavi/Cyber/ansible/csv_files/packages.csv'
user_file='/home/bhargavi/Cyber/ansible/csv_files/users.csv'
remove_file='/home/bhargavi/Cyber/ansible/csv_files/users_remove.csv'
dir_file='/home/bhargavi/Cyber/ansible/csv_files/dir.csv'
cmd_file='/home/bhargavi/Cyber/ansible/csv_files/cmd.csv'
copy_file='/home/bhargavi/Cyber/ansible/csv_files/copy.csv'
install_packages(install_file,host_name)
# user_add(user_file,host_name)
# user_remove(remove_file,host_name)
# restart(host_name)
# create_dir(dir_file,host_name)
# delete_dir(dir_file,host_name)
# run_cmds(cmd_file,host_name)
# copy_files(copy_file,host_name)
# ufw_ssh('ub-20')
