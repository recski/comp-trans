# comp-trans

Code and data for the paper **Language complexity in human and machine translation: a preliminary
study** presented at the [HiT-IT 2023](http://hit-it-conference.org/home/) conference.

Authors: [Gábor Recski](https://informatics.tuwien.ac.at/people/gabor-recski) and Fanni Kádár

## Dependencies

To install dependencies, run

```
python setup.py install
```

## Usage
The four text samples described in the paper are in the `samples` directory.
To calculate readability and lexical diversity stats in the paper on all samples, run

```
python stats.py -p 1984 ted3 fgm DC567 -s 4
```

Code for some of the preprocessing steps and for calculating the statistics of syllable counts in
English and Hungarian presented in the paper are made available in the directories `preprocessing`
and `syllable_stats`. These are not documented, but feel free to reach out to the first author if you need help.

## Citing

If you use or describe the data or software in this package, please cite the following paper:

```
@inproceedings{Recski:2023b,
    title = "Language complexity in human and machine translation: a preliminary study",
    author = "Recski, G{\'a}bor and K{\'a}d{\'a}r, Fanni",
    booktitle = "Proceedings of the International Conference on Human-Informed Translation and Interpreting Technology (HiT-IT 2023)",
    year = "2023",
    address = "Naples, Italy"
}

```
