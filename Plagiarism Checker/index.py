import os
import pickle
from preprocess import vectorize_file
from minhash import Minhash
from lsh import LSH


class Index:
    def __init__(self, config):
        self.MINHASH_FILE = config.get('MINHASH_FILE', None)
        self.LSH_FILE = config.get('LSH_FILE', None)
        self.CORPUS_DIR = config.get('CORPUS_DIR', None)

        if not os.path.exists(self.MINHASH_FILE) or not os.path.exists(self.LSH_FILE):
            self.build_index()
        else:
            self.load_lsh()
            self.load_minhash()

    def _build_lsh(self, minhashes):
        print("Building LSH")
        self.lsh = LSH(minhashes)
        with open(self.LSH_FILE, 'wb') as f:
            pickle.dump(self.lsh.hash_tables, f)

        print("Built LSH Successfully")

    def build_index(self):
        self.minhashes = {}

        print("Building Minhashes")
        for file_name in os.listdir(self.CORPUS_DIR):
            file_name = os.path.join(self.CORPUS_DIR, file_name)

            if(file_name.endswith('.txt')):
                hash_vector = vectorize_file(file_name)
                signature = Minhash(hash_vector)
                self.minhashes[file_name] = signature

        with open(self.MINHASH_FILE, 'wb') as f:
            pickle.dump(self.minhashes, f)

        print("Successfully build minhashes")
        self._build_lsh(self.minhashes)

    def load_minhash(self):
        with open(self.MINHASH_FILE, 'rb') as f:
            self.minhashes = pickle.load(f)

    def load_lsh(self):
        with open(self.LSH_FILE, 'rb') as f:
            data = pickle.load(f)
            self.lsh = LSH(table=data)
