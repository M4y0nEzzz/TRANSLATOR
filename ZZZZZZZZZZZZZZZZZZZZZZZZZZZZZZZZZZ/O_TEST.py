# Тестовый модуль

from O_SCAN import *
from O_TEXT import *
import sys


# Константы
keywords_pasc = 0
n_kwp = 0
OLEX_COUNT = 1000
TAB = '   '
Name = ''
Num = 0


def enter_kwp(name, lex):
    global keywords_pasc, n_kwp
    n_kwp += 1
    keywords_pasc[n_kwp] = {'Word': name, 'Lex': lex}


# Инициализация словаря ключевых слов Pascal
def init_keywords_pasc():
    global keywords_pasc, n_kwp
    keywords_pasc = {}
    n_kwp = 0
    enter_kwp('BEGIN', 'lexBEGIN')
    enter_kwp('DO', 'lexDO')
    enter_kwp('ELSE', 'lexElse')
    enter_kwp('IF', 'lexIF')
    enter_kwp('PROGRAM', 'lexMODULE')
    enter_kwp('THEN', 'lexTHEN')
    enter_kwp('VAR', 'lexVAR')
    enter_kwp('WHILE', 'lexWHILE')
    enter_kwp('READLN', 'lexCONST')
    enter_kwp('READ', 'lexCONST')
    enter_kwp('WRITE', 'lexCONST')
    enter_kwp('WRITELN', 'lexCONST')
    enter_kwp('FOR', 'lexCONST')
    enter_kwp('REPEAT', 'lexCONST')
    enter_kwp('ARRAY', 'lexCONST')
    enter_kwp('OF', 'lexCONST')
    enter_kwp('OR', 'lexCONST')
    enter_kwp('TYPE', 'lexCONST')
    enter_kwp('IN', 'lexCONST')
    enter_kwp('AND', 'lexCONST')
    enter_kwp('CASE', 'lexCONST')
    enter_kwp('DOWNTO', 'lexCONST')
    enter_kwp('FUNCTION', 'lexCONST')
    enter_kwp('MOD', 'lexCONST')
    enter_kwp('DIV', 'lexCONST')
    enter_kwp('PROCEDURE', 'lexCONST')
    enter_kwp('UNTIL', 'lexCONST')
    enter_kwp('TO', 'lexCONST')
    enter_kwp('END', 'lexCONST')
    enter_kwp('RECORD', 'lexCONST')
    enter_kwp('STRING', 'lexCONST')
    enter_kwp('FILE', 'lexCONST')
    enter_kwp('SQRT', 'lexCONST')
    enter_kwp('HALT', 'lexCONST')
    enter_kwp('ABS', 'lexCONST')
    enter_kwp('INTEGER', 'lexCONST')
    enter_kwp('CLASS', 'lexCONST')


def init_OTEST_table():
    global is_begin, o_lex_cnt, cur_tab, n, otest_table, o_lex_count
    is_begin = False
    o_lex_cnt = 0
    cur_tab = ''
    n = 0
    otest_table = [{} for _ in range(o_lex_count + 1)]

    for k in range(1, o_lex_count + 1):
        otest_table[k]['Lex'] = 'LexEOT'
        otest_table[k]['c'] = 0


def add_to_OTEST_table(otest_table, lex):
    global is_begin, o_lex_cnt, count
    if lex == 'lexBEGIN':
        is_begin = True
    o_lex_cnt += 1
    otest_table[o_lex_cnt] = {'lex': lex}
    if lex == 'lexName':
        otest_table[o_lex_cnt]['name'] = Name
    elif lex == 'lexNum':
        otest_table[o_lex_cnt]['num'] = Num
    # print(f"{o_lex_cnt} ------------------ {otest_table[o_lex_cnt]['lex']}")
    count += 1


def cap(ch):
    if 'a' <= ch <= 'z':
        return chr(ord(ch) - (ord('a') - ord('А')))
    else:
        return ch


def cap_str(name):
    # print('here')
    return ''.join(cap(ch) for ch in name)


def convert_names_for_pasc(otest_table, n_kwp, key_words_pasc):
    global o_lex_cnt
    for i in range(1, o_lex_cnt + 1):
        if (otest_table[i]['Lex'] == 'lexName' and otest_table[i]['name'] not in ['In', 'ABS'] and
                otest_table[i + 1]['Lex'] not in ['lexLpar', 'lexDOT']):
            if otest_table[i]['name'] == 'INTEGER':
                otest_table[i]['name'] = 'integer'
            else:
                k = n_kwp
                temp = cap_str(otest_table[i]['name'])
                while k > 0 and temp != key_words_pasc[k]['Word']:
                    k -= 1
                if k > 0:
                    otest_table[i]['name'] += '_'


def convert_oto_pasc():
    global OTestTable
    for entry in OTestTable:
        if entry.lex == lexMODULE:
            entry.pasc_int = 'program '
        elif entry.lex == lexName:
            entry.pasc_int = entry.name
        elif entry.lex == lexNum:
            entry.pasc_int = str(entry.num)
        elif entry.lex == lexSemi:
            entry.pasc_int = ';'
        elif entry.lex == lexIMPORT:
            entry.pasc_int = ''
        elif entry.lex == lexComma:
            entry.pasc_int = ', '
        elif entry.lex == lexCONST:
            entry.pasc_int = 'const'
        elif entry.lex == lexEQ:
            entry.pasc_int = '= '
        elif entry.lex == lexVAR:
            entry.pasc_int = 'var'
        elif entry.lex == lexColon:
            entry.pasc_int = ': '
        elif entry.lex == lexBEGIN:
            entry.pasc_int = 'begin'
        elif entry.lex == lexAss:
            entry.pasc_int = ':= '
        elif entry.lex == lexDot:
            entry.pasc_int = '.'
        elif entry.lex == lexLpar:
            entry.pasc_int = '('
        elif entry.lex == lexRpar:
            entry.pasc_int = ')'
        elif entry.lex == lexWHILE:
            entry.pasc_int = 'while '
        elif entry.lex == lexMOD:
            entry.pasc_int = 'mod '
        elif entry.lex == lexNE:
            entry.pasc_int = '<> '
        elif entry.lex == lexDO:
            entry.pasc_int = 'do begin'
        elif entry.lex == lexPlus:
            entry.pasc_int = ' + '
        elif entry.lex == lexEND:
            entry.pasc_int = 'end'
        elif entry.lex == lexIF:
            entry.pasc_int = 'if '
        elif entry.lex == lexTHEN:
            entry.pasc_int = 'then begin'
        elif entry.lex == lexMinus:
            entry.pasc_int = '- '
        elif entry.lex == lexMult:
            entry.pasc_int = '*'
        elif entry.lex == lexLT:
            entry.pasc_int = '< '
        elif entry.lex == lexGT:
            entry.pasc_int = '> '
        elif entry.lex == lexLE:
            entry.pasc_int = '<= '
        elif entry.lex == lexGE:
            entry.pasc_int = '>= '
        elif entry.lex == lexDIV:
            entry.pasc_int = 'div '
        elif entry.lex == lexELSE:
            entry.pasc_int = 'else begin'
        elif entry.lex == lexELSIF:
            entry.pasc_int = 'else if '
        else:
            entry.pasc_int = '?'


def write_test(otest_table, o_lex_count):
    if len(sys.argv) < 3:
        print('Введите файл для вывода')
    else:
        file_name = sys.argv[2]
        with open(file_name, 'w') as f:
            # f.write('Число лексем: {}\n'.format(count))
            for i in range(1, o_lex_count + 1):
                # f.write('{} {}\n'.format(otest_table[i]['Lex'], otest_table[i]['c']))
                pass


def del_tab(cur_tab):
    # Уменьшает текущую вкладку на 3 пробела
    return cur_tab[:-3] if len(cur_tab) > 3 else ''


def min_tab(cur_tab):
    # Возвращает минимальную вкладку, уменьшенную на 3 пробела, если это возможно
    return cur_tab[:-3] if len(cur_tab) >= 3 else cur_tab


def read_import(otest_table, i):
    while otest_table[i]['Lex'] not in (lexCONST, lexVAR, lexBEGIN, lexRpar):
        i += 1
    return i


def read_in(i):
    global CurTab
    k = i
    otest_table[k]['pascint'] = ''
    otest_table[k+1]['pascint'] = ''
    k += 2
    if otest_table[k]['name'] == 'Open':
        while (otest_table[k]['Lex'] not in [lexSemi, lexEND, lexELSE, lexELSIF]):
            otest_table[k]['pascint'] = ''
            k += 1
        otest_table[k]['pascint'] = ''
        otest_table[k]['Lex'] = lexFCK
    else:
        print('?', file = f)
        print(CurTab, file = f)
        i += 2
        while otest_table[i]['Lex'] != lexLpar:
            i += 1
        otest_table[i]['Lex'] = lexName
        otest_table[i]['pascint'] = 'Readln('
        # i += 1


def read_out(i):
    k = i
    otest_table[k]['pascint'] = ''
    otest_table[k + 1]['pascint'] = ''
    k += 2
    if otest_table[k]['name'] == 'Ln':
        while otest_table[k]['Lex'] not in [lexSemi, lexEND, lexELSE, lexELSIF]:
            temp = otest_table[k]['pascint']
            otest_table[k]['pascint'] = ''
            k += 1
        otest_table[k - 1]['Lex'] = lexName
        otest_table[k - 1]['pascint'] = 'Writeln()'
    else:
        i += 2
        while otest_table[i]['Lex'] != lexLpar:
            i += 1
        otest_table[i]['pascint'] = 'Write('
        j = i
        while otest_table[j]['Lex'] != lexComma:
            j += 1
        otest_table[j]['pascint'] = ':'


def read_inc(i):
    global OTestTable
    i += 2
    temp = OTestTable[i].name
    i += 1
    if OTestTable[i].lex == lexRpar:
        OTestTable[i].pascint = f'{temp} := {temp} + 1'
    else:
        i += 1
        tempnum = ''
        while not (OTestTable[i].lex == lexRpar and
                   (OTestTable[i+1].lex in [lexEND, lexELSE, lexELSIF, lexSemi])):
            tempnum += OTestTable[i].pascint
            i += 1
        OTestTable[i].pascint = f'{temp} := {temp} + {tempnum}' + (';' if OTestTable[i+1].lex == lexSemi else '')


def read_dec(i):
    global OTestTable
    i += 2
    temp = OTestTable[i].name
    i += 1
    if OTestTable[i].lex == lexRpar:
        OTestTable[i].pascint = f'{temp} := {temp} - 1'
    else:
        i += 1
        tempnum = ''
        while not (OTestTable[i].lex == lexRpar and
                   (OTestTable[i+1].lex in [lexEND, lexELSE, lexELSIF, lexSemi])):
            tempnum += OTestTable[i].pascint
            i += 1
        OTestTable[i].pascint = f'{temp} := {temp} - {tempnum}' + (';' if OTestTable[i+1].lex == lexSemi else '')


def read_max(i):
    global OTestTable
    while OTestTable[i].lex != lexRpar:
        i += 1
    OTestTable[i].pascint = 'maxint'


def read_min(i):
    global OTestTable
    while OTestTable[i].lex != lexRpar:
        i += 1
    OTestTable[i].pascint = '-maxint - 1'


def read_odd(i):
    global OTestTable
    i += 2
    temp = OTestTable[i].name
    i += 1
    OTestTable[i].pascint = f'({temp} % 2 != 0)'


def write_pasc_int(OTestTable, ParamStr):
    fu = False
    i = 1
    with open(ParamStr(2), 'w') as f:
        f.write('Program ')
        # f.write('program ')
        while OTestTable[i].lex != lexEOT:
            # Увеличение таба
            if OTestTable[i].lex in (lexCONST, lexVAR, lexBEGIN, lexTHEN, lexDO):
                CurTAB += TAB

            # Вывод текущей лексемы
            if OTestTable[i].lex == lexDot and OTestTable[i + 1].lex == lexDot:
                OTestTable[i + 1].pascint = ''

            if OTestTable[i].lex == lexEND:
                f.write('begin\n')

            if OTestTable[i].lex == lexIMPORT:
                curLex = lexIMPORT
                read_import(i)
                i -= 1
            elif OTestTable[i].lex == lexELSE:
                f.write('end\n')
                f.write(min_tab(CurTAB) + 'else begin')
            elif OTestTable[i].lex == lexELSIF:
                f.write('end\n')
                f.write(min_tab(CurTAB) + 'else if ')
                OTestTable[i].lex = lexFCK
                fu = True

            # Имя
            elif OTestTable[i].lex in (lexName, lexNum):
                name = OTestTable[i].name
                if name == 'In':
                    read_in(i)
                elif name == 'Out':
                    read_out(i)
                elif name == 'INC':
                    read_inc(i)
                elif name == 'DEC':
                    read_dec(i)
                elif name == 'MAX':
                    read_max(i)
                elif name == 'MIN':
                    read_min(i)
                elif name == 'ODD':
                    read_odd(i)
                f.write(OTestTable[i].pascint + ' ' if OTestTable[i + 1].lex not in (lexSemi, lexColon, lexComma, lexRpar, lexLpar, lexDot, lexName, lexMult, lexPlus, lexFCK) else OTestTable[i].pascint)
                curlex = OTestTable[i].lex

            # End
            # Остальное
            else:
                f.write(OTestTable[i].pascint)
                curlex = OTestTable[i].lex

            # Обработка табуляции после точки с запятой
            if OTestTable[i].lex == lexSemi:
                if OTestTable[i + 1].lex in (lexVAR, lexBEGIN, lexCONST):
                    CurTAB = ''

            # Перенос строки и обработка табуляции
            if ((OTestTable[i].lex in (lexSemi, lexBEGIN, lexCONST, lexVAR, lexTHEN, lexDO, lexELSE) or
                 OTestTable[i + 1].lex in (lexELSIF, lexELSE, lexEND)) and
                curlex != lexIMPORT) or (OTestTable[i].lex != lexSemi and OTestTable[i + 1].lex in (lexELSE, lexELSIF, lexEND) and OTestTable[i].lex != lexFCK):
                f.write('\n')
                if OTestTable[i + 1].lex in (lexEND, lexELSE, lexELSIF):
                    if OTestTable[i].lex == lexEND and OTestTable[i + 1].lex == lexEND:
                        f.write(min_tab(min_tab(CurTAB)))
                    else:
                        f.write(min_tab(CurTAB))
                else:
                    f.write(CurTAB)

            # Удаление табуляции
            if OTestTable[i].lex == lexEND or fu:
                del_tab()

            # Очистка pascint для следующего элемента, если текущий lex - END
            if OTestTable[i].lex == lexEND and OTestTable[i + 1].lex == lexName:
                OTestTable[i + 1].pascint = ''

            i += 1
            fu = False

            # Закрытие файла после записи
        f.close()


def read_test(OTestTable):
    # init_o_test_table()
    # init_keywords_pasc()
    # next_lex()
    # while lex != LexEOT:
    #     add_to_o_test_table(OTestTable, lex)
    #     next_lex()
    add_to_OTEST_table(OTestTable, lexDot)
    convert_names_for_pasc(OTestTable)
    # write_test()
    convert_oto_pasc(OTestTable)
    write_pasc_int(OTestTable)