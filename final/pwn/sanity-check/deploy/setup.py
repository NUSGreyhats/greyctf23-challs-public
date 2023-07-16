#!/usr/bin/python3

import subprocess
import os
import sys

p = subprocess.Popen(["/home/ctf/pow"], stdout=subprocess.PIPE)
print(p.stdout.readline().decode().strip())
out = p.communicate()[0].decode()
if out != "solution: good\n":
    print(out)
    sys.exit(0)

p = subprocess.Popen(['bash', '/home/ctf/run.sh'])
try:
    p.wait(600)
except subprocess.TimeoutExpired:
    p.kill()
