from ansible_runner import run
import pandas as pd
import json
import numpy as np
import math
import os, sys, random

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
        'envvars':{
             'ANSIBLE_SUDO_PASS':become_password,
             
        },
        'extravars':extra_vars
    }
    run(playbook=playbook_path, **options)
   
def power_on(machine_list):
    playbook_path='/home/bhargavi/Cyber/ansible/playbooks/power_server.yml'
    extra_vars={
	'machine_list':machine_list
    }
    
    options={
        'envvars':{
             'ANSIBLE_SUDO_PASS':become_password,
             
        },
        'extravars':extra_vars
    }
    run(playbook=playbook_path, **options)
    
def restart(machine_list):

    playbook_path='/home/bhargavi/Cyber/ansible/playbooks/restart.yml'
    extra_vars={
	'machine_list':machine_list
    }
    
    options={
        
        'envvars':{
             'ANSIBLE_SUDO_PASS':become_password,
             
        },
        'extravars':extra_vars
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
        'copy_csv_list':input_file
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
        'envvars':{
             'ANSIBLE_SUDO_PASS':become_password,
        
        },
        'extravars':extra_vars
    }

    run(playbook=playbook_path, **options)



def ceaser(opath,plaintexts):

    Cipherpaths=[]
    inputfile="Ceaser-Plain.txt"
    outputfile = opath + "Cipher".join(inputfile.split("-Plain"))

    plainu = [ chr(letter) for letter in range(65, 65+26)] # Uppercase Letters
    plainl = [ chr(letter) for letter in range(97, 97+26)] # Lowercase Letters
    plainm = [' ', '.'] 
    

    # Combine upper, lower and symbols
    plain = plainu + plainl + plainm
   

    for i in range(len(plaintexts)):

        cipheru = [ chr(letter) for letter in range(65, 65+26)] 
        cipherl = [ chr(letter) for letter in range(97, 97+26)]
        cipherm = ['@', '_']

        # Shuffle cipher chars randomly
        random.shuffle(cipheru)
        random.shuffle(cipherl)
        random.shuffle(cipherm)

        cipher = cipheru + cipherl + cipherm
        
        ciphertext=[]
        keycount = dict()
        for ch in plaintexts[i]: # For every character in plaintext
            if ch in plain: # If it is in plain
                index = plain.index(ch) # Get index of the plain
                ciphertext.append(cipher[index]) # append the cipher at that index in cipher

                # To keep frequency count
                if ch not in plainm: # If ch is a letter (and not symbol)
                    val = keycount.get(ch,0) # Get Value(count) of char, return 0 if char not in keycount
                    keycount[ch] = val + 1 # Increment the count 
            else:
                ciphertext.append(ch) # If plaintext is not a upper, lower, space and dot, dont replace

        if i<9:output=('0'+str(i+1)+'.').join(outputfile.split('.'))
        else: output=(str(i+1)+'.').join(outputfile.split('.'))
        
        Cipherpaths.append(output)
        ofile = open(output,"w") # Open the file in writing mode
        ofile.write(''.join(ciphertext)) # Write the ciphertext in output file

        # write key for a character with max occurrence.
        ofile.write("\n")
        ofile.write("Key mapping (ciphertext->plaintext) for max occurring character\n")
        keyalpha = max(keycount, key=keycount.get) # Get character with max freq
        ofile.write(cipher[plain.index(keyalpha)] + " -> " + keyalpha + "\n") 
        ofile.close()

        keyfilepath='key/'+inputfile
        if i<9:keyfilename=('0'+str(i+1)+'_key.').join(keyfilepath.split('.'))
        else: keyfilename=(str(i+1)+'_key.').join(keyfilepath.split('.'))

        keyfile = open(keyfilename, "w")
        keyfile.write(''.join(plain) +"\n")
        keyfile.write(''.join(cipher) + "\n")

        keyfile.write('\nPlaintext: '+ plaintexts[i] + "\n")
        keyfile.write('\nCiphertext: '+ ''.join(ciphertext) + "\n")
        keyfile.close()
    return Cipherpaths

def rotation(opath,plaintexts,plain,key):

    Cipherpaths=[]
    inputfile="Rotate-Plain.txt"
    outputfile = opath + "Cipher".join(inputfile.split("-Plain"))

    for i in range(len(plaintexts)):
        
        if key!='random':
            rot_key=int(key)
        else:
            rot_key = random.choice([num for num in range(1, 101) if num % 26 != 0])

        cipheru = [ chr(((letter-65+rot_key) % 26)+65) for letter in range(65, 65+26)] 
        # Rotate each letter by key
        cipherl = [ chr(((letter-97+rot_key) % 26)+97) for letter in range(97, 97+26)]
        cipherm = ['@', '_']

        cipher = cipheru + cipherl + cipherm
        ciphertext = [] # List for cipertext

        for ch in plaintexts[i]: # For every character in plaintext
            if ch in plain: # If it is in plain
                index = plain.index(ch) # Get index of the plain
                ciphertext.append(cipher[index]) # append the cipher at that index in cipher

            else:
                ciphertext.append(ch) # If plaintext is not a upper, lower, space and dot, dont replace
        
        if i<9:output=('0'+str(i+1)+'.').join(outputfile.split('.'))
        else: output=(str(i+1)+'.').join(outputfile.split('.'))
        
        ofile = open(output,"w") # Open the file in writing mode
        ofile.write(''.join(ciphertext)) # Write the ciphertext in output file
        ofile.close()
        Cipherpaths.append(output)
        keyfilepath='key/'+inputfile
        if i<9:keyfilename=('0'+str(i+1)+'_key.').join(keyfilepath.split('.'))
        else: keyfilename=(str(i+1)+'_key.').join(keyfilepath.split('.'))

        keyfile = open(keyfilename, "w")
        keyfile.write(''.join(plain) +"\n")
        keyfile.write(''.join(cipher) + "\n")

        keyfile.write('\nPlaintext: '+ plaintexts[i] + "\n")
        keyfile.write('\nCiphertext: '+ ''.join(ciphertext) + "\n")
        keyfile.write('\nKey: '+ str(rot_key) + "\n")
        keyfile.close()
    return Cipherpaths

def vernam(opath,plaintexts):
    Cipherpaths=[]
    inputfile="Vernam-Plain.txt"
    outputfile = opath + "Cipher".join(inputfile.split("-Plain"))

    cipherm = ['@', '_']

    plainu = [ chr(letter) for letter in range(65, 65+26)] # Uppercase Letters
    plainl = [ chr(letter) for letter in range(97, 97+26)] # Lowercase Letters
    plainm = [' ', '.'] 
    

    # Combine upper, lower and symbols
    plain = plainu + plainl + plainm

    
    for i in range(len(plaintexts)):

        keytext=""
        for _ in range(len(plaintexts[i])):
            random_char = chr(random.randint(65, 90))
            keytext += random_char

        ciphertext = [] # List for cipertext

        for idx in range(len(plaintexts[i])): # For every character in plaintext
            
            if plaintexts[i][idx] in plainu: # If it is in plain
                rot_key=ord(keytext[idx])-ord('A')
                subs=chr(((ord(plaintexts[i][idx])-65^rot_key) % 26)+65)
                ciphertext.append(subs)
            elif plaintexts[i][idx] in plainl:
                rot_key=ord(keytext[idx])-ord('A')
                subs=chr(((ord(plaintexts[i][idx])-97^rot_key) % 26)+97)
                ciphertext.append(subs)
            elif plaintexts[i][idx] in plainm:
                index = plainm.index(plaintexts[i][idx]) # Get index of the plain
                ciphertext.append(cipherm[index])
            else:
                ciphertext.append(plaintexts[i][idx]) 
                # If plaintext is not a upper, lower, space and dot, dont replace

        if i<9:output=('0'+str(i+1)+'.').join(outputfile.split('.'))
        else: output=(str(i+1)+'.').join(outputfile.split('.'))
        Cipherpaths.append(output)
        ofile = open(output,"w") # Open the file in writing mode
        ofile.write(''.join(ciphertext)) # Write the ciphertext in output file
        ofile.close()

        keyfilepath='key/'+inputfile
        if i<9:keyfilename=('0'+str(i+1)+'_key.').join(keyfilepath.split('.'))
        else: keyfilename=(str(i+1)+'_key.').join(keyfilepath.split('.'))
        
        keyfile = open(keyfilename, "w")
        keyfile.write('Plaintext: '+ plaintexts[i] + "\n")
        keyfile.write('\nCiphertext: '+ ''.join(ciphertext) + "\n")
        keyfile.write('\nKey: '+ keytext + "\n")
        keyfile.close()
    return Cipherpaths

def vigenere(opath, plaintexts,key):

    Cipherpaths=[]
    plainu = [ chr(letter) for letter in range(65, 65+26)] # Uppercase Letters
    plainl = [ chr(letter) for letter in range(97, 97+26)] # Lowercase Letters
    plainm = [' ', '.'] 

    cipherm = ['@', '_']

    inputfile="Vigenere-Plain.txt"
    outputfile = opath + "Cipher".join(inputfile.split("-Plain"))
    for i in range(len(plaintexts)):

        keytext=""
        for _ in range(10):
            random_char = chr(random.randint(65, 90))
            keytext += random_char

        ciphertext = [] # List for cipertext

        for idx in range(len(plaintexts[i])): # For every character in plaintext
            
            if plaintexts[i][idx] in plainu: # If it is in plain
                rot_key=ord(keytext[idx%len(keytext)])-ord('A')
                subs=chr(((ord(plaintexts[i][idx])-65+rot_key) % 26)+65)
                ciphertext.append(subs)
            elif plaintexts[i][idx] in plainl:
                rot_key=ord(keytext[idx%len(keytext)])-ord('A')
                subs=chr(((ord(plaintexts[i][idx])-97+rot_key) % 26)+97)
                ciphertext.append(subs)
            elif plaintexts[i][idx] in plainm:
                index = plainm.index(plaintexts[i][idx]) # Get index of the plain
                ciphertext.append(cipherm[index])
            else:
                ciphertext.append(plaintexts[i][idx]) # If plaintext is not a upper, lower, space and dot, dont replace
        
        if i<9:output=('0'+str(i+1)+'.').join(outputfile.split('.'))
        else: output=(str(i+1)+'.').join(outputfile.split('.'))
        
        Cipherpaths.append(output)
        ofile = open(output,"w") # Open the file in writing mode
        ofile.write(''.join(ciphertext)) # Write the ciphertext in output file
        ofile.close()

        keyfilepath='key/'+inputfile
        if i<9:keyfilename=('0'+str(i+1)+'_key.').join(keyfilepath.split('.'))
        else: keyfilename=(str(i+1)+'_key.').join(keyfilepath.split('.'))
        
        keyfile = open(keyfilename, "w")
        keyfile.write('Plaintext: '+ plaintexts[i] + "\n")
        keyfile.write('\nCiphertext: '+ ''.join(ciphertext) + "\n")
        keyfile.write('\nKey: '+ keytext + "\n")
        keyfile.close()
    return Cipherpaths


def transposition(opath,plaintexts,key):

    Cipherpaths=[]
    inputfile="Transpose-Plain.txt"
    outputfile = opath + "Cipher".join(inputfile.split("-Plain"))

    for idx in range(len(plaintexts)):

        ciphertext = [] # List for ciphertext

        plain=plaintexts[idx].replace(" ","@")
        plain=plain.replace(".","_")

        if key!='random':
            keytext=key
        else:    
            key_length=random.randint(10,20)
        
            keytext=""

            for _ in range(key_length):
                random_char = chr(random.randint(65, 90))
                keytext += random_char

        l_key = list(keytext) # list of key characters 
        s_key = sorted(l_key) # sorted key 

        plain_list = list(plain) # list of plain cipher text characters 

        # # Encryption 

        rem = len(plaintexts[idx]) % len(keytext) 
        emp = len(keytext)-rem # Finding empty characters at the end in matrix 
        
        for i in range(emp): 
            plain_list.append('@') # replacing empty space at the end with @

        matrix = [[] for j in range(len(keytext))] 
        cipher = [] 

        for i in range(len(matrix)): 
            for j in range(i, len(plain_list), len(keytext)): 
                matrix[i].append(plain_list[j])

        mat_t=list(map(list, zip(*matrix)))

        # Rearranging matrix according to the key 
        for i in range(len(keytext)): 
            cipher.append(matrix[l_key.index(s_key[i])]) 

        cip_t=list(map(list, zip(*cipher)))

        # Converting matrix to list 
        for i in range(len(keytext)): 
            cipher[i] = ''.join(cipher[i]) 

        # Converting list to string 
        ciphertext = ''.join(cipher) 

        if idx<9:output=('0'+str(idx+1)+'.').join(outputfile.split('.'))
        else: output=(str(idx+1)+'.').join(outputfile.split('.'))
        
        Cipherpaths.append(output)
        ofile = open(output,"w") # Open the file in writing mode
        ofile.write(''.join(ciphertext)) # Write the ciphertext in output file
        ofile.close()

        keyfilepath='key/'+inputfile
        if idx<9:keyfilename=('0'+str(idx+1)+'_key.').join(keyfilepath.split('.'))
        else: keyfilename=(str(idx+1)+'_key.').join(keyfilepath.split('.'))
        
        keyfile = open(keyfilename, "w")
        keyfile.write('Plaintext: '+ plaintexts[idx] + "\n")
        keyfile.write('\nCiphertext: '+ ''.join(ciphertext) + "\n")
        keyfile.write('\nKey: '+ keytext + "\n")
        keyfile.close()
    return Cipherpaths


def get_plaintexts_from_file(file_path,num):
    with open(file_path, "r") as file:
        text = file.read()
        file.close()
    plaintexts = text.split("\n\n")
    if num!='':
        return plaintexts[:int(num)]
    else:
        return plaintexts
        
def create_output_folder(output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        return 
    else:
        print("Output folder already exists.")

def cryptography(input_file):

    output_folder = "ciphertext"
    create_output_folder(output_folder)

    opath=output_folder+'/'
    create_output_folder('key')

    plainu = [ chr(letter) for letter in range(65, 65+26)] # Uppercase Letters
    plainl = [ chr(letter) for letter in range(97, 97+26)] # Lowercase Letters
    plainm = [' ', '.'] 

    cipherm = ['@', '_']

    # Combine upper, lower and symbols
    plain = plainu + plainl + plainm

    df_crypt=pd.read_csv(input_file)
    df_crypt=df_crypt.fillna('')
    
    for index,row in df_crypt.iterrows():
        if row[3]=='Yes':
            key='random'
        else:
            key=row[4]
            print(key)

        if row[5]=='':
            file_path = "default_Plain.txt"
            try:
                # Get the paragraphs from the default file path
                plaintexts = get_plaintexts_from_file(file_path,row[6])

            except FileNotFoundError:
                print("Default file not found.")
                exit(1)

        else:
            plaintexts=[r for r in row[5].split('\n\n')]

        if row[2]=='Ceasar Cipher':
            Cipherpaths=ceaser(opath,plaintexts)
        elif row[2]=='Rotation Cipher':
            Cipherpaths=rotation(opath,plaintexts,plain,key)
        elif row[2]=='Transposition Cipher':
            Cipherpaths=transposition(opath,plaintexts,key)
        elif row[2]=='Vernam Cipher':
            Cipherpaths=vernam(opath,plaintexts)
        elif row[2]=="Vigenere":
            Cipherpaths=vigenere(opath,plaintexts,key)
        
        if row[7]!='':
            host_name=[f'crange1@{r}' for r in row[7].split(',')]
            
            create_dir_list=json.dumps(['/Cryptography'])
            copy_csv=[]
            
            for i in range(len(Cipherpaths)):
                copy_csv.append(host_name[i]+','+'../'+Cipherpaths[i]+',/Cryptography/ciphertext.txt')
            
            copy_csv_list=json.dumps(copy_csv)
            copy_files(copy_csv_list,host_name)
            create_dir(create_dir_list,host_name)


host_name='vmservers'
# install_file='/home/bhargavi/Cyber/ansible/csv_files/packages.csv'
# user_file='/home/bhargavi/Cyber/ansible/csv_files/users.csv'
# remove_file='/home/bhargavi/Cyber/ansible/csv_files/users_remove.csv'
# dir_file='/home/bhargavi/Cyber/ansible/csv_files/dir.csv'
# cmd_file='/home/bhargavi/Cyber/ansible/csv_files/cmd.csv'
# copy_file='/home/bhargavi/Cyber/ansible/csv_files/copy.csv'
# install_packages(install_file,host_name)






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

class Switcher(object): 
    def indirect(self, i): 
        # to call the required method of cryptography 
        method_name = 'choice_'+str(i) 
        method = getattr(self, method_name, lambda: print('Invalid option')) 
        return method() 
    
    def choice_1(self): 
        power_csv_process('Power.csv')

    def choice_2(self):
        user_csv_process('Users.csv')

    def choice_3(self):
        deploy_template_csv('VM.csv')
    
    def choice_4(self):
        dir_csv_process('Dir.csv') 
    
    def choice_5(self):
        cryptography('Crypt.csv')


s = Switcher() # Creating object of Switcher Class 
ch = int(input("Select the task you want to perform:\n1. Power on/off/Restart\n2. User add/remove\n3. Create VM\n4. Create/Delete Directory\n5. Cryptography Excercise\n")) 
s.indirect(ch) 



    



    
