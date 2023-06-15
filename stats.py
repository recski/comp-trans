import argparse
import json
import os
from collections import Counter
from math import log

import pronouncing
from lexical_diversity import lex_div
from stanza.utils.conll import CoNLL
from tabulate import tabulate


STATS1 = ["toks", "sens", "word types", "lemma types"]

STATS2 = [
    "words per sen",
    "complex word ratio",
    "Herdan's C (words)",
    "Herdan's C (lemmas)",
    "MTLD (words)",
    "MTLD (lemmas)",
    "Gunning's F",
]


STAT_LABELS1 = ["words", "sentences", "word types", "lemma types"]

STAT_LABELS2 = [
    "w/s",
    "$L_c/L$",
    "$C_w$",
    "$C_l$",
    "MTLD$_w$",
    "MTLD$_l$",
    "F",
]

STAT_FMTS1 = ["d", "d", "d", "d"]
STAT_FMTS2 = [".2f", ".2%", ".2f", ".2f", ".1f", ".1f", ".2f"]


def get_syllable_count(lemma, lang):
    if lang == "en":
        pronunciation_list = pronouncing.phones_for_word(lemma)
        if not pronunciation_list:
            return -1
        return pronouncing.syllable_count(pronunciation_list[0])
    elif lang == "hu":
        return sum(lemma.count(char) for char in "aáeéiíoóöőüű")
    else:
        raise ValueError(f"unsupported lang: {lang}")


def get_counts(doc, lang, hu_min_syllables):
    counts = Counter()
    vocabs = {"words": Counter(), "lemmas": Counter()}
    for sen in doc.sentences:
        counts["sens"] += 1
        for word in sen.words:
            counts["toks"] += 1
            counts["chars"] += len(word.text)
            vocabs["words"][word.text] += 1
            vocabs["lemmas"][word.lemma] += 1

            if word.upos != "PROPN":
                syllable_count = get_syllable_count(word.lemma, lang)
                min_syllables = 3 if lang == "en" else hu_min_syllables
                if syllable_count >= min_syllables:
                    counts["complex_words"] += 1

    return counts, vocabs


def get_stats(counts, vocabs):
    stats = {
        "chars": counts["chars"],
        "toks": counts["toks"],
        "sens": counts["sens"],
        "word types": len(vocabs["words"]),
        "lemma types": len(vocabs["lemmas"]),
        "complex words": counts["complex_words"],
    }

    log_toks = log(stats["toks"])
    stats.update(
        {
            "chars per word": counts["chars"] / counts["toks"],
            "words per sen": counts["toks"] / counts["sens"],
            "complex word ratio": counts["complex_words"] / counts["toks"],
            "Herdan's C (words)": log(stats["word types"]) / log_toks,
            "Herdan's C (lemmas)": log(stats["lemma types"]) / log_toks,
        }
    )

    stats["Gunning's F"] = 0.4 * (
        counts["toks"] / counts["sens"] + 100 * counts["complex_words"] / counts["toks"]
    )

    return stats


def print_stats(all_stats):
    fns = list(all_stats.keys())
    table1 = [[fn] + [all_stats[fn][stat] for stat in STATS1] for fn in fns]
    table2 = [[fn] + [all_stats[fn][stat] for stat in STATS2] for fn in fns]

    print(
        tabulate(
            table1,
            headers=STAT_LABELS1,
            tablefmt="latex_booktabs",
            # tablefmt="github",
            floatfmt=["s"] + STAT_FMTS1,
        )
    )

    print(
        tabulate(
            table2,
            headers=STAT_LABELS2,
            tablefmt="latex_booktabs",
            # tablefmt="github",
            floatfmt=["s"] + STAT_FMTS2,
        )
    )


def get_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-p", "--prefixes", nargs="+", default=[])
    parser.add_argument("-l", "--lang", type=str)
    parser.add_argument("-s", "--hu_min_syllables", type=int)
    return parser.parse_args()


def main():
    args = get_args()
    all_stats = {}
    input_files = {
        prefix: {
            version: os.path.join("samples", prefix, f"{prefix}_{version}.conll")
            for version in ("en_orig", "hu_human", "hu_deepl")
        }
        for prefix in args.prefixes
    }

    for prefix, versions in input_files.items():
        all_stats[prefix] = {}
        for version, fn in versions.items():
            lang = "hu" if "_hu_" in fn else "en"
            doc = CoNLL.conll2doc(fn)
            counts, vocabs = get_counts(doc, lang, args.hu_min_syllables)
            stats = get_stats(counts, vocabs)

            words = [word.text for sen in doc.sentences for word in sen.words]
            lemmas = [word.lemma for sen in doc.sentences for word in sen.words]
            stats['MTLD (words)'] = lex_div.mtld(words)
            stats['MTLD (lemmas)'] = lex_div.mtld(lemmas)

            all_stats[prefix][version] = stats

    for prefix, stats in all_stats.items():
        print(f"============ {prefix} ============")
        print_stats(stats)
        print()

    with open("stats.json", "w") as f:
        json.dump(all_stats, f)
    print("stats saved to stats.json")


if __name__ == "__main__":
    main()
