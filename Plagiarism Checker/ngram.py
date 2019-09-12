import os
import csv
import re
import pickle
from zlib import crc32
from nltk import ngrams, line_tokenize


def clean_text(text):
    text = re.sub(r'[^\w\s]', '', text)
    return text


def get_text(filename):
    try:
        with open(filename) as f:
            text = f.read()
            text = text.lower()
            text = clean_text(text)
            return text
    except UnicodeDecodeError:
        return None


def get_hash(text: str):
    return crc32(bytes(text, 'utf-8'))


N = 10
max_val = (2**32)-1
perms = [(39134679, 3958371718), (1934647404, 2107734587), (1401358403, 4243171327), (3105189876, 260436580), (3840209418, 1601302872),
         (4056554230, 3092965197), (2678475855, 433466823), (1873974458, 156358566), (3468388933, 4275652503), (3378917926, 3324770469)]


def minhash(s, prime=4294967311):

    vec = [float('inf') for i in range(N)]

    for val in s:
        if not isinstance(val, int):
            val = hash(val)
        for perm_idx, perm_vals in enumerate(perms):
            a, b = perm_vals
            output = (a * val + b) % prime

            if vec[perm_idx] > output:
                vec[perm_idx] = output
    return vec


def get_similarity(vec1, vec2):
    assert(len(vec1) is len(vec2))

    X = set(vec1)
    Y = set(vec2)

    jaccard = len(X.intersection(Y)) / len(X.union(Y))

    jaccard = round(jaccard, 3)
    return jaccard * 100


def get_minhash(file_name):
    hashes = []
    text = get_text(file_name)
    if not text:
        return None

    for gram in ngrams(text, 3):
        hashes.append(get_hash(''.join(gram)))

    return minhash(hashes)


def build_index(dir_name, index_file):
    print("building minhash indexes")

    corpusDir = os.listdir(dir_name)
    corpusDir = [dir_name + '/' + f for f in corpusDir]

    all_hashes = {}

    for file_name in corpusDir:
        if file_name.endswith('.txt'):
            signature = get_minhash(file_name)
            if signature:
                all_hashes[file_name] = signature

    with open(index_file, 'wb') as f:
        pickle.dump(all_hashes, f)

    print("Done building hashes")


def get_minhashes_from_index(index_file):
    with open(index_file, 'rb') as f:
        hash_dict = pickle.load(f)
        return hash_dict


def query_doc(doc_name, corpus_dir, index_file):
    signature = get_minhash(doc_name)
    if not signature:
        return

    scores = {}
    minhashes = get_minhashes_from_index(index_file)
    docs = list(minhashes.keys())

    for file_name in docs:
        signature2 = minhashes[file_name]
        score = get_similarity(signature, signature2)
        scores[file_name] = score

    docs.sort(key=lambda x: scores[x], reverse=True)

    for doc in docs[:10]:
        print(doc, str(scores[doc]) + ' %')


def main():
    index_file = "msh.pkl"
    corpus_dir = "./corpus"

    if not os.path.exists(index_file):
        build_index(corpus_dir, index_file)

    doc_name = input("Enter relative path to document: \n")
    query_doc(doc_name, corpus_dir, index_file)


if __name__ == '__main__':
    main()
