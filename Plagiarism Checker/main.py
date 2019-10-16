import json
import os
import argparse

from preprocess import vectorize_file
from minhash import Minhash
from index import Index
from lsh import LSH


class Handler:
    def __init__(self):
        self.config = {
            "LSH_FILE": "lsh.pkl",
            "MINHASH_FILE": "min.pkl",
            "CORPUS_DIR": "./corpus"
        }

        self.index = Index(self.config)
        self.lsh = self.index.lsh
        self.minhashes = self.index.minhashes

    def set_config(self, key, value):
        self.config[key] = value

    def query(self, file_name):
        vector = vectorize_file(file_name)
        minhash = Minhash(vector)
        similarItems = self.lsh.get_similar(minhash)

        res = []
        for doc in similarItems:
            res.append(doc)

        res.sort(key=lambda doc: minhash.compare(
            self.minhashes[doc]), reverse=True)

        return [(doc, minhash.compare(self.minhashes[doc]) * 100) for doc in res]


if __name__ == '__main__':
    handler = Handler()

    parser = argparse.ArgumentParser(description="Plagiarism Checker")
    parser.add_argument(
        "--file_name", help="Relative path to the file which you want to check", type=str)
    parser.add_argument(
        '--build', help='Build the LSH and minhash from scratch', action="store_true")

    args = parser.parse_args()

    if args.build:
        handler.index.build_index()
    elif args.file_name:
        results = handler.query(args.file_name)

        for item in results:
            print("{} {}".format(*item))
