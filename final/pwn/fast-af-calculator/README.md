# Description

Try out our newest calculator model, known to be the fastest ever!! (or you can just do the pwn challenge...)

Unfortunately, it only supports addition, but it should be faaaaaaaaaaaaaaaaaast as fudge.

# Setup Instructions

```sh
docker build . -t fast-af-calculator-pwn
docker run -d -p 32110:5000 --privileged fast-af-calculator-pwn
```

# Key Concepts

- ROP chain

- ret2libc

- misaligned instructions

# Solution

see solve.py

# Flag

**grey{budg3t_j1t_c0mp1l3r}**
