'''
Rotation Cipher: Rotate the characters by the given rotation key. 
'''

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

inputfile="Rotate-Plain.txt"
outputfile = opath + "Cipher".join(inputfile.split("-Plain"))
ciphertexts=[]

create_output_folder('key')

plainu = [ chr(letter) for letter in range(65, 65+26)] # Uppercase Letters
plainl = [ chr(letter) for letter in range(97, 97+26)] # Lowercase Letters
plainm = [' ', '.'] 

# Combine upper, lower and symbols
plain = plainu + plainl + plainm

for i in range(len(plaintexts)):
    
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
