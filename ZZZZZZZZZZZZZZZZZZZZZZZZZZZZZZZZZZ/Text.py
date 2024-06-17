import sys

chEOT = ''
text = ''
pos = -1

def init(filename):
    global text, pos
    with open(filename, 'r', encoding = 'utf-8') as f:
        text = f.read()
    pos = -1

def next_ch():
    global pos
    if pos < len(text):
        pos += 1
        if pos < len(text):
            return text[pos]
    return chEOT

def error(message, pos = None):
    if pos is None:
        pos = globals()['pos']
    lineStartPos = text.rfind('\n', 0, pos) + 1
    afterLinePos = text.find('\n', lineStartPos)
    if afterLinePos == -1:
        afterLinePos = len(text)
    line = text.count('\n', 0, lineStartPos) + 1
    print(text[lineStartPos:afterLinePos])
    print(''.join(map(lambda c: ' ' if c != '\t' else '\t', text[lineStartPos:pos])) + '^')
    print(f'Ошибка в строке {line}: {message}')
    sys.exit(1)