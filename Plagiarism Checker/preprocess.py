import re

from nltk import ngrams, line_tokenize
from zlib import crc32

_regex = re.compile(r'[^\w\s]')


def vectorize_file(file_name):
    try:
        with open(file_name, 'r') as f:
            text = f.read()
        return vectorize(text)
    except UnicodeDecodeError:
        return []


def vectorize(text):
    text = text.lower()
    text = _clean(text)

    vector = []

    for gram in ngrams(text, 3):
        vector.append(_hash(''.join(gram)))

    return vector


def _clean(text):
    return _regex.sub("", text)


def _hash(text):
    return crc32(bytes(text, 'utf-8'))
