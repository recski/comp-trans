import sys
from collections import Counter

import pronouncing
import stanza
from tqdm import tqdm

nlp = stanza.Pipeline('en', processors='tokenize,lemma')

stats = Counter()

for line in tqdm(sys.stdin):
    try:
        w, count = line.strip().split()
    except ValueError:
        sys.stderr.write(f'skipping line: {line}')
        continue
    count = int(count)
    d = nlp(w)
    for sen in d.sentences:
        for word in sen.words:
            pronunciation_list = pronouncing.phones_for_word(word.lemma)
            if len(pronunciation_list) > 0:
                n = pronouncing.syllable_count(pronunciation_list[0])
                stats[n] += count


for k, v in stats.most_common():
    print(k, v)
