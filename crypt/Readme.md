# Cryptography Techniques for Cryptanalysis Attacks Exercise

## Techniques used:

1. Rotation Cipher
2. Vigenere Cipher
3. Vernam Cipher
4. Transposition Cipher


## Overview of Techniques:

1. Rotation Cipher:

    -> A rotation cipher, also known as a Caesar cipher, is a simple method of encrypting a message by shifting each letter in the message by a fixed number of positions down the alphabet. 
    -> For example, with a shift of 3, 'A' would be replaced by 'D', 'B' by 'E', 'C' by 'F', and so on. -> When the end of the alphabet is reached, the counting wraps around to the beginning. For instance, 'X' would be replaced by 'A', 'Y' by 'B', and 'Z' by 'C'.

2. Vigener Cipher:

    -> The Vigenère cipher is a polyalphabetic substitution cipher that provides a higher level of security compared to simple substitution ciphers like the Caesar cipher.
    -> Unlike the Caesar cipher, which uses a fixed shift for all letters, the Vigenère cipher uses a keyword or phrase to determine the shifting of letters. The keyword is repeated to match the length of the message being encrypted.
    -> Working of Vigenere Cipher:
        1. Choose a keyword or phrase. For example, "KEY" or "SECRET".
        2. Convert the keyword to numeric values, using a letter-to-number mapping such as A=0, B=1, C=2, and so on. In this case, "KEY" would be converted to [10, 4, 24].
        3. Take the message you want to encrypt and repeat the keyword to match its length. For example, if the message is "HELLO WORLD" and the keyword is "KEY", repeat the keyword as "KEYKEYKEYKEYKEYKEYKE" to match the length of the message.
        4. Convert each letter of the message to its corresponding numeric value, similar to step 2.
        5. For each letter in the message, shift it by the corresponding value from the keyword. For example, if the first letter is 'H' (7 in the numeric mapping) and the first letter of the keyword is 'K' (10 in the numeric mapping), the resulting letter would be 'X' (17 in the numeric mapping).
        6. Repeat steps 4 and 5 for each letter in the message, using the next letter from the keyword each time.
        7. The resulting encrypted message is formed by converting the numeric values back to letters.


3. Vernam Cipher:

    -> The Vernam cipher operates by combining the plaintext message with a random key of the same length to produce the encrypted ciphertext. 
    -> The key is typically generated as a random sequence of characters, such as letters or numbers.

    -> Working of Vernam Cipher:

        1. Choose a plaintext message that you want to encrypt. For example, "HELLO".
        2. Generate a random key of the same length as the plaintext. For example, "XMCKL".
        3. Convert both the plaintext and the key to a numerical representation, such as using a letter-to-number mapping (e.g., A=0, B=1, C=2, and so on). For "HELLO", the numerical representation could be [7, 4, 11, 11, 14], and for "XMCKL", it could be [23, 12, 2, 10, 11].
        4. Perform bitwise XOR (exclusive OR) operation between each corresponding pair of numbers in the plaintext and the key. XOR combines the bits such that if the corresponding bits are the same, the result is 0; otherwise, it is 1. For example, XOR between 7 and 23 would result in 16, XOR between 4 and 12 would result in 8, and so on.
        5. Convert the resulting numerical values back to letters using the same mapping used in step 3. In this case, the ciphertext would be "QHOPF". 

4. Columnar Transposition Cipher:

    -> A transposition cipher is a cryptographic technique that involves rearranging the letters or characters of a message without changing the actual letters themselves. 
    -> Instead of substituting letters with other letters or symbols, as in substitution ciphers, transposition ciphers focus on changing the order of the characters. 
    -> In Columnar Transposition the message is written out in rows of a fixed length, and the columns are read out in a different order to obtain the ciphertext. 
    -> The columns are chosen in some scrambled order. Both the width of the rows and the permutation of the columns are usually defined by a keyword. For example, the word ZEBRAS is of length 6 (so the rows are of length 6), and the permutation is defined by the alphabetical order of the letters in the keyword. In this case, the order would be "6 3 2 4 1 5". 
    -> In a regular columnar transposition cipher, any spare spaces are filled with nulls; in an irregular columnar transposition cipher, the spaces are left blank. Finally, the message is read off in columns, in the order specified by the keyword. 

    -> Working of Transposition Cipher:

        1. Choose a plaintext message that you want to encrypt. For example, "HELLO WORLD".
        2. Select a key that determines the order in which the columns will be read. The key is typically a keyword or a series of numbers. For this example, let's use the key "3142". Write the plaintext message in rows, with the number of rows equal to the length of the key. 
        3. Label the columns of the rows with the numbers from the key. In this case, the columns are labeled as 3, 1, 4, and 2.
        4. Read the columns of the rows in the order specified by the key. i.e. The column with number 1 is read first, then 2 , and so on.
        5. The resulting rearranged message is the ciphertext. In this case, the ciphertext is "LOHRELLWOD".
    

## Programs Execution:

-> The programs have default plaintexts and output folder. If user wants to give theis own input,
they can give it using -i and -o flags in commandline. 

python cipher.py -i plaintext_path -o cipher_folder_path

Eg: python cipher.py -i Plain.txt -o ciphertext

-> Then select the cipher method you want. 


