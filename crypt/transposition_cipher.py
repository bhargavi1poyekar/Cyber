import os, sys, random

import argparse

def get_plaintexts_from_file(file_path):
    with open(file_path, "r") as file:
        text = file.read()
        file.close()
    plaintexts = text.split("\n\n")
    return plaintexts

def create_output_folder(output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        return 
    else:
        print("Output folder already exists.")

# Create an ArgumentParser object
parser = argparse.ArgumentParser()

# Add the file path argument with a flag
parser.add_argument("-i", "--ifile", help="Input File of Plaintexts")
parser.add_argument("-o", "--ofolder", help="Folder for Ciphertext output")

# Parse the command-line arguments
args = parser.parse_args()

if args.ifile:
    file_path = args.ifile
    try:
        # Get the paragraphs from the provided file path
        plaintexts = get_plaintexts_from_file(file_path)
    except FileNotFoundError:
        print("File not found.")
        exit(1)
else:
    # Use a default text file
    file_path = "default_Plain.txt"
    
    try:
        # Get the paragraphs from the default file path
        plaintexts = get_plaintexts_from_file(file_path)
    
    except FileNotFoundError:
        print("Default file not found.")
        exit(1)


if args.ofolder:
    output_folder = args.ofolder
    if not os.path.isdir(output_folder):
        # Create the specified output folder
        create_output_folder(output_folder)
else:
    # Use a default output folder named "Cipher"
    output_folder = "ciphertext"
    create_output_folder(output_folder)

opath=output_folder+'/'

inputfile="Transpose-Plain.txt"
outputfile = opath + "Cipher".join(inputfile.split("-Plain"))
ciphertexts=[]

create_output_folder('key')

for idx in range(len(plaintexts)):

    ciphertext = [] # List for ciphertext

    plain=plaintexts[idx].replace(" ","@")
    plain=plain.replace(".","_")

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

    if i<9:output=('0'+str(idx+1)+'.').join(outputfile.split('.'))
    else: output=(str(idx+1)+'.').join(outputfile.split('.'))
    
    ofile = open(output,"w") # Open the file in writing mode
    ofile.write(''.join(ciphertext)) # Write the ciphertext in output file
    ofile.close()

    keyfilepath='key/'+inputfile
    if i<9:keyfilename=('0'+str(idx+1)+'_key.').join(keyfilepath.split('.'))
    else: keyfilename=(str(idx+1)+'.').join(keyfilepath.split('.'))
    
    keyfile = open(keyfilename, "w")
    keyfile.write('Plaintext: '+ plaintexts[idx] + "\n")
    keyfile.write('\nCiphertext: '+ ''.join(ciphertext) + "\n")
    keyfile.write('\nKey: '+ keytext + "\n")
    keyfile.close()






