# Web-Azzembly

### Challenge Details
...

### Setup instructions
- Run `node chall.js` 

### Key Concepts
The WebAssembly binary checks a system of congruent equations. The JavaScript program modifies this binary based on user input. Solve the system to retrieve the correct input.

### Solution
- The exported WebAssembly function checks multiple equations of the form `x + y == z (mod 64)`. The return value is the number of invalid equations (so `0` means all equations are correct).
- Each character in the user input modifies the LHS of some equations. The aim is to find the flag so that all equations are satisfied, i.e. solve the system.
- For each flag character, the equations it modifies are roughly `offset + scale * equation_index` for some fixed `offset` and `scale`. Find the `offset` and `scale` to retrieve the LHS of the equations.
- The RHS of each equation can be retrieved similarly.
- Use Z3 theorem prover to find a solution for the system of equations and retrieve the flag.

### Learning Objectives
- Learn how to reverse a WebAssembly binary.
- Learn how to use Z3 or similar constraints solvers.

### Flag
`grey{d1d_y0u_u53_4_c0nstr4int_s0lv3r_cuz_th1s_f1ag_1s_90nna_be_v3ry_lo0o0o00oo0ng}`
