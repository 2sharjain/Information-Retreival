import re
from zlib import crc32

from nltk import ngrams, line_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

_regex = re.compile(r'[^\w\s]')


def vectorize_file(file_name):
    '''
        Creates a vector from hashing the shingles from the file
    '''
    try:
        with open(file_name, 'r') as f:
            text = f.read()
        return vectorize(text)
    except UnicodeDecodeError:
        return []


def process_doc(doc):
    '''
        Process the doc according to the following pipeline. Returns a dict of 
        words and their frequency in the doc.

        Tokenization -> Removal of Stop words -> Stemming.
    '''
    words = word_tokenize(doc)
    stop_words = set(stopwords.words('english'))
    filtered = [w for w in words if w not in stop_words]

    porter = PorterStemmer()
    stemmed = [porter.stem(w) for w in filtered]

    res = {}

    for w in stemmed:
        res[w] = res.get(w, 0) + 1
    return res


def vectorize(text):
    '''
        Creates a vector of 32bit ints from the shingles of the text.
    '''
    text = text.lower()
    text = _clean(text)

    vector = []

    for gram in ngrams(text, 3):
        vector.append(_hash(''.join(gram)))

    return vector


def _clean(text):
    '''
        Removes punctuations, whitespaces etc from the text.
    '''
    return _regex.sub("", text)


def _hash(text):
    '''
        Hashes the string to a 32 bit int.
    '''
    return crc32(bytes(text, 'utf-8'))
