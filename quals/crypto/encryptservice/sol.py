from pwn import * 

io = remote("localhost", 1337)
io.recvline()
io.recvline()
io.recvuntil(b': ')

# Any plaintext of length 40 works
plaintext = ('b' * 40).encode().hex()
io.sendline(plaintext.encode())

keystreams = []
for i in range(256):
    server_response = io.recvline().decode().strip()
    ciphertext = server_response.split(": ")[1]
    keystream = xor(bytes.fromhex(plaintext), bytes.fromhex(ciphertext))
    keystreams.append(keystream)

io.recvline()
io.recvline()
io.recvline()
enc_flag = io.recvline().decode().strip().split(": ")[1]
enc_flag = bytes.fromhex(enc_flag)

for keystream in keystreams:
    temp = xor(keystream, enc_flag)
    if b'grey' in temp:
        print(temp.decode())
        break