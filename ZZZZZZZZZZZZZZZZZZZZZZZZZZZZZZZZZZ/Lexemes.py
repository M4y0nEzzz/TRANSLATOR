from enum import Enum

class Lex(Enum):
    NAME, NUMBER, SEMICOLON, ASSIGN, COLON, COMMA, LPAR, RPAR, DOT, PLUS, MINUS, \
    MULTIPLY, EQ, NE, LE, LT, GE, GT, BEGIN, CONST, DIV, DO, ELSE, ELSIF, \
    END, IF, IMPORT, MOD, MODULE, THEN, VAR, WHILE, NONE, EOT = range(34)

lexToStr = {
    Lex.NAME: 'имя',
    Lex.NUMBER: 'число',
    Lex.SEMICOLON: '";"',
    Lex.ASSIGN: '":="',
    Lex.COLON: '":"',
    Lex.COMMA: '","',
    Lex.LPAR: '"("',
    Lex.RPAR: '")"',
    Lex.DOT: '"."',
    Lex.PLUS: '"+"',
    Lex.MINUS: '"-"',
    Lex.MULTIPLY: '"*"',
    Lex.EQ: '"="',
    Lex.NE: '"#"',
    Lex.LE: '"<="',
    Lex.LT: '"<"',
    Lex.GE: '">="',
    Lex.GT: '">"',
    Lex.BEGIN: 'BEGIN',
    Lex.CONST: 'CONST',
    Lex.DIV: 'DIV',
    Lex.DO: 'DO',
    Lex.ELSE: 'ELSE',
    Lex.ELSIF: 'ELSIF',
    Lex.END: 'END',
    Lex.IF: 'IF',
    Lex.IMPORT: 'IMPORT',
    Lex.MOD: 'MOD',
    Lex.MODULE: 'MODULE',
    Lex.THEN: 'THEN',
    Lex.VAR: 'VAR',
    Lex.WHILE: 'WHILE',
    Lex.NONE: '(зарезервированное слово языка Оберон-2)',
    Lex.EOT: 'конец текста'
}