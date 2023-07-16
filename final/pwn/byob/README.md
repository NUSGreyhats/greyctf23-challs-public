# BYOB

## Description

```
BYOB (Bring Your Own Bytecode)!

I don't understand why we don't just ship bytecode instead of javascript code to JS interpreters.
So much time wasted on interpreting!

Luckily, I've fixed that. Now quickjs can even become quickerjs.

Note: compiled from latest commit of quickjs

`nc <host> <port>`
```

## Setup

1. Distribute files in `/dist`
2. `docker compose up` (Edit port if necessary)

## Exploit


## Concept

quickjs is not meant to run arbitrary bytecode.

The bytecode VM can easily be corrupted given handwritten bytecode.

