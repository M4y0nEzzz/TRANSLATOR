import sys
import os
from O_ERROR import *

# Константы
CH_SPACE = ' '  # Пробел
CH_TAB = '\t'   # Табуляция
CH_EOL = '\n'   # Конец строки
CH_EOT = '\0'   # Конец текста
Pos = 0


# Глобальные переменные
ch = ''         # Очередной символ
line = 1        # Номер строки
pos = 0         # Номер символа в строке
tab_size = 3    # Размер табуляции

# Инициализация файла
f = None


def reset_text():
    global f, pos, line, ch
    if len(sys.argv) < 2:
        print('Формат вызова:')
        print('   O <входной файл>')
        sys.exit()
    else:
        if os.path.isfile(sys.argv[1]):
            f = open(sys.argv[1], 'r')
            pos = 0
            line = 1
            next_ch()
        else:
            error('Входной файл не найден')


def close_text():
    global f
    if f is not None:
        f.close()


def next_ch():
    global f, ch, pos, line
    if f is None or f.read(1) == '':
        ch = CH_EOT
    else:
        f.seek(f.tell() - 1)  # Возврат на один символ назад
        if f.readline() == '':
            print()
            line += 1
            pos = 0
            ch = CH_EOL
        else:
            ch = f.read(1)
            if ch != CH_TAB:
                print(ch, end='')
                pos += 1
            else:
                while pos % tab_size != 0:
                    print(' ', end='')
                    pos += 1
