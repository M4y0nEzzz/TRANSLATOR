MEM_SIZE = 8 * 1024

CM_STOP = -1

CM_ADD = -2
CM_SUB = -3
CM_MULT = -4
CM_DIV = -5
CM_MOD = -6
CM_NEG = -7

CM_LOAD = -8
CM_SAVE = -9

CM_DUP = -10
CM_DROP = -11
CM_SWAP = -12
CM_OVER = -13

CM_GOTO = -14
CM_IF_EQ = -15
CM_IF_NE = -16
CM_IF_LE = -17
CM_IF_LT = -18
CM_IF_GE = -19
CM_IF_GT = -20

CM_IN = -21
CM_OUT = -22
CM_OUT_LN = -23

# Инициализация памяти
M = [0] * MEM_SIZE


def run():
    pc = 0
    sp = MEM_SIZE
    cmd = M[pc]
    while cmd != CM_STOP:
        pc += 1
        if cmd >= 0:
            sp -= 1
            M[sp] = cmd
        else:
            if cmd == CM_ADD:
                sp += 1
                M[sp] = M[sp] + M[sp - 1]
            elif cmd == CM_SUB:
                sp += 1
                M[sp] = M[sp] - M[sp - 1]
            elif cmd == CM_MULT:
                sp += 1
                M[sp] = M[sp] * M[sp - 1]
            elif cmd == CM_DIV:
                sp += 1
                M[sp] = M[sp] // M[sp - 1]
            elif cmd == CM_MOD:
                sp += 1
                M[sp] = M[sp] % M[sp - 1]
            elif cmd == CM_NEG:
                M[sp] = -M[sp]
            elif cmd == CM_LOAD:
                M[sp] = M[M[sp]]
            elif cmd == CM_SAVE:
                M[M[sp + 1]] = M[sp]
                sp += 2
            elif cmd == CM_DUP:
                sp -= 1
                M[sp] = M[sp + 1]
            elif cmd == CM_DROP:
                sp += 1
            elif cmd == CM_SWAP:
                buf = M[sp]
                M[sp] = M[sp + 1]
                M[sp + 1] = buf
            elif cmd == CM_OVER:
                sp -= 1
                M[sp] = M[sp + 2]
            elif cmd == CM_GOTO:
                pc = M[sp]
                sp += 1
            elif cmd == CM_IF_EQ:
                if M[sp + 2] == M[sp + 1]:
                    pc = M[sp]
                sp += 3
            elif cmd == CM_IF_NE:
                if M[sp + 2] != M[sp + 1]:
                    pc = M[sp]
                sp += 3
            elif cmd == CM_IF_LE:
                if M[sp + 2] <= M[sp + 1]:
                    pc = M[sp]
                sp += 3
            elif cmd == CM_IF_LT:
                if M[sp + 2] < M[sp + 1]:
                    pc = M[sp]
                sp += 3
            elif cmd == CM_IF_GE:
                if M[sp + 2] >= M[sp + 1]:
                    pc = M[sp]
                sp += 3
            elif cmd == CM_IF_GT:
                if M[sp + 2] > M[sp + 1]:
                    pc = M[sp]
                sp += 3
            # Пропущены операции ввода/вывода, так как они требуют дополнительной реализации
            else:
                print('Недопустимый код операции')
                M[pc] = CM_STOP
        cmd = M[pc]