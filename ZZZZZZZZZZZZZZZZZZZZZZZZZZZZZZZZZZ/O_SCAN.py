# Сканер

from O_TEST import *
from O_GEN import *
from O_TEXT import *

# Константы
NameLen = 31
KWNum = 34
chSpace = ' '
chTab = '\t'
chEOL = '\n'
chEOT = '\0'
nkw = 0
KWTable = []


lexNone, lexName, lexNum, lexMODULE, lexIMPORT, lexBEGIN, lexEND, \
lexCONST, lexVAR, lexWHILE, lexDO, lexIF, lexTHEN, lexELSIF, lexELSE, \
lexMult, lexDIV, lexMOD, lexPlus, lexMinus, lexEQ, lexNE, lexLT, \
lexLE, lexGT, lexGE, lexDot, lexComma, lexColon, lexSemi, \
lexAss, lexLpar, lexRpar, lexEOT, lexFCK = range(35)


# Процедура для ввода ключевых слов
def enter_kw(name, lex):
    global nkw, KWTable
    nkw += 1
    KWTable.append({'Word': name, 'Lex': lex})


# Функция для тестирования ключевых слов
def test_kw():
    global nkw, KWTable, Name
    i = nkw
    while i > 0 and Name != KWTable[i - 1]['Word']:
        i -= 1
    return KWTable[i - 1]['Lex'] if i > 0 else 'lexName'


# Процедура для идентификаторов
def ident():
    global Name, Lex
    i = 0
    Name = ''
    while True:
        if i < NameLen:
            i += 1
            Name += ch
        else:
            error('Слишком длинное имя')
        next_ch()
        if not ch.isalnum():
            break
    Lex = test_kw()  # Проверка на ключевое слово


# Процедура для чисел
def number():
    global Lex, Num
    Lex = 'lexNum'
    Num = 0
    while True:
        d = ord(ch) - ord('0')
        if (MaxInt - d) // 10 >= Num:
            Num = 10 * Num + d
        else:
            error('Слишком большое число')
        next_ch()
        if not ch.isdigit():
            break


# Процедура для комментариев
def comment():
    global Pos, LexPos
    next_ch()
    while True:
        while ch != '*' and ch != chEOT:
            if ch == '(':
                next_ch()
                if ch == '*':
                    comment()
            else:
                next_ch()
        if ch == '*':
            next_ch()
        if ch in [')', chEOT]:
            break
    if ch == ')':
        next_ch()
    else:
        LexPos = Pos
        error('Не закончен комментарий')


def next_lex():
    global Ch, LexPos, Pos, Lex, otest_table
    while Ch in [chSpace, chTab, chEOL]:
        next_ch()
    LexPos = Pos
    add_to_OTEST_table(otest_table, Lex)
    if Ch.isalpha():
        ident()
    elif Ch.isdigit():
        number()
    elif Ch == ';':
        next_ch()
        Lex = lexSemi
    elif Ch == ':':
        next_ch()
        if Ch == '=':
            next_ch()
            Lex = lexAss
        else:
            Lex = lexColon
    elif Ch == '.':
        next_ch()
        Lex = lexDot
    elif Ch == ',':
        next_ch()
        Lex = lexComma
    elif Ch == '=':
        next_ch()
        Lex = lexEQ
    elif Ch == '#':
        next_ch()
        Lex = lexNE
    elif Ch == '<':
        next_ch()
        if Ch == '=':
            next_ch()
            Lex = lexLE
        else:
            Lex = lexLT
    elif Ch == '>':
        next_ch()
        if Ch == '=':
            next_ch()
            Lex = lexGE
        else:
            Lex = lexGT
    elif Ch == '(':
        next_ch()
        if Ch == '*':
            comment()
            next_lex()
        else:
            Lex = lexLpar
    elif Ch == ')':
        next_ch()
        Lex = lexRpar
    elif Ch == '+':
        next_ch()
        Lex = lexPlus
    elif Ch == '-':
        next_ch()
        Lex = lexMinus
    elif Ch == '*':
        next_ch()
        Lex = lexMult
    elif Ch == chEOT:
        Lex = lexEOT
    else:
        error('Недопустимый символ')
    add_to_OTEST_table(otest_table, Lex)


def init_scan():
    global nkw, KWTable
    nkw = 0

# Добавление ключевых слов в таблицу
enter_kw('ARRAY',     lexNone)
enter_kw('BY',        lexNone)
enter_kw('BEGIN',     lexBEGIN)
enter_kw('CASE',      lexNone)
enter_kw('CONST',     lexCONST)
enter_kw('DIV',       lexDIV)
enter_kw('DO',        lexDO)
enter_kw('ELSE',      lexELSE)
enter_kw('ELSIF',     lexELSIF)
enter_kw('END',       lexEND)
enter_kw('EXIT',      lexNone)
enter_kw('FOR',       lexNone)
enter_kw('IF',        lexIF)
enter_kw('IMPORT',    lexIMPORT)
enter_kw('IN',        lexNone)
enter_kw('IS',        lexNone)
enter_kw('LOOP',      lexNone)
enter_kw('MOD',       lexMOD)
enter_kw('MODULE',    lexMODULE)
enter_kw('NIL',       lexNone)
enter_kw('OF',        lexNone)
enter_kw('OR',        lexNone)
enter_kw('POINTER',   lexNone)
enter_kw('PROCEDURE', lexNone)
enter_kw('RECORD',    lexNone)
enter_kw('REPEAT',    lexNone)
enter_kw('RETURN',    lexNone)
enter_kw('THEN',      lexTHEN)
enter_kw('TO',        lexNone)
enter_kw('TYPE',      lexNone)
enter_kw('UNTIL',     lexNone)
enter_kw('VAR',       lexVAR)
enter_kw('WHILE',     lexWHILE)
enter_kw('WITH',      lexNone)

# Вызов функции next_lex для начала сканирования
next_lex()
