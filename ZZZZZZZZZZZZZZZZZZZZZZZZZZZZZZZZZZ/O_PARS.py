# Распознаватель


from O_SCAN import *
from O_GEN import *
from OVM import *
from O_TABLE import *
from typing import Optional


class Cat:
    CONST, VAR, TYPE, STPROC, MODULE, GUARD = range(6)


class tType:
    typNONE, typINT, typBOOL = range(3)


class tObj:
    def __init__(self, name: 'TName', cat: 'TCat', typ: 'TType', val: int, prev: Optional['TObjRec']):
        self.name = name
        self.cat = cat
        self.typ = typ
        self.val = val
        self.prev = prev


# Константы
spABS = 1
spMAX = 2
spMIN = 3
spDEC = 4
spODD = 5
spHALT = 6
spINC = 7
spInOpen = 8
spInInt = 9
spOutInt = 10
spOutLn = 11


name_len = 31
PC = 0


lexMODULE = 'MODULE'
lexName = 'NAME'
lexSemi = ';'
lexIMPORT = 'IMPORT'
lexBEGIN = 'BEGIN'
lexEND = 'END'
lexDot = '.'

catModule = 'MODULE'
cmStop = 'STOP'


# Функции, заменяющие процедуры Pascal
def check(L, M):
    global Lex
    if Lex != L:
        expected(M)
    else:
        next_lex()


def const_expr(V):
    global Lex, Num, Name
    X = tObj()
    Op = '+'
    if Lex in ['+', '-']:
        Op = Lex
        next_lex()
    if Lex == 'NUM':
        V = Num
        next_lex()
    elif Lex == 'NAME':
        find(Name, X)
        if X.Cat == 'catGuard':
            error('Нельзя определять константу через себя')
        elif X.Cat != 'catConst':
            expected('имя константы')
        else:
            V = X.Val
        next_lex()
    else:
        expected('константное выражение')
    if Op == '-':
        V = -V
    return V


def const_decl():
    global Lex, Name
    ConstRef = tObj()
    new_name(Name, 'catGuard', ConstRef)
    next_lex()
    check('=', '"="')
    ConstRef.Val = const_expr(ConstRef.Val)
    ConstRef.Typ = 'typInt'
    ConstRef.Cat = 'catConst'


def parse_type():
    global Lex, Name  # Предполагается, что эти переменные определены глобально

    if Lex != lexName:
        expected('имя')
    else:
        TypeRef = find(Name)
        if TypeRef.cat != Сat.Type:
            expected('имя типа')
        elif TypeRef.typ != typInt:
            expected('целый тип')
        next_lex()


def var_decl():
    global Lex, Name
    if Lex != 'NAME':
        expected('имя')
    else:
        NameRef = tObj()
        new_name(Name, 'catVar', NameRef)
        NameRef.Typ = 'typInt'
        next_lex()
    while Lex == ',':
        next_lex()
        if Lex != 'NAME':
            expected('имя')
        else:
            NameRef = tObj()
            new_name(Name, 'catVar', NameRef)
            NameRef.Typ = 'typInt'
            next_lex()
    check(':', '":"')
    parse_type()


def decl_seq():
    global Lex
    while Lex in ['CONST', 'VAR']:
        if Lex == 'CONST':
            next_lex()
            while Lex == 'NAME':
                const_decl()
                check(';', '";"')
        else:
            next_lex()  # VAR
            while Lex == 'NAME':
                var_decl()
                check(';', '";"')


def int_expression():
    T = tType()
    expression(T)
    if T != 'typInt':
        expected('выражение целого типа')


def st_func(F, T):
    if F == spABS:
        int_expression()
        gen_abs()
        T = 'typInt'
    elif F == spMAX:
        parse_type()
        gen(MaxInt)
        T = 'typInt'
    elif F == spMIN:
        parse_type()
        gen_min()
        T = 'typInt'
    elif F == spODD:
        int_expression()
        gen_odd()
        T = 'typBool'
    return T


def factor(T):
    global Lex, Name, Num
    X = tObj()
    if Lex == 'NAME':
        find(Name, X)
        if X.Cat == 'catVar':
            gen_addr(X)
            gen(CM_LOAD)
            T = X.Typ
            next_lex()
        elif X.Cat == 'catConst':
            gen_const(X.Val)
            T = X.Typ
            next_lex()
        elif X.Cat == 'catStProc' and X.Typ != 'typNone':
            next_lex()
            check('(', '"("')
            T = st_func(X.Val, T)
            check(')', '")"')
        else:
            expected('переменная, константа или процедура-функции')
    elif Lex == 'NUM':
        T = 'typInt'
        gen_const(Num)
        next_lex()
    elif Lex == '(':
        next_lex()
        expression(T)
        check(')', '")"')
    else:
        expected('имя, число или "("')
    return T


def term(T):
    global Lex
    Op = None
    T = factor(T)
    while Lex in ['*', '/', '%']:
        if T != 'typInt':
            error('Несоответствие операции типу операнда')
        Op = Lex
        next_lex()
        T = factor(T)
        if T != 'typInt':
            expected('выражение целого типа')
        if Op == '*':
            gen('cmMult')
        elif Op == '/':
            gen('cmDIV')
        elif Op == '%':
            gen('cmMOD')
    return T


def simple_expr(T):
    global Lex, Num, Name
    Op = None
    if Lex in ['+', '-']:
        Op = Lex
        next_lex()
        T = term(T)
        if T != 'typInt':
            expected('выражение целого типа')
        if Op == '-':
            gen('cmNeg')
    else:
        T = term(T)
    while Lex in ['+', '-']:
        if T != 'typInt':
            error('Несоответствие операции типу операнда')
        Op = Lex
        next_lex()
        T = term(T)
        if T != 'typInt':
            expected('выражение целого типа')
        if Op == '+':
            gen('cmAdd')
        elif Op == '-':
            gen('cmSub')


def expression(T):
    global Lex
    Op = None
    simple_expr(T)
    if Lex in ['==', '!=', '>', '>=', '<', '<=']:
        Op = Lex
        if T != 'typInt':
            error('Несоответствие операции типу операнда')
        next_lex()
        simple_expr(T)
        if T != 'typInt':
            expected('выражение целого типа')
        gen_comp(Op)
        T = 'typBool'


def variable():
    global Lex, Name
    X = tObj()
    if Lex != 'NAME':
        expected('имя')
    else:
        find(Name, X)
        if X.Cat != 'catVar':
            expected('имя переменной')
        gen_addr(X)
        next_lex()


def st_proc(sp):
    global Lex
    c = None
    if sp == spDEC:
        variable()
        gen('cmDup')
        gen('cmLoad')
        if Lex == ',':
            next_lex()
            int_expression()
        else:
            gen(1)
        gen('cmSub')
        gen('cmSave')
    elif sp == spINC:
        variable()
        gen('cmDup')
        gen('cmLoad')
        if Lex == ',':
            next_lex()
            int_expression()
        else:
            gen(1)
        gen('cmAdd')
        gen('cmSave')
    elif sp == spInOpen:
        pass
    elif sp == spInInt:
        variable()
        gen('cmIn')
        gen('cmSave')
    elif sp == spOutInt:
        int_expression()
        check(',', '","')
        int_expression()
        gen('cmOut')
    elif sp == spOutLn:
        gen('cmOutLn')
    elif sp == spHALT:
        c = const_expr(c)
        gen_const(c)
        gen('cmStop')


def bool_expression():
    T = tType()
    expression(T)
    if T != 'typBool':
        expected('логическое выражение')


def ass_statement():
    variable()
    if Lex == ':=':
        next_lex()
        int_expression()
        gen('cmSave')
    else:
        expected('":="')


def call_statement(sp):
    check('NAME', 'имя процедуры')
    if Lex == '(':
        next_lex()
        st_proc(sp)
        check(')', '")"')
    elif sp in [spOutLn, spInOpen]:
        st_proc(sp)
    else:
        expected('"("')


def if_statement():
    global Lex
    global PC
    CondPC = None
    LastGOTO = None
    check('IF', 'IF')
    LastGOTO = 0
    bool_expression()
    CondPC = PC
    check('THEN', 'THEN')
    stat_seq()
    while Lex == 'ELSIF':
        gen(LastGOTO)
        gen('cmGOTO')
        LastGOTO = PC
        next_lex()
        fixup(CondPC)
        bool_expression()
        CondPC = PC
        check('THEN', 'THEN')
        stat_seq()
    if Lex == 'ELSE':
        gen(LastGOTO)
        gen('cmGOTO')
        LastGOTO = PC
        next_lex()
        fixup(CondPC)
        stat_seq()
    else:
        fixup(CondPC)
    check('END', 'END')
    fixup(LastGOTO)


def while_statement():
    global PC
    while_pc = PC
    check('WHILE')
    bool_expression()
    cond_pc = PC
    check('DO')
    stat_seq()
    check('END')
    gen(while_pc)
    gen('GOTO')
    fixup(cond_pc)


def statement():
    global lex, name
    if lex == 'NAME':
        x = find(name)
        if x['Cat'] == 'MODULE':
            next_lex()
            check('.')
            if lex == 'NAME' and (len(x['Name']) + len(name) < name_len):
                find(f"{x['Name']}.{name}")
            else:
                expected('имя из модуля ' + x['Name'])
        if x['Cat'] == 'VAR':
            ass_statement()  # Присваивание
        elif x['Cat'] == 'STPROC' and x['Typ'] == 'NONE':
            call_statement() (x['Val'])  # Вызов процедуры
        else:
            expected('обозначение переменной или процедуры')
    elif lex == 'IF':
        if_statement()
    elif lex == 'WHILE':
        while_statement()


def stat_seq():
    statement()  # Оператор
    while lex == 'SEMI':
        next_lex()
        statement()  # Оператор


def import_module():
    global lex, name
    if lex == 'NAME':
        new_name(name, 'MODULE')
        if name == 'In':
            enter('In.Open', 'STPROC', 'NONE', 'spInOpen')
            enter('In.Int', 'STPROC', 'NONE', 'spInInt')
        elif name == 'Out':
            enter('Out.Int', 'STPROC', 'NONE', 'spOutInt')
            enter('Out.Ln', 'STPROC', 'NONE', 'spOutLn')
        else:
            error('Неизвестный модуль')
        next_lex()
    else:
        expected('имя импортируемого модуля')


def import_():
    check('IMPORT')
    import_module()
    while lex == 'COMMA':
        next_lex()
        import_module()
    check('SEMI')


def module():
    global Lex, Name, ModRef
    check(lexMODULE, 'MODULE')
    if Lex != lexName:
        expected('имя модуля')
    else:  # Имя модуля - в таблицу имен
        new_name(Name, catModule, ModRef)
    next_lex()
    check(lexSemi, '";"')
    if Lex == lexIMPORT:
        import_()
    decl_seq()
    if Lex == lexBEGIN:
        next_lex()
        stat_seq()
    check(lexEND, 'END')

    # Сравнение имени модуля и имени после END
    if Lex != lexName:
        expected('имя модуля')
    elif Name != ModRef.name:  # Предполагается, что ModRef это объект с атрибутом name
        expected(f'имя модуля "{ModRef.name}"')
    else:
        next_lex()
    if Lex != lexDot:
        expected('"."')
    gen(0)  # Код возврата
    gen(cmStop)  # Команда останова
    allocate_variables()  # Размещение переменных


def compile():
    init_name_table()
    open_scope()  # Блок стандартных имен
    enter('ABS', 'catStProc', 'typInt', 'spABS')
    enter('MAX', 'catStProc', 'typInt', 'spMAX')
    enter('MIN', 'catStProc', 'typInt', 'spMIN')
    enter('DEC', 'catStProc', 'typNone', 'spDEC')
    enter('ODD', 'catStProc', 'typBool', 'spODD')
    enter('HALT', 'catStProc', 'typNone', 'spHALT')
    enter('INC', 'catStProc', 'typNone', 'spINC')
    enter('INTEGER', 'catType', 'typInt', 0)
    open_scope()  # Блок модуля
    module()
    close_scope()  # Блок модуля
    close_scope()  # Блок стандартных имен
    print()
    print('Компиляция завершена')