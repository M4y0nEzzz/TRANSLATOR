import Text
from Text import error, chEOT
from Lexemes import Lex

MAXINT=(2**31)-1

#Ключевые слова Оберона-2
KEYWORDS={
    'ARRAY': Lex.NONE,
    'BEGIN': Lex.BEGIN,
    'BY': Lex.NONE,
    'CASE': Lex.NONE,
    'CONST': Lex.CONST,
    'DIV': Lex.DIV,
    'DO': Lex.DO,
    'ELSE': Lex.ELSE,
    'ELSIF': Lex.ELSIF,
    'END': Lex.END,
    'EXIT': Lex.NONE,
    'FOR': Lex.NONE,
    'IF': Lex.IF,
    'IMPORT': Lex.IMPORT,
    'IN': Lex.NONE,
    'IS': Lex.NONE,
    'LOOP': Lex.NONE,
    'MOD': Lex.MOD,
    'MODULE': Lex.MODULE,
    'NIL': Lex.NONE,
    'OF': Lex.NONE,
    'OR': Lex.NONE,
    'POINTER': Lex.NONE,
    'PROCEDURE': Lex.NONE,
    'RECORD': Lex.NONE,
    'REPEAT': Lex.NONE,
    'RETURN': Lex.NONE,
    'THEN': Lex.THEN,
    'TO': Lex.NONE,
    'TYPE': Lex.NONE,
    'UNTIL': Lex.NONE,
    'VAR': Lex.VAR,
    'WHILE': Lex.WHILE,
    'WITH': Lex.NONE
}
lexPos = -1
name = ''
value = -1


def next_ch():
    global ch
    ch = Text.next_ch()


def init(fileName):
    Text.init(fileName)
    next_ch()


def scanName():
    assert 'A' <= ch <= 'Z' or 'a' <= ch <= 'z'
    global name
    name = ch
    next_ch()
    while 'A' <= ch <= 'Z' or 'a' <= ch <= 'z' or '0' <= ch <= '9':
        name += ch
        next_ch()
    if name in KEYWORDS:
        return KEYWORDS[name]
    else:
        return Lex.NAME


def scanNumber():
    assert '0' <= ch <= '9'
    global value
    value = ord(ch) - ord('0')
    next_ch()
    while '0' <= ch <= '9':
        d = ord(ch) - ord('0')
        value = value * 10 + d
        if value > MAXINT:
            error(f'слишком большое число, максимум {MAXINT}')
        next_ch()
    return Lex.NUMBER


def skipComment():
    while True:
        if ch == chEOT:
            error('неожиданный конец комментария')
        elif ch== '*':
            next_ch()
            if ch == ')':
                next_ch()
                return
        elif ch == '(':
            next_ch()
            if ch == '*':
                next_ch()
                skipComment()
        else:
            next_ch()


def nextLex():
    while ch in (' ', '\t', '\r', '\n'):
        next_ch()
    global lexPos
    lexPos = Text.pos
    if 'A' <= ch <= 'Z' or 'a' <= ch <= 'z':
        return scanName()
    elif '0' <= ch <= '9':
        return scanNumber()
    elif ch == ';':
        next_ch()
        return Lex.SEMICOLON
    elif ch == ':':
        next_ch()
        if ch == '=':
            next_ch()
            return Lex.ASSIGN
        else:
            return Lex.COLON
    elif ch == ',':
        next_ch()
        return Lex.COMMA
    elif ch == '(':
        next_ch()
        if ch == '*':
            next_ch()
            skipComment()
            return nextLex()
        else:
            return Lex.LPAR
    elif ch == ')':
        next_ch()
        return Lex.RPAR
    elif ch == '.':
        next_ch()
        return Lex.DOT
    elif ch == '+':
        next_ch()
        return Lex.PLUS
    elif ch == '-':
        next_ch()
        return Lex.MINUS
    elif ch == '*':
        next_ch()
        return Lex.MULTIPLY
    elif ch == '=':
        next_ch()
        return Lex.EQ
    elif ch == '#':
        next_ch()
        return Lex.NE
    elif ch == '<':
        next_ch()
        if ch == '=':
            next_ch()
            return Lex.LE
        else:
            return Lex.LT
    elif ch == '>':
        next_ch()
        if ch == '=':
            next_ch()
            return Lex.GE
        else:
            return Lex.GT
    elif ch == chEOT:
        return Lex.EOT
    else:
        error('недопустимый символ')