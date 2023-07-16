ld = b"/root/glibc/build/install/lib/ld-linux-x86-64.so.2"
ldr = b"./lib/ld-linux-x86-64.so.2"
ldr += b"\x00"*(len(ld)-len(ldr))
path = b"/root/glibc/build/install/lib"
pathr = b"./lib"
pathr += b"\x00"*(len(path)-len(pathr))

with open("./chall", "rb") as f:
    contents = f.read()

ld_idx = contents.find(ld)
path_idx = contents.find(path, ld_idx+1)
contents = contents.replace(ld, ldr)
contents = contents.replace(path, pathr)

with open("./chall.patched", "wb") as f:
    f.write(contents)
