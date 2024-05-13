# Обработка ошибок

from O_TEXT import *

current_line = 0
lex_position = 0
ch = ''
ch_EOL = '\n'
ch_EOT = '\0'


def error(msg):
    # Функция для вывода сообщения об ошибке и завершения программы
    global current_line, lex_position
    e_line = current_line
    while ch != ch_EOL and ch != ch_EOT:
        next_ch()
    if ch == ch_EOT:
        print()
    print('^'.rjust(lex_position))
    print(f'(Строка {e_line}) Ошибка: {msg}')
    print()
    exit(1)


def expected(msg):
    # Функция для вывода сообщения о том, что что-то ожидалось
    error(f'Ожидается {msg}')


def warning(msg):
    # Функция для вывода предупреждения
    print()
    print(f'Предупреждение: {msg}')
    print()
