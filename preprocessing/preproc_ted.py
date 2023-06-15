import html
import sys

for line in sys.stdin:
    if 'NULL' in line:
        continue
    print(html.unescape(line.strip()))
