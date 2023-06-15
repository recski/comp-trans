import sys

from collections import Counter
from tqdm import tqdm

stats = Counter()

for raw_line in tqdm(sys.stdin, unit='words', unit_scale=True):
    if raw_line.startswith('form') or raw_line.startswith('#'):
        continue
    line = raw_line.strip()
    if not line:
        continue

    lemma = line.split('\t')[2]

    count = sum(lemma.count(char) for char in "aáeéiíoóöőuúüű")
    if count > 0:
        stats[count] += 1


for k, v in stats.most_common():
    print(k, v)
