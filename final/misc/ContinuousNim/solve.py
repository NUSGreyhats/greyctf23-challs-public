from pwn import *

PRECISION = 1000

conn = remote("127.0.0.1", 19600)
conn.recvline()

state_str = conn.recvline(keepends=False)[1:-1].decode()
state: list[float] = list(map(float, state_str.split(", ")))

conn.recvuntil(b"of ")
R = float(conn.recvline(keepends=False).decode())
scaled_R = round(R * PRECISION)

L = 0
# Choose correct L
for try_L in range(1, scaled_R):
    scaled_LR = round(R * PRECISION) + try_L
    grundy = 0
    for pile in range(len(state)):
        scaled_state = round(state[pile] * PRECISION)
        grundy ^= (scaled_state % scaled_LR) // try_L

    if grundy != 0:
        L = round(try_L / 1000, 3)
        break

assert(L != 0)
print(L)
conn.sendlineafter(b": ", str(L).encode())

scaled_L = round(L * PRECISION)
scaled_LR = round((L + R) * PRECISION)

def getInput():
    for pile in range(len(state)):
        for num in range(scaled_L, min(scaled_R, round(state[pile] * PRECISION)) + 1):
            # calculate grundy value
            grundy = 0
            for i in range(len(state)):
                scaled_state = round(state[i] * PRECISION)
                if i == pile: grundy ^= ((scaled_state - num) % scaled_LR) // scaled_L
                else: grundy ^= (scaled_state % scaled_LR) // scaled_L

            if grundy == 0:
                return str(pile), str(round(num / PRECISION, 3))

    assert(False)


while True:
    print(state)
    
    if "#" in conn.clean().decode():
        print("Lost")
        break

    pile, num = getInput()
    conn.sendline(pile.encode())
    conn.sendlineafter(b": ", num.encode())

    pile, num = int(pile), float(num)
    state[pile] = round(state[pile] - num, 3)

    conn.recvline()
    next_line = conn.recvline(keepends=False).decode()

    if "grey" in next_line:
        print(next_line)
        break

    next_input = next_line.split(": ")[1]
    bot_pile = int(next_input)
    conn.recvuntil(b": ")
    bot_num = float(conn.recvline(keepends=False).decode())

    state[bot_pile] = round(state[bot_pile] - bot_num, 3)
