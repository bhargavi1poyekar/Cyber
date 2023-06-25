# generate cipher text and transformation keys as per Ceasers Cipher.

'''
Vernam Cipher: Given a key, find the ascii value of the key and xor the chars of plaintext
by values of key  
'''

import os, sys, random

plainu = [ chr(letter) for letter in range(65, 65+26)] # Uppercase Letters
plainl = [ chr(letter) for letter in range(97, 97+26)] # Lowercase Letters
plainm = [' ', '.'] 

cipherm = ['@', '_']

# Combine upper, lower and symbols
plain = plainu + plainl + plainm

# First argument-> inputpath of plaintext
inputfile = sys.argv[1]

# Second argument-> output folder path
opath = sys.argv[2]

# Check if the paths are valid
if not os.path.isfile(inputfile):
    print("input file " + inputfile + ", not found")
    exit()
if not os.path.isdir(opath):
    print("Output file " + opath + ", not found")
    exit()


# Input File 
infile = open(inputfile)

# Output file name -> Split input file (Ceaser-Plain-01.txt) on Plain -> so we get [Ceaser, 01] 
# and join them with Cipher-> opath/CeaserCipher01.txt
outputfile = opath + "Cipher".join(inputfile.split("/")[-1].split("-Plain-"))

# Read the input file
plaintext = infile.read()
infile.close()

keytext=""
for _ in range(len(plaintext)):
    random_char = chr(random.randint(65, 90))
    keytext += random_char


ciphertext = [] # List for cipertext
keycount = dict()


for idx in range(len(plaintext)): # For every character in plaintext
    
    if plaintext[idx] in plainu: # If it is in plain
        rot_key=ord(keytext[idx])-ord('A')
        subs=chr(((ord(plaintext[idx])-65^rot_key) % 26)+65)
        ciphertext.append(subs)
    elif plaintext[idx] in plainl:
        rot_key=ord(keytext[idx])-ord('A')
        subs=chr(((ord(plaintext[idx])-97^rot_key) % 26)+97)
        ciphertext.append(subs)
    elif plaintext[idx] in plainm:
        index = plainm.index(plaintext[idx]) # Get index of the plain
        ciphertext.append(cipherm[index])
    else:
        ciphertext.append(plaintext[idx]) # If plaintext is not a upper, lower, space and dot, dont replace
    
    # To keep frequency count
    if plaintext[idx] not in plainm: # If ch is a letter (and not symbol)
        val = keycount.get(plaintext[idx],0) # Get Value(count) of char, return 0 if char not in keycount
        keycount[plaintext[idx]] = val + 1 # Increment the count 

ofile = open(outputfile,"w") # Open the file in writing mode
ofile.write(''.join(ciphertext)) # Write the ciphertext in output file

keyfilename = ".".join(inputfile.split(".")[:-1])+".key"
keyfile = open(keyfilename, "w")
keyfile.write(''.join(plaintext) +"\n")
keyfile.write(''.join(ciphertext) + "\n")
keyfile.write('Key: '+ str(keytext) + "\n")
keyfile.close()

