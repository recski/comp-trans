from setuptools import find_packages, setup

setup(
    name="comp-trans",
    version="1.0.0",
    description="code for the paper \"Language complexity in human and machine translation: a preliminary study\" ",
    url="https://github.com/recski/comp-trans",
    author="Gabor Recski",
    author_email="gabor.recski@tuwien.ac.at",
    license="MIT",
    install_requires=[
        "lexical_diversity",
        "pronouncing",
        "stanza",
        "tabulate",
        "tqdm",
    ],
    packages=find_packages(),
    zip_safe=False,
)
