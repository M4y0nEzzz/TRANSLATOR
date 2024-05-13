# Генератор кода
from O_ERROR import *
from O_TABLE import *

MemSize = 1024
cmDup = 6
cmNeg = 7
cmSub = 8
cmMod = 9
cmIfNE = 0
cmIfEQ = 1
cmIfGT = 2
cmIfLT = 3
cmIfLE = 4
cmIfGE = 5

PC = 0

MaxInt = 2147483647

lexEQ = '=='
lexNE = '!='
lexLE = '<='
lexLT = '<'
lexGE = '>='
lexGT = '>'


M = [0] * MemSize

FirstVar = None
NextVar = None


def init_gen():
    global PC
    PC = 0


def gen(cmd):
    global PC, M
    if PC < MemSize:
        M[PC] = cmd
        PC += 1
    else:
        error('Недостаточно памяти для кода')


def fixup(a):
    global PC, M
    while a > 0:
        temp = M[a - 2]
        M[a - 2] = PC
        a = temp


def gen_abs():
    gen(cmDup)
    gen(0)
    gen(PC + 3)
    gen(cmIfGE)
    gen(cmNeg)


def gen_min():
    gen(MaxInt)
    gen(cmNeg)
    gen(1)
    gen(cmSub)


def gen_odd():
    gen(2)
    gen(cmMod)
    gen(1)
    gen(0)  # Адрес перехода вперед
    gen(cmIfNE)


def gen_const(c):
    gen(abs(c))
    if c < 0:
        gen(cmNeg)


def gen_comp(op):
    gen(0)  # Переход вперед
    if op == lexEQ:
        gen(cmIfNE)
    elif op == lexNE:
        gen(cmIfEQ)
    elif op == lexLE:
        gen(cmIfGT)
    elif op == lexLT:
        gen(cmIfGE)
    elif op == lexGE:
        gen(cmIfLT)
    elif op == lexGT:
        gen(cmIfLE)


def gen_addr(x):
    global PC
    gen(x.val)  # В текущую ячейку адрес предыдущей + 2
    x.val = PC + 1  # Адрес+2 = PC+1


def allocate_variables():
    global PC, M
    v_ref = first_var()  # Найти первую переменную
    while v_ref is not None:
        if v_ref.val == 0:
            pass  # Warning('Переменная ' + v_ref.name + ' не используется')
        elif PC < MemSize:
            fixup(v_ref.val)  # Адресная привязка переменной
            PC += 1
        else:
            error('Недостаточно памяти для переменных')
        v_ref = next_var()  # Найти следующую переменную
