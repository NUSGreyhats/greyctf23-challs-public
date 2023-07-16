
# Sick - pwn
| Sick                            |                                                                           |
| ------------------------------- | ------------------------------------------------------------------------- |
| Challenge Details               | `Idk what this program is doing??? can you help`                                                                     |
| Possible hints                  | `Maybe you can change permissions somewhere?`                                           |
| Key concepts                    | `Scripting, ROP`                                                               |
| Solution (Can also be a script) | `Sigreturn based ROP to set execution permission on mem space and execute shellcode to get shell and read flag`                          |
| Learning objectives             | `ROP, changing permission in memory space`                                                                     |
| Flag                            | `grey{s1gr3tuRn_s4V3s_7He_D4Y_gsfs9761bk}`                                  |

# Setup
```sh
docker build . -t sick-pwn 
docker run -d -p 32111:5000 --privileged sick-pwn
```
