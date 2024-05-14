# Таблица имен

# Импорт необходимых модулей
from O_SCAN import *
from O_ERROR import *


# Категории имён
class Cat:
    CONST, VAR, TYPE, STPROC, MODULE, GUARD = range(6)


# Типы
class Type:
    NONE, INT, BOOL = range(3)


# Запись таблицы имен
class ObjRec:
    def __init__(self, name, cat, typ, value, prev=None):
        self.name = name
        self.cat = cat
        self.typ = typ
        self.value = value
        self.prev = prev

    # Инициализация top с охранником (guard node)


top = ObjRec('', Cat.GUARD, Type.NONE, 0)

# Инициализация таблицы имен
bottom = None
curr_obj = None


def init_name_table():
    global top
    top = None


def enter(name, cat, typ, val):
    global top
    p = ObjRec(name, cat, typ, val, top)
    top = p


def open_scope():
    global top, bottom
    enter('', Cat.GUARD, Type.NONE, 0)
    if top.prev is None:
        bottom = top


def close_scope():
    global top
    while top.cat != Cat.GUARD:
        top = top.prev
    top = top.prev


def new_name(name, cat):
    global top
    obj_ref = top
    while obj_ref is not None and obj_ref.cat != Cat.GUARD and obj_ref.name != name:
        obj_ref = obj_ref.prev
    if obj_ref is None or obj_ref.cat == Cat.GUARD:
        obj_ref = ObjRec(name, cat, Type.NONE, 0, top)
        top = obj_ref
    else:
        error('Повторное объявление имени')


def find(name, obj):
    global bottom, top
    bottom.name = name
    obj_ref = top
    while obj_ref.name != name:
        obj_ref = obj_ref.prev
    if obj_ref == bottom:
        error('Необъявленное имя')
    else:
        obj[0] = obj_ref


def first_var():
    global curr_obj
    curr_obj = top
    return next_var()


def next_var():
    global curr_obj, bottom
    while curr_obj != bottom and curr_obj.cat != Cat.VAR:
        curr_obj = curr_obj.prev
    if curr_obj == bottom:
        return None
    else:
        v_ref = curr_obj
        curr_obj = curr_obj.prev
        return v_ref
