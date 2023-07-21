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
create_output_folder('key')

plainu = [ chr(letter) for letter in range(65, 65+26)] # Uppercase Letters
plainl = [ chr(letter) for letter in range(97, 97+26)] # Lowercase Letters
plainm = [' ', '.'] 

cipherm = ['@', '_']

# Combine upper, lower and symbols
plain = plainu + plainl + plainm

def ceaser(opath,plaintexts,plain):

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

def rotation(opath,plaintexts,plain):

    inputfile="Rotate-Plain.txt"
    outputfile = opath + "Cipher".join(inputfile.split("-Plain"))

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

def vernam(opath,plaintexts,plain):
    inputfile="Vernam-Plain.txt"
    outputfile = opath + "Cipher".join(inputfile.split("-Plain"))

    cipherm = ['@', '_']

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

def vigenere(opath, plaintexts,key):

    plainu = [ chr(letter) for letter in range(65, 65+26)] # Uppercase Letters
    plainl = [ chr(letter) for letter in range(97, 97+26)] # Lowercase Letters
    plainm = [' ', '.'] 

    cipherm = ['@', '_']

    inputfile="Vigenere-Plain.txt"
    outputfile = opath + "Cipher".join(inputfile.split("-Plain"))

    for i in range(len(plaintexts)):

        if key!='random':
            keytext=key
        else:
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


def transposition(opath,plaintexts):

    inputfile="Transpose-Plain.txt"
    outputfile = opath + "Cipher".join(inputfile.split("-Plain"))

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

        if idx<9:output=('0'+str(idx+1)+'.').join(outputfile.split('.'))
        else: output=(str(idx+1)+'.').join(outputfile.split('.'))
        
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


class Switcher(object): 
    def indirect(self, i): 
        # to call the required method of cryptography 
        method_name = 'choice_'+str(i) 
        method = getattr(self, method_name, lambda: print('Invalid option')) 
        return method() 
    
    def choice_1(self): 
        ceaser(opath,plaintexts,plain)

    def choice_2(self):
        rotation(opath,plaintexts,plain)

    def choice_3(self):
        vernam(opath,plaintexts,plain)
    
    def choice_4(self):
        vigenere(opath,plaintexts)
    
    def choice_5(self):
        transposition(opath,plaintexts)

s = Switcher() # Creating object of Switcher Class 
ch = int(input("Select the cryptography method:\n(1)Ceaser Cipher.\n(2)Rotation Cipher.\n(3)Vernam Cipher.\n(4)Vigenere Cipher.\n(5)Transposition Cipher.\n")) 
s.indirect(ch) 

 

