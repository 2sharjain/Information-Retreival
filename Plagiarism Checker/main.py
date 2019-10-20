import json
import os
import argparse

from preprocess import vectorize, process_doc
from minhash import Minhash
from index import Index
from lsh import LSH


class Handler:
    def __init__(self):
        self.config = self.get_config()
        self.index = Index(self.config)

    def set_config(self, key, value):
        self.config[key] = value

    def query(self, file_name, use_idf=False):
        with open(file_name, 'r') as f:
            text = f.read()
            return self.query_using_idf(text) if use_idf else self.query_using_lsh(text)

    def query_using_idf(self, text):
        self.idf = self.index.idf
        vector = self.idf.to_vector(process_doc(text))
        docs = list(self.idf.vectors.keys())
        vectors = self.idf.vectors

        docs.sort(key=lambda x: self.idf.cosine(
            vector, vectors[x]), reverse=True)

        res = docs[:10]
        res = [(doc, self.idf.cosine(vector, vectors[doc])) for doc in res]

        return res

    def query_using_lsh(self, text):
        self.lsh = self.index.lsh
        self.minhashes = self.index.minhashes

        vector = vectorize(text)
        minhash = Minhash(vector)
        similarItems = self.lsh.get_similar(minhash)

        res = []
        for doc in similarItems:
            res.append(doc)

        res.sort(key=lambda doc: minhash.compare(
            self.minhashes[doc]), reverse=True)

        return [(doc, minhash.compare(self.minhashes[doc]) * 100) for doc in res]

    def get_config(self):
        with open('config.json', 'r') as f:
            return json.load(f)


if __name__ == '__main__':
    handler = Handler()

    parser = argparse.ArgumentParser(description="Plagiarism Checker")
    parser.add_argument(
        "--file_name", help="Relative path to the file which you want to check", type=str)
    parser.add_argument(
        '--build', help='Build the LSH and minhash from scratch', action="store_true")
    parser.add_argument(
        '--use_idf', help='use TF-IDF to get similar', action='store_true')

    args = parser.parse_args()

    if args.build:
        handler.index.build_index()
    elif args.file_name:
        results = handler.query(args.file_name, args.use_idf)

        for item in results:
            print("{} {}".format(*item))
