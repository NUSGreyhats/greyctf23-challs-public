export glibc_install=/root/glibc/build/install
gcc -L "${glibc_install}/lib"   -I "${glibc_install}/include"   -Wl,--rpath="${glibc_install}/lib"   -Wl,--dynamic-linker="${glibc_install}/lib/ld-linux-x86-64.so.2"   -no-pie -fno-stack-protector -o chall ./chall.c
python3 patch.py
mv chall.patched chall
chmod +x chall
mv ./chall ../
