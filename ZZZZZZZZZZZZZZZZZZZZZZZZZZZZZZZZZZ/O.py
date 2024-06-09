import sys
import Parser

if len(sys.argv) != 2:
    print('Usage: python O.py filename.o')
    sys.exit(0)
filename = sys.argv[1]
Parser.parse(filename)
print('Ok')