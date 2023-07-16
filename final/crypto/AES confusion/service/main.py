#!/usr/local/bin/python

import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

FLAG = b"grey{tr4v3ll1n9_84ck_1n_t1m3}"
key = random.randbytes(16)
iv = random.randbytes(16)
cipher = AES.new(key, AES.MODE_CBC, iv=iv)
FLAG = cipher.encrypt(pad(FLAG, AES.block_size))

menu = """Secure Flag Storage
1. Encrypt a random string
2. Decrypt a string
3. Get encrypted flag
Choice: """

def encrypt():
    pt = input("Plaintext: ")
    try:
        pt = bytes.fromhex(pt)
    except:
        return
    iv = random.randbytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    ct = cipher.encrypt(pad(pt, AES.block_size))
    print(f"Ciphertext: {ct.hex()}")

def decrypt(): # i'm not sure why this doesn't work
    ct = input("Ciphertext: ")
    try:
        ct = bytes.fromhex(ct)
    except:
        return
    cipher = AES.new(key, AES.MODE_ECB)
    pt = cipher.decrypt(ct)
    print(f"Plaintext: {pt.hex()}")

def print_flag():
    print(f"Flag: {FLAG.hex()}")

while True:
    choice = int(input(menu))
    if choice == 1:
        encrypt()
    elif choice == 2:
        decrypt()
    elif choice == 3:
        print_flag()
        break
    else:
        break
