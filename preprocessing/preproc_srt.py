import sys

import srt


for sub in srt.parse(sys.stdin):
    print(sub.content.replace('\n', ' '))
