import sys

lines = []
for raw_line in sys.stdin:
    line = raw_line.strip()
    if line:
        lines.append(line)
    else:
        if lines:
            print(" ".join(lines))
            lines = []

if lines:
    print(" ".join(lines))
