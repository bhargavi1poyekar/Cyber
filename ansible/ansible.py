from ansible_runner import run

inventory_path="/home/bhargavi/cyber/ansible/inventory"
become_password='adminpass'

def install_packages(input_file, host_name):  

    playbook_path='/home/bhargavi/cyber/ansible/install_package.yml'

    extra_vars={
        'host_name':host_name,
        'csv_file_path':input_file
    }
    
    ansible_run(playbook_path,extra_vars)

def user_add(input_file, host_name):
    playbook_path='/home/bhargavi/cyber/ansible/userremove.yml'

    extra_vars={
        'host_name':host_name,
        'csv_file_path':input_file
    }
    
    ansible_run(playbook_path,extra_vars)

def user_remove(input_file, host_name):
    playbook_path='/home/bhargavi/cyber/ansible/userremove.yml'

    extra_vars={
        'host_name':host_name,
        'csv_file_path':input_file
    }
    
    ansible_run(playbook_path,extra_vars)

def restart(hosts):

    playbook_path='/home/bhargavi/cyber/ansible/restart_server.yml'

    extra_vars={
        'host_name':host_name,
    }
    
    ansible_run(playbook_path,extra_vars)

def create_dir(input_file,hosts):
    playbook_path='/home/bhargavi/cyber/ansible/create_directory.yml'

    extra_vars={
        'host_name':host_name,
        'csv_file_path':input_file
    }
    
    ansible_run(playbook_path,extra_vars)

def delete_dir(input_file,hosts):
    playbook_path='/home/bhargavi/cyber/ansible/del_dir.yml'

    extra_vars={
        'host_name':host_name,
        'csv_file_path':input_file
    }
    
    ansible_run(playbook_path,extra_vars)

def run_cmds(input_file,hosts):
    playbook_path='/home/bhargavi/cyber/ansible/run_cmds.yml'

    extra_vars={
        'host_name':host_name,
        'csv_file_path':input_file
    }
    
    ansible_run(playbook_path,extra_vars)

def copy_files(input_file,hosts):
    playbook_path='/home/bhargavi/cyber/ansible/copy_files.yml'

    extra_vars={
        'host_name':host_name,
        'csv_file_path':input_file
    }
    
    ansible_run(playbook_path,extra_vars)

def ansible_run(playbook_path,extra_vars):

    options={
        'inventory':inventory_path,
        'envvars':{'ANSIBLE_SUDO_PASS':become_password},
        'extravars':extra_vars
    }

    run(playbook=playbook_path, **options)

host_name='all'
install_file='/home/bhargavi/cyber/ansible/packages.csv'
user_file='/home/bhargavi/cyber/ansible/users.csv'
remove_file='/home/bhargavi/cyber/ansible/users_remove.csv'
dir_file='/home/bhargavi/cyber/ansible/dir.csv'
cmd_file='/home/bhargavi/cyber/ansible/cmd.csv'
copy_file='/home/bhargavi/cyber/ansible/copy.csv'
# install_packages(install_file,host_name)
# user_add(user_file,host_name)
# user_remove(remove_file,host_name)
# restart(host_name)
# create_dir(dir_file,host_name)
# delete_dir(dir_file,host_name)
# run_cmds(cmd_file,host_name)
copy_files(copy_file,host_name)