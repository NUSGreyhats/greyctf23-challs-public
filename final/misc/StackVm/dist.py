from typing import List


class StackVM(object):
    def __init__(self: 'StackVM') -> None:
        self.stack = []
        self.pc = 0  # Program counter
        self.line_execution = 0  # Length of execution
        self.max_execution = 150000  # Max length of execution

    def _push(self, value: int) -> None:
        self.stack.append(value)

    def _pop(self) -> None:
        if self.stack:
            return self.stack.pop()
        else:
            raise IndexError("Stack is empty")

    def _nand(self) -> None:
        if len(self.stack) >= 2:
            a = self._pop()
            b = self._pop()
            result = ~(a & b)
            self._push(result)
        else:
            raise IndexError("Insufficient operands on the stack")

    def _jne(self, target) -> None:
        if self._pop() != 0:
            self.pc = target

    def _je(self, target) -> None:
        if self._pop() == 0:
            self.pc = target

    def _swap(self, to, fro) -> None:
        if len(self.stack) >= 2:
            tmp = self.stack[-1-fro]
            self.stack[-1-fro] = self.stack[-1-to]
            self.stack[-1-to] = tmp
        else:
            raise IndexError("Insufficient operands on the stack")

    def _dup(self) -> None:
        if self.stack:
            self._push(self.stack[-1])
        else:
            raise IndexError("Stack is empty")

    def _shift(self) -> None:
        if len(self.stack) >= 2:
            a = self._pop()
            b = self._pop()
            result = (b << a)
            self._push(result)
        else:
            raise IndexError("Insufficient operands on the stack")

    def _execute(self, bytecode: List[str]) -> None:
        while self.pc < len(bytecode):
            instruction = bytecode[self.pc]

            if self.line_execution > self.max_execution:
                raise Exception("Max execution length reached")

            self.pc += 1
            self.line_execution += 1

            if instruction == "NAND":
                self._nand()
            elif instruction.startswith("JNE"):
                target = int(instruction[3:])
                self._jne(target)
            elif instruction.startswith("JE"):
                target = int(instruction[2:])
                self._je(target)
            elif instruction.startswith("SWAP "):
                _, arg1, arg2 = instruction.split(" ")
                self._swap(int(arg1), int(arg2))
            elif instruction == "DUP":
                self._dup()
            elif instruction == "SHIFT":
                self._shift()
            elif instruction.startswith("PUSH"):
                value = int(instruction[4:])
                self._push(value)
            elif instruction == "POP":
                self._pop()
            else:
                raise ValueError("Invalid instruction: " + instruction)

    def _reset(self) -> None:
        self.line_execution = 0
        self.pc = 0
        self.stack = []

    @staticmethod
    def compile(program: str) -> List[str]:
        """Compile this program into bytecode"""
        return list(
            filter(
                lambda x: len(x) > 0,
                map(
                    lambda x: x.strip().upper(),
                    program.split("\n")
                )
            )
        )

    def run(self: 'StackVM', bytecode: List[str], args: List[int]) -> int:
        """Returns final answer on stack and number of instructions in code"""
        # Code cannot be too long (Prevent hard coding)
        if len(bytecode) > 1000:
            return -1

        self._reset()
        for i in args:
            self.stack.append(i)
        try:
            self._execute(bytecode)
        except:
            pass
        return self.stack[-1] if len(self.stack) > 0 else -1
