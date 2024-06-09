from enum import Enum

class Kind(Enum):
    STANDARD_FUNCTION, STANDARD_PROCEDURE, TYPE, CURRENT_MODULE_NAME, \
    IMPORTED_MODULE_NAME, VAR, CONST_EXPR, TYPE_NAME, GENERAL_EXPR, CONST, UNDEFINED_CONST = range(11)

class BuiltIn(Enum):
    ABS, DEC, HALT, INC, MAX, MIN, ODD, INTEGER, IN_OPEN, IN_INT, OUT_INT, OUT_LN, BOOLEAN = range(13)

table = []

keywordC = ['and', 'break', 'do', 'else', 'elseif', 'end',
            'false', 'for', 'function', 'goto', 'if', 'in', 'local',
            'nil', 'not', 'or', 'repeat', 'return',
            'then', 'true', 'until', 'while']

def openScope():
    table.append({})

def closeScope():
    table.pop()

class NameAlreadyDefined(Exception): pass

def add(name, obj):
    if name in table[-1]:
        raise NameAlreadyDefined()
    table[-1][name] = obj

class NameNotFound(Exception): pass

def find(name):
    for scope in reversed(table):
        if name in scope:
            return scope[name]
    raise NameNotFound()