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

def nextChar():
    global c
    c = Text.nextChar()

def init(fileName):
    Text.init(fileName)
    nextChar()

def scanName():
    assert 'A' <= c <= 'Z' or 'a' <= c <= 'z'
    global name
    name = c
    nextChar()
    while 'A' <= c <= 'Z' or 'a' <= c <= 'z' or '0' <= c <= '9':
        name += c
        nextChar()
    if name in KEYWORDS:
        return KEYWORDS[name]
    else:
        return Lex.NAME

def scanNumber():
    assert '0' <= c <= '9'
    global value
    value = ord(c) - ord('0')
    nextChar()
    while '0' <= c <= '9':
        d = ord(c) - ord('0')
        value = value * 10 + d
        if value > MAXINT:
            error(f'слишком большое число, максимум {MAXINT}')
        nextChar()
    return Lex.NUMBER

def skipComment():
    while True:
        if c == chEOT:
            error('неожиданный конец комментария')
        elif c == '*':
            nextChar()
            if c == ')':
                nextChar()
                return
        elif c == '(':
            nextChar()
            if c == '*':
                nextChar()
                skipComment()
        else:
            nextChar()

def nextLex():
    while c in (' ', '\t', '\r', '\n'):
        nextChar()
    global lexPos
    lexPos = Text.pos
    if 'A' <= c <= 'Z' or 'a' <= c <= 'z':
        return scanName()
    elif '0' <= c <= '9':
        return scanNumber()
    elif c == ';':
        nextChar()
        return Lex.SEMICOLON
    elif c == ':':
        nextChar()
        if c == '=':
            nextChar()
            return Lex.ASSIGN
        else:
            return Lex.COLON
    elif c == ',':
        nextChar()
        return Lex.COMMA
    elif c == '(':
        nextChar()
        if c == '*':
            nextChar()
            skipComment()
            return nextLex()
        else:
            return Lex.LPAR
    elif c == ')':
        nextChar()
        return Lex.RPAR
    elif c == '.':
        nextChar()
        return Lex.DOT
    elif c == '+':
        nextChar()
        return Lex.PLUS
    elif c == '-':
        nextChar()
        return Lex.MINUS
    elif c == '*':
        nextChar()
        return Lex.MULTIPLY
    elif c == '=':
        nextChar()
        return Lex.EQ
    elif c == '#':
        nextChar()
        return Lex.NE
    elif c == '<':
        nextChar()
        if c == '=':
            nextChar()
            return Lex.LE
        else:
            return Lex.LT
    elif c == '>':
        nextChar()
        if c == '=':
            nextChar()
            return Lex.GE
        else:
            return Lex.GT
    elif c == chEOT:
        return Lex.EOT
    else:
        error('недопустимый символ')