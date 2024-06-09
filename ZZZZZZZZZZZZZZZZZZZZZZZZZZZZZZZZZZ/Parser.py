import Scanner
from Lexemes import Lex, lexToStr
from Text import error
import Table
from Table import Kind
from Table import BuiltIn
from Table import keywordC

cText = ''
tab = '   '
importModule = set()
isOdd = False
isDiv = False
isMod = False
isSemicolonAndNewLine = True
isSemicolon = True
uni = 0

def convert(convertLex):
    global cText
    cText += convertLex

def nextLex():
    global lex, lexPos
    lex = Scanner.nextLex()
    lexPos = Scanner.lexPos

def skip(need):
    if lex == need:
        nextLex()
    else:
        error('ожидается ' + lexToStr[need], lexPos)

def skipName(description):
    if lex == Lex.NAME:
        name = Scanner.name
        nextLex()
        return name
    else:
        error('ожидается ' + description, lexPos)

'''
factor = ident ["(" expression ")"] | number | "(" expression ")".
'''
def factor():
    global isOdd, isMod, importModule
    if lex == Lex.NAME:
        namePos = lexPos
        name = Scanner.name
        nextLex()
        try:
            obj = Table.find(name)
        except Table.NameNotFound:
            error(f'имя {name} не найдено', namePos)
        if lex == Lex.LPAR:
            nextLex()
            exprPos = lexPos
            if obj['kind'] != Kind.STANDARD_FUNCTION:
                error(f'имя {name} принадлежит не функции', namePos)

            if obj['id'] == BuiltIn.ABS:
                convert('abs(')
                importModule.add('<stdlib.h>')
            elif obj['id'] == BuiltIn.ODD:
                convert('isOdd(')
                importModule.add('<stdbool.h>')
                isMod = True
                isOdd = True
            argKind, argType = expression()

            assert argKind in (Kind.VAR, Kind.CONST_EXPR, Kind.TYPE_NAME, Kind.GENERAL_EXPR)
            assert argType in (BuiltIn.INTEGER, BuiltIn.BOOLEAN)

            skip(Lex.RPAR)

            if obj['id'] == BuiltIn.ABS:
                if argKind == Kind.CONST_EXPR and argType == BuiltIn.INTEGER:
                    return Kind.CONST_EXPR, BuiltIn.INTEGER
                elif argKind in (Kind.VAR, Kind.GENERAL_EXPR) and argType == BuiltIn.INTEGER:
                    return Kind.GENERAL_EXPR, BuiltIn.INTEGER
                else:
                    error('недопустимый аргумент функции ABS - ожидается целочисленное выражение', exprPos)
                convert(')')
            elif obj['id'] == BuiltIn.MAX:
                convert('INT_MAX')
                importModule.add('<limits.h>')
                if argKind == Kind.TYPE_NAME and argType == BuiltIn.INTEGER:
                    return Kind.CONST_EXPR, BuiltIn.INTEGER
                else:
                    error('недопустимый аргумент функции MAX - ожидается имя целочисленного типа', exprPos)
            elif obj['id'] == BuiltIn.MIN:
                convert('INT_MIN')
                importModule.add('<limits.h>')
                if argKind == Kind.TYPE_NAME and argType == BuiltIn.INTEGER:
                    return Kind.CONST_EXPR, BuiltIn.INTEGER
                else:
                    error('недопустимый аргумент функции MIN - ожидается имя целочисленного типа', exprPos)
            else:
                assert obj['id'] == BuiltIn.ODD
                convert(')')
                if argKind in (Kind.VAR, Kind.CONST_EXPR, Kind.GENERAL_EXPR) and argType == BuiltIn.INTEGER:
                    return Kind.GENERAL_EXPR, BuiltIn.BOOLEAN
                else:
                    error('недопустимый аргумент функции ODD - ожидается целочисленное выражение', exprPos)
            assert False
        else:
            # просто имя
            if obj['kind'] == Kind.TYPE and obj['id'] == BuiltIn.INTEGER:
                return Kind.TYPE_NAME, BuiltIn.INTEGER
            elif obj['kind'] == Kind.VAR:
                assert obj['type'] == BuiltIn.INTEGER
                if name in keywordC:
                    convert('_' + name)
                else:
                    convert(name)
                return Kind.VAR, BuiltIn.INTEGER
            elif obj['kind'] == Kind.CONST:
                assert obj['type'] == BuiltIn.INTEGER
                if name in keywordC:
                    convert('_' + name)
                else:
                    convert(name)
                return Kind.CONST_EXPR, BuiltIn.INTEGER
            elif obj['kind'] == Kind.UNDEFINED_CONST:
                error('константа ещё не определена', namePos)
            else:
                error('ожидается имя переменной, константы или типа', namePos)
    elif lex == Lex.NUMBER:
        nextLex()
        value = Scanner.value
        convert(str(value))
        return Kind.CONST_EXPR, BuiltIn.INTEGER
    else:
        openPos = lexPos
        skip(Lex.LPAR)
        convert('(')
        kind, type = expression()

        assert kind in (Kind.VAR, Kind.CONST_EXPR, Kind.TYPE_NAME, Kind.GENERAL_EXPR)
        assert type in (BuiltIn.INTEGER, BuiltIn.BOOLEAN)

        if kind == Kind.TYPE_NAME:
            error('имя типа нельзя заключать в дополнительные скобки', openPos)

        skip(Lex.RPAR)
        convert(')')

        if kind == Kind.VAR:
            kind = Kind.GENERAL_EXPR

        return kind, type

'''
term = factor {MulOperator factor}.
MulOperator = "*"|DIV|MOD.
'''
def term():
    global cText, importModule, isDiv, isMod
    convert('{')
    figScSt = cText.rfind('{')
    isFigScSt = True
    kind1, type1 = factor()

    assert kind1 in (Kind.VAR, Kind.CONST_EXPR, Kind.TYPE_NAME, Kind.GENERAL_EXPR)
    assert type1 in (BuiltIn.INTEGER, BuiltIn.BOOLEAN)

    delen = False
    delenCol = 0
    while lex in (Lex.MULTIPLY, Lex.DIV, Lex.MOD):
        if lex == Lex.MULTIPLY:
            convert(' * ')
            cText = cText[:-(len(cText) - figScSt)] + cText[figScSt:]
        elif lex == Lex.DIV:
            cTextleft = cText[:-(len(cText) - figScSt)]
            cText = cTextleft + 'DIV(' + cText[figScSt:] + ', '
            isDiv = True
            isMod = True
            delen = True
        else:
            cTextleft = cText[:-(len(cText) - figScSt)]
            cText = cTextleft + 'MOD(' + cText[figScSt:] + ', '
            isMod = True
            delen = True
        binaryPos = lexPos
        nextLex()
        kind2, type2 = factor()
        if delen:
            convert(')')
        delen = False
        assert kind2 in (Kind.VAR, Kind.CONST_EXPR, Kind.TYPE_NAME, Kind.GENERAL_EXPR)
        assert type2 in (BuiltIn.INTEGER, BuiltIn.BOOLEAN)

        if kind1 == kind2 == Kind.CONST_EXPR and type1 == type2 == BuiltIn.INTEGER:
            pass
            # result: kind1 == Kind.CONST_EXPR, type1 == BuiltIn.INTEGER
        elif (
            kind1 in (Kind.VAR, Kind.CONST_EXPR, Kind.GENERAL_EXPR) and
            kind2 in (Kind.VAR, Kind.CONST_EXPR, Kind.GENERAL_EXPR) and
            type1 == type2 == BuiltIn.INTEGER
        ):
            kind1 = Kind.GENERAL_EXPR
            # type1 == BuiltIn.INTEGER
        else:
            error('недопустимые типы операндов - ожидается два целочисленных выражения', binaryPos)
    convert(')'*delenCol)
    if isFigScSt:
        figSc = cText.rfind('{')
        cText = cText[:-(len(cText) - figSc)] + cText[figSc+1:]
    return kind1, type1

'''
SimpleExpression = ["+"|"-"] term {AddOperator term}.
AddOperator = "+"|"-".
'''
def simpleExpression():
    wasUnary = False
    if lex in (Lex.PLUS, Lex.MINUS):
        unaryPos = lexPos
        if lex == lex.PLUS:
            convert('+')
        else:
            convert('-')
        nextLex()
        wasUnary = True

    kind1, type1 = term()

    assert kind1 in (Kind.VAR, Kind.CONST_EXPR, Kind.TYPE_NAME, Kind.GENERAL_EXPR)
    assert type1 in (BuiltIn.INTEGER, BuiltIn.BOOLEAN)

    if wasUnary:
        if kind1 == Kind.VAR and type1 == BuiltIn.INTEGER:
            kind1 = Kind.GENERAL_EXPR
        elif kind1 in (Kind.CONST_EXPR, Kind.GENERAL_EXPR) and type1 == BuiltIn.INTEGER:
            pass # ok
        else:
            error('унарный плюс и минус применимы только к значениям целого типа', unaryPos)

    while lex in (Lex.PLUS, Lex.MINUS):
        binaryPos = lexPos
        if lex == lex.PLUS:
            convert(' + ')
        else:
            convert(' - ')
        nextLex()
        kind2, type2 = term()

        assert kind2 in (Kind.VAR, Kind.CONST_EXPR, Kind.TYPE_NAME, Kind.GENERAL_EXPR)
        assert type2 in (BuiltIn.INTEGER, BuiltIn.BOOLEAN)

        if kind1 == kind2 == Kind.CONST_EXPR and type1 == type2 == BuiltIn.INTEGER:
            pass
            # result: kind1 == Kind.CONST_EXPR, type1 == BuiltIn.INTEGER
        elif (
            kind1 in (Kind.VAR, Kind.CONST_EXPR, Kind.GENERAL_EXPR) and
            kind2 in (Kind.VAR, Kind.CONST_EXPR, Kind.GENERAL_EXPR) and
            type1 == type2 == BuiltIn.INTEGER
        ):
            kind1 = Kind.GENERAL_EXPR
            # type1 == BuiltIn.INTEGER
        else:
            error('недопустимые типы операндов - ожидается два целочисленных выражения', binaryPos)

    return kind1, type1

'''
expression = SimpleExpression [relation SimpleExpression].
relation = "=" | "#" | "<" | "<=" | ">" | ">=".
'''
def expression():
    kind1, type1 = simpleExpression()
    if lex in (Lex.EQ, Lex.NE, Lex.LT, Lex.LE, Lex.GT, Lex.GE):
        comparisonPos = lexPos
        if lexToStr[lex][1: -1] == '#':
            convert(' != ')
        elif lexToStr[lex][1: -1] == '=':
            convert(' == ')
        else:
            convert(' ' + lexToStr[lex][1: -1] + ' ')
        nextLex()
        kind2, type2 = simpleExpression()
        if (
            kind1 in (Kind.VAR, Kind.CONST_EXPR, Kind.GENERAL_EXPR) and
            kind2 in (Kind.VAR, Kind.CONST_EXPR, Kind.GENERAL_EXPR) and
            type1 == type2 == BuiltIn.INTEGER
        ):
            return Kind.GENERAL_EXPR, BuiltIn.BOOLEAN
        else:
            error('недопустимые типы операндов - ожидается два целочисленных выражения', comparisonPos)
    return kind1, type1

def intExpression():
    exprPos = lexPos

    kind, type = expression()

    assert kind in (Kind.VAR, Kind.CONST_EXPR, Kind.TYPE_NAME, Kind.GENERAL_EXPR)
    assert type in (BuiltIn.INTEGER, BuiltIn.BOOLEAN)

    if not (kind in (Kind.VAR, Kind.CONST_EXPR, Kind.GENERAL_EXPR) and type == BuiltIn.INTEGER):
        error('ожидается целочисленное выражение', exprPos)

def boolExpression():
    exprPos = lexPos

    kind, type = expression()

    assert kind in (Kind.VAR, Kind.CONST_EXPR, Kind.TYPE_NAME, Kind.GENERAL_EXPR)
    assert type in (BuiltIn.INTEGER, BuiltIn.BOOLEAN)

    if not (kind in (Kind.VAR, Kind.CONST_EXPR, Kind.GENERAL_EXPR) and type == BuiltIn.BOOLEAN):
        error('ожидается логическое выражение', exprPos)

def intVariable():
    exprPos = lexPos

    kind, type = expression()

    assert kind in (Kind.VAR, Kind.CONST_EXPR, Kind.TYPE_NAME, Kind.GENERAL_EXPR)
    assert type in (BuiltIn.INTEGER, BuiltIn.BOOLEAN)

    if not (kind == Kind.VAR and type == BuiltIn.INTEGER):
        error('ожидается целочисленная переменная', exprPos)

def procedureCallArguments(procId):
    global tab, cText
    global importModule, isSemicolonAndNewLine
    if procId == BuiltIn.HALT:
        skip(Lex.LPAR)
        convert('exit(')
        intExpression()
        skip(Lex.RPAR)
        convert(')')
        importModule.add('<stdlib.h>')
    elif procId == BuiltIn.INC:
        skip(Lex.LPAR)
        intVariable()
        convert('+')
        if lex == Lex.COMMA:
            convert('=')
            nextLex()
            intExpression()
        else:
            convert('+')
        skip(Lex.RPAR)
    elif procId == BuiltIn.DEC:
        skip(Lex.LPAR)
        intVariable()
        convert('-')
        if lex == Lex.COMMA:
            convert('=')
            nextLex()
            intExpression()
        else:
            convert('-')
        skip(Lex.RPAR)
    elif procId == BuiltIn.IN_OPEN:
        skip(Lex.LPAR)
        skip(Lex.RPAR)
        cText = cText[:-len(tab)]
        isSemicolonAndNewLine = False
    elif procId == BuiltIn.IN_INT:
        skip(Lex.LPAR)
        convert('scanf("%d", &')
        intVariable()
        skip(Lex.RPAR)
        convert(')')
    elif procId == BuiltIn.OUT_INT:
        skip(Lex.LPAR)
        convert('printf(\"%*d\", \"')
        intExpression()
        otstupStartPos = cText.rfind('\"')
        otstupExpr = cText[otstupStartPos + 1:]
        cText = cText[:-(len(cText) - otstupStartPos)]
        skip(Lex.COMMA)
        intExpression()
        convert(', ' + otstupExpr)
        skip(Lex.RPAR)
        convert(')')
    else:
        assert procId == BuiltIn.OUT_LN
        skip(Lex.LPAR)
        skip(Lex.RPAR)
        convert('printf("\\n")')

'''
statement = [
    ident ":=" expression
    |[ident "."] ident "(" [expression {"," expression}] ")"
    |IF expression THEN
        StatementSequence
    {ELSIF expression THEN
        StatementSequence}
    [ELSE StatementSequence]
    END
    |WHILE expression DO
        StatementSequence
    END
].
'''
def statement(colTab):
    global tab, cText, isSemicolon
    convert(tab*colTab)
    if lex == Lex.NAME:
        name = Scanner.name
        namePos = lexPos
        nextLex()
        try:
            obj = Table.find(name)
        except Table.NameNotFound:
            error(f'имя {name} не найдено', namePos)
        if lex == Lex.ASSIGN:
            if name in keywordC:
                convert('_' + name + ' = ')
            else:
                convert(name + ' = ')
            nextLex()
            if not (obj['kind'] == Kind.VAR):
                error('ожидается имя переменной', namePos)
            assert obj['type'] == BuiltIn.INTEGER
            intExpression()
        else:
            # ProcedureCall
            if lex == Lex.DOT:
                nextLex()
                if obj['kind'] != Kind.IMPORTED_MODULE_NAME:
                    error('ожидается имя модуля', namePos)
                moduleName = name
                table = obj['table']
                namePos = lexPos
                procName = skipName('имя процедуры')
                if procName in table:
                    assert table[procName]['kind'] == Kind.STANDARD_PROCEDURE
                    procId = table[procName]['id']
                else:
                    error(f'имя {procName} не найдено в модуле {name}', namePos)
            else:
                if obj['kind'] != Kind.STANDARD_PROCEDURE:
                    error('ожидается имя процедуры', namePos)
                procId = obj['id']
            procedureCallArguments(procId)
    elif lex == Lex.IF:
        convert('if ')
        nextLex()
        convert('(')
        boolExpression()
        convert(')')
        skip(Lex.THEN)
        convert(' {\n')
        statementSequence(colTab+1)
        while lex == Lex.ELSIF:
            cText = cText[:-len(tab)]
            convert('} else if ')
            nextLex()
            convert('(')
            boolExpression()
            convert(')')
            skip(Lex.THEN)
            convert(' {\n')
            statementSequence(colTab + 1)
        if lex == Lex.ELSE:
            cText = cText[:-len(tab)]
            convert('} else {\n')
            nextLex()
            statementSequence(colTab + 1)
        skip(Lex.END)
        cText = cText[:-len(tab)]
        convert('}')
        isSemicolon = False
    elif lex == Lex.WHILE:
        convert('while ')
        nextLex()
        convert('(')
        boolExpression()
        convert(')')
        skip(Lex.DO)
        convert(' {\n')
        statementSequence(colTab + 1)
        skip(Lex.END)
        cText = cText[:-len(tab)]
        convert('}')
        isSemicolon = False

'''
StatementSequence = statement {statement }.
'''
def statementSequence(colTab):
    global isSemicolon, isSemicolonAndNewLine
    statement(colTab)
    while lex == Lex.SEMICOLON:
        if not isSemicolon:
            convert('\n')
            isSemicolon = True
        elif isSemicolonAndNewLine:
            convert('\n')
        else:
            isSemicolonAndNewLine = True

        nextLex()
        statement(colTab)

'''
VariableDeclaration = ident {"," ident} ":" type.
type = ident.
'''
def variableDeclaration():
    vars = []
    while True:
        namePos = lexPos
        name = skipName('имя переменной')
        if name in keywordC:
            convert('_' + name)
        else:
            convert(name)
        try:
            varObj = {'kind': Kind.VAR}
            vars.append(varObj)
            Table.add(name, varObj)
        except Table.NameAlreadyDefined:
            error(f'имя {name} уже определено', namePos)
        if lex == Lex.COMMA:
            convert(', ')
            nextLex()
        else:
            break
    skip(Lex.COLON)
    namePos = lexPos
    name = skipName('имя типа')
    try:
        typeObj = Table.find(name)
    except Table.NameNotFound:
        error(f'имя {name} не найдено', namePos)
    if typeObj['kind'] != Kind.TYPE:
        error(f'имя {name} принадлежит не типу', namePos)
    assert typeObj['id'] == BuiltIn.INTEGER
    for var in vars:
        var['type'] = typeObj['id']

'''
ConstDeclaration = ident "=" ConstExpression.
ConstExpression = expression.
'''
def constDeclaration():
    namePos = lexPos
    name = skipName('имя константы')
    if name in keywordC:
        convert('_' + name)
    else:
        convert(name)
    try:
        constObj = {'kind': Kind.UNDEFINED_CONST}
        Table.add(name, constObj)
    except Table.NameAlreadyDefined:
        error(f'имя {name} уже определено', namePos)

    skip(Lex.EQ)
    convert(' = ')

    exprPos = lexPos
    kind, type = expression()

    assert kind in (Kind.VAR, Kind.CONST_EXPR, Kind.TYPE_NAME, Kind.GENERAL_EXPR)
    assert type in (BuiltIn.INTEGER, BuiltIn.BOOLEAN)

    if kind == Kind.CONST_EXPR and type == BuiltIn.INTEGER:
        constObj['kind'] = Kind.CONST
        constObj['type'] = BuiltIn.INTEGER
    else:
        error('ожидается целочисленное константное выражение', exprPos)

'''
DeclarationSequence = {CONST {ConstDeclaration} | VAR {VariableDeclaration}}.
'''
def declarationSequence():
    while True:
        if lex == Lex.CONST:
            nextLex()
            while lex == Lex.NAME:
                convert('const local ')
                constDeclaration()
                skip(Lex.SEMICOLON)
                convert('\n')
        elif lex == Lex.VAR:
            nextLex()
            while lex == Lex.NAME:
                convert('local ')
                variableDeclaration()
                skip(Lex.SEMICOLON)
                convert('\n')
        else:
            break

'''
ImportList = IMPORT ident {"," ident}.
'''
def importList():
    global importModule
    skip(Lex.IMPORT)
    while True:
        namePos = lexPos
        name = skipName('имя модуля')
        try:
            if name == 'In':
                inTable = {}
                inTable['Open'] = {'kind': Kind.STANDARD_PROCEDURE, 'id': BuiltIn.IN_OPEN}
                inTable['Int'] = {'kind': Kind.STANDARD_PROCEDURE, 'id': BuiltIn.IN_INT}
                Table.add('In', {'kind': Kind.IMPORTED_MODULE_NAME, 'table': inTable})
            elif name == 'Out':
                outTable = {}
                outTable['Int'] = {'kind': Kind.STANDARD_PROCEDURE, 'id': BuiltIn.OUT_INT}
                outTable['Ln'] = {'kind': Kind.STANDARD_PROCEDURE, 'id': BuiltIn.OUT_LN}
                Table.add('Out', {'kind': Kind.IMPORTED_MODULE_NAME, 'table': outTable})
            else:
                error('доступны для импорта только модули In и Out', namePos)
        except Table.NameAlreadyDefined:
            error(f'имя {name} уже определено', namePos)

        if lex == Lex.COMMA:
            nextLex()
        else:
            break
    skip(Lex.SEMICOLON)
    importModule.add("'In', 'Out'")

'''
Module = MODULE ident [ImportList] DeclarationSequence [BEGIN StatementSequence] END ident ".".
Модуль =
    MODULE Имя
    [Импорт]
    ПослОбъявл
    [BEGIN
        ПослОператоров]
    END Имя ".".
'''
def module():
    global tab, cText
    skip(Lex.MODULE)
    moduleName = skipName('имя модуля')
    Table.openScope()
    Table.add(moduleName, {'kind': Kind.CURRENT_MODULE_NAME})
    skip(Lex.SEMICOLON)
    Table.openScope()
    if lex == Lex.IMPORT:
        importList()
    declarationSequence()
    if lex == Lex.BEGIN:
        nextLex()
        statementSequence(1)
    Table.closeScope()
    skip(Lex.END)
    closingNamePos = lexPos
    closingName = skipName('имя модуля')
    if closingName != moduleName:
        error(f'ожидается {moduleName}', closingNamePos)
    skip(Lex.DOT)
    cText = cText[:-len(tab)]
    convert('}')
    Table.closeScope()

def addNameConvertModelesAndisOdd():
    global cText, importModule
    for moduleName in importModule:
        cText = 'require (' + moduleName + ')' +'\n' + cText

def parse(filename):
    Table.openScope()

    Table.add('ABS', {'kind': Kind.STANDARD_FUNCTION, 'id': BuiltIn.ABS})
    Table.add('MIN', {'kind': Kind.STANDARD_FUNCTION, 'id': BuiltIn.MIN})
    Table.add('MAX', {'kind': Kind.STANDARD_FUNCTION, 'id': BuiltIn.MAX})
    Table.add('ODD', {'kind': Kind.STANDARD_FUNCTION, 'id': BuiltIn.ODD})

    Table.add('HALT', {'kind': Kind.STANDARD_PROCEDURE, 'id': BuiltIn.HALT})
    Table.add('INC', {'kind': Kind.STANDARD_PROCEDURE, 'id': BuiltIn.INC})
    Table.add('DEC', {'kind': Kind.STANDARD_PROCEDURE, 'id': BuiltIn.DEC})

    Table.add('INTEGER', {'kind': Kind.TYPE, 'id': BuiltIn.INTEGER})

    Scanner.init(filename)
    nextLex()
    module()
    skip(Lex.EOT)
    addNameConvertModelesAndisOdd()
    Table.closeScope()

    convertC = open(filename[:-1] + 'c', 'w')
    convertC.write(cText)
    convertC.close()