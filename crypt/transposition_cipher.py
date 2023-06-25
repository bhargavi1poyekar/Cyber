# generate cipher text and transformation keys as per Ceasers Cipher.

import os, sys, random


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

ciphertext = [] # List for cipertext


plain=plaintext.replace(" ","@")
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

rem = len(plaintext) % len(keytext) 
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

ofile = open(outputfile,"w") # Open the file in writing mode
ofile.write(''.join(ciphertext)) # Write the ciphertext in output file
ofile.close()


keyfilename = ".".join(inputfile.split(".")[:-1])+".key"
keyfile = open(keyfilename, "w")
keyfile.write(''.join(plaintext) +"\n")
keyfile.write(''.join(ciphertext) + "\n")
keyfile.write('Key: '+ str(keytext) + "\n")
keyfile.close()






