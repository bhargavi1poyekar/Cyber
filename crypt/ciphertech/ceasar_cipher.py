# generate cipher text and transformation keys as per Ceasers Cipher.

import os, sys, random
plainu = [ chr(letter) for letter in range(65, 65+26)] # Uppercase Letters
plainl = [ chr(letter) for letter in range(97, 97+26)] # Lowercase Letters
plainm = [' ', '.'] 
cipheru = [ chr(letter) for letter in range(65, 65+26)] 
cipherl = [ chr(letter) for letter in range(97, 97+26)]
cipherm = ['@', '_']

# Shuffle cipher chars randomly
random.shuffle(cipheru)
random.shuffle(cipherl)
random.shuffle(cipherm)

# Combine upper, lower and symbols
plain = plainu + plainl + plainm
cipher = cipheru + cipherl + cipherm

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

# Not used
inpath = "/".join(inputfile.split("/")[:-1])


# Output file name -> Split input file (Ceaser-Plain-01.txt) on Plain -> so we get [Ceaser, 01] 
# and join them with Cipher-> opath/CeaserCipher01.txt
outputfile = opath + "Cipher".join(inputfile.split("/")[-1].split("-Plain-"))

# Read the input file
plaintext = infile.read()
infile.close()

ciphertext = [] # List for cipertext
keycount = dict()

for ch in plaintext: # For every character in plaintext
    if ch in plain: # If it is in plain
        index = plain.index(ch) # Get index of the plain
        ciphertext.append(cipher[index]) # append the cipher at that index in cipher

        # To keep frequency count
        if ch not in plainm: # If ch is a letter (and not symbol)
            val = keycount.get(ch,0) # Get Value(count) of char, return 0 if char not in keycount
            keycount[ch] = val + 1 # Increment the count 
    else:
        ciphertext.append(ch) # If plaintext is not a upper, lower, space and dot, dont replace

ofile = open(outputfile,"w") # Open the file in writing mode
ofile.write(''.join(ciphertext)) # Write the ciphertext in output file

# write key for a character with max occurrence.
ofile.write("\n")
ofile.write("Key mapping (ciphertext->plaintext) for max occurring character\n")
keyalpha = max(keycount, key=keycount.get) # Get character with max freq
ofile.write(cipher[plain.index(keyalpha)] + " -> " + keyalpha + "\n") 

ofile.close()


keyfilename = ".".join(inputfile.split(".")[:-1])+".key"
keyfile = open(keyfilename, "w")
keyfile.write(''.join(plain) +"\n")
keyfile.write(''.join(cipher) + "\n")
keyfile.close()
