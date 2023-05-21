# MonkeyType

## Description

```
monkeytype is overrated.

`stty -icanon -echo ; nc <host> <port>; stty sane`
```

## Setup

1. Distribute files in `/dist`
2. `docker compose up` (Edit port if necessary)

## Exploit

Backspace 72 times, then press 'A' 5 times.

## Concept

Meant to be a mini source code reading basic challenge.
No special tools required to solve.
Just read some code and press some buttons.

The backspace is unbounded, you can "backspace" many times and cause idx to be negative.
```c
        if((ch = getch()) == ERR){
        } else if (ch == '\x7f') {
            idx--;
            update_text(mainwin, buf, idx);
        } else if (ch >= 0x20 && ch < 0x7f) {
            ...
            if (idx < QUOTE_LEN) {
                buf[idx++] = ch;
                update_text(mainwin, buf, idx);
            }
            ...
        }
```

With a negative `idx` we can overwrite other variables in the stack.

```c
        /* win condition */
        if (highscore > POWERPUFF_GIRLS_SCORE) {
            endwin();
            puts("You win! Here's the flag:");
            puts("grey{I_am_M0JO_J0JO!}");
            exit(0);
        }
```

Target `highscore` to overwrite, this is 72 bytes away from our buffer, so we have to backspace 72 times.
Then we type at least 5 characters to meet the win condition.
Alternatively, backspace 68 times and type any character.