# Компилятор языка О

import O_TEXT
import O_TEST
import O_PARS
import O_SCAN
import O_GEN
from O_SCAN import *
from OVM import *


def init():
    O_TEXT.reset_text()
    O_SCAN.init_scan()
    O_TEST.init_OTEST_table()
    O_PARS.init_keywords_pasc()
    O_GEN.init_gen()


def done():
    O_TEXT.close_text()


if __name__ == "__main__":
    print('Компилятор языка О')
    init()  # Инициализация
    compile()  # Компиляция
    run()  # Выполнение
    read_test()  # Чтение теста
    # t1 = milliseconds()  # Начало отсчета времени
    # t2 = milliseconds()  # Конец отсчета времени
    # print('Время', t2 - t1)  # Вывод времени выполнения
    done()  # Завершение
