# Распознаватель


from O_SCAN import *
from O_GEN import *
from OVM import *
from O_TABLE import *
from typing import Optional


class Cat:
    CONST, VAR, TYPE, STPROC, MODULE, GUARD = range(6)


class t_type:
    typNONE, typINT, typBOOL = range(3)


class TName:
    slots = ['name']

    def __init__(self, name: str):
        if len(name) > name_len:
            raise ValueError(f"Имя не может быть длиннее {name_len} символов.")
        self.name = name

class tObj:
    def __init__(self, name: 'TName', cat: 'Cat', typ: 't_type', val: int, prev: Optional['tObj'] = None):
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

catModule = 'MODULE'
cmStop = 'STOP'

top = None


def check(l, m):
    if Lex != l:
        expected(m)
    else:
        next_lex()


def const_expr():
    v = None
    x = tObj(TName("Имя"), Cat.VAR, t_type.typINT, 0, None)
    op = '+'
    if Lex in ['+', '-']:
        op = Lex
        next_lex()
    if Lex == 'NUM':
        v = Num
        next_lex()
    elif Lex == 'NAME':
        find(Name, x)
        if x.cat == 'catGuard':
            error('Нельзя определять константу через себя')
        elif x.cat != 'catConst':
            expected('имя константы')
        else:
            v = x.val
        next_lex()
    else:
        expected('константное выражение')
    if op == '-':
        v = -v
    return v


def const_decl():
    const_ref = {}
    new_name(name, Cat.GUARD)
    next_lex()
    check('lexEQ', '=')
    const_ref['Val'] = const_expr()
    const_ref['Typ'] = 'typInt'
    const_ref['Cat'] = 'catConst'


def parse_type():
    if Lex != lexName:
        expected('имя')
    else:
        TypeRef = find(Name)
        if TypeRef.cat != Cat.TYPE:
            expected('имя типа')
        elif TypeRef.typ != t_type.typINT:
            expected('целый тип')
        next_lex()


def var_decl():
    if Lex != 'NAME':
        expected('имя')
    else:
        nameref = tObj()
        new_name(Name, 'catVar', nameref)
        nameref.Typ = 'typInt'
        next_lex()
    while Lex == ',':
        next_lex()
        if Lex != 'NAME':
            expected('имя')
        else:
            nameref = tObj()
            new_name(Name, 'catVar', nameref)
            nameref.Typ = 'typInt'
            next_lex()
    check(':', '":"')
    parse_type()


def decl_seq():
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
    T = t_type()
    expression(T)
    if T != 'typInt':
        expected('выражение целого типа')


def st_func(f, t):
    if f == spABS:
        int_expression()
        gen_abs()
        t = 'typInt'
    elif f == spMAX:
        parse_type()
        gen(MaxInt)
        t = 'typInt'
    elif f == spMIN:
        parse_type()
        gen_min()
        t = 'typInt'
    elif f == spODD:
        int_expression()
        gen_odd()
        t = 'typBool'
    return t


def factor(t):
    x = tObj()
    if Lex == 'NAME':
        find(Name, x)
        if x.cat == 'catVar':
            gen_addr(x)
            gen(CM_LOAD)
            t = x.typ
            next_lex()
        elif x.cat == 'catConst':
            gen_const(x.val)
            t = x.typ
            next_lex()
        elif x.cat == 'catStProc' and x.typ != 'typNone':
            next_lex()
            check('(', '"("')
            t = st_func(x.val, t)
            check(')', '")"')
        else:
            expected('переменная, константа или процедура-функции')
    elif Lex == 'NUM':
        t = 'typInt'
        gen_const(Num)
        next_lex()
    elif Lex == '(':
        next_lex()
        expression(t)
        check(')', '")"')
    else:
        expected('имя, число или "("')
    return t


def term(t):
    global Lex
    op = None
    t = factor(t)
    while Lex in ['*', '/', '%']:
        if t != 'typInt':
            error('Несоответствие операции типу операнда')
        op = Lex
        next_lex()
        t = factor(t)
        if t != 'typInt':
            expected('выражение целого типа')
        if op == '*':
            gen('cmMult')
        elif op == '/':
            gen('cmDIV')
        elif op == '%':
            gen('cmMOD')
    return t


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


def expression(t):
    global Lex
    op = None
    simple_expr(t)
    if Lex in ['==', '!=', '>', '>=', '<', '<=']:
        op = Lex
        if t != 'typInt':
            error('Несоответствие операции типу операнда')
        next_lex()
        simple_expr(t)
        if t != 'typInt':
            expected('выражение целого типа')
        gen_comp(op)
        t = 'typBool'


def variable():
    x = tObj()
    if Lex != 'NAME':
        expected('имя')
    else:
        find(Name, x)
        if x.cat != 'catVar':
            expected('имя переменной')
        gen_addr(x)
        next_lex()


def st_proc(sp):
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
    t = t_type()
    expression(t)
    if t != 'typBool':
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