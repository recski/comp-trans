import argparse
import logging
import sys

import deepl
from tqdm import tqdm


def get_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-f", "--format", default=None, type=str)
    parser.add_argument("-t", "--target-lang", default=None, type=str)
    return parser.parse_args()


def main():
    logging.basicConfig(
        format="%(asctime)s : "
        + "%(module)s (%(lineno)s) - %(levelname)s - %(message)s"
    )
    logging.getLogger().setLevel(logging.WARNING)
    args = get_args()

    auth_key = None  #  "add your DeepL API key here"
    translator = deepl.Translator(auth_key)

    tgt_lang = args.target_lang
    assert tgt_lang in ('EN-US', 'HU')

    if args.format == "lines":
        for line in tqdm(sys.stdin):
            result = translator.translate_text(line.strip(), target_lang=tgt_lang)
            print(result.text)
    elif args.format == "blocks":
        input_text = []
        for line in tqdm(sys.stdin):
            text = line.strip()
            if not text:
                if input_text:
                    result = translator.translate_text(
                        "\n".join(input_text), target_lang=tgt_lang
                    )
                    print(result.text)
                    input_text = []
            else:
                input_text.append(text)

    elif args.format == "all":
        input_text = sys.stdin.read()
        result = translator.translate_text(input_text, target_lang=tgt_lang)
        print(result.text)

    else:
        raise ValueError(f"unknown format: {args.format}")


if __name__ == "__main__":
    main()
