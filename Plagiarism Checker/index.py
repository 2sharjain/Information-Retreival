import os
import pickle
from preprocess import vectorize, process_doc
from minhash import Minhash
from lsh import LSH
from inverted import TFIDF


class Index:
    '''
        This class handles all the indices created which are TF-IDF and LSH.

        Takes in a config dictionary and loads or creates the index if the files
        are already present and if not present respectively
    '''

    def __init__(self, config: dict):
        self.MINHASH_FILE = config.get('MINHASH_FILE', None)
        self.LSH_FILE = config.get('LSH_FILE', None)
        self.CORPUS_DIR = config.get('CORPUS_DIR', None)
        self.TFIDF_FILE = config.get('TFIDF_FILE', None)

        if not all(map(os.path.exists, config.values())):
            self.build_index()
        else:
            self.load_lsh()
            self.load_minhash()
            self.load_tfidf()

    def _build_lsh(self, minhashes):
        '''
            Builds the LSH using the given minhash vectors
        '''
        self.lsh = LSH(minhashes)
        with open(self.LSH_FILE, 'wb') as f:
            pickle.dump(self.lsh.hash_tables, f)

    def build_index(self):
        '''
            Builds the indices. 
        '''
        self.minhashes = {}
        docs = self.get_docs()

        print("Building Minhashes")
        for doc in docs:
            hash_vector = vectorize(docs[doc])
            signature = Minhash(hash_vector)
            self.minhashes[doc] = signature

        with open(self.MINHASH_FILE, 'wb') as f:
            pickle.dump(self.minhashes, f)

        print("Successfully build minhashes")

        print("Building LSH")
        self._build_lsh(self.minhashes)
        print("Built LSH Successfully")

        self.build_idf(docs)

    def build_idf(self, docs):
        '''
            Builds the TF-IDF index for the given corpus
        '''
        processed = {}
        for doc in docs:
            processed[doc] = process_doc(docs[doc])

        self.idf = TFIDF(processed)

        with open(self.TFIDF_FILE, 'wb') as f:
            pickle.dump(self.idf, f)

        print("built tfidf successfully")

    def get_docs(self):
        '''
            Opens and reads all the files in the CORPUS_DIR and 
            returns the dict of {file_name:text} for all files.
        '''
        docs = {}
        for file_name in os.listdir(self.CORPUS_DIR):
            file_name = os.path.join(self.CORPUS_DIR, file_name)

            if(file_name.endswith('.txt')):
                with open(file_name, 'r') as f:
                    try:
                        with open(file_name, 'r') as f:
                            text = f.read()
                    except UnicodeDecodeError:
                        continue

            docs[file_name] = text

        return docs

    def load_minhash(self):
        '''
            Loads the Minhash vectors from the file.
        '''
        with open(self.MINHASH_FILE, 'rb') as f:
            self.minhashes = pickle.load(f)

    def load_lsh(self):
        '''
            Loads the buckets from the files and initalizes a LSH object using this 
            data.
        '''
        with open(self.LSH_FILE, 'rb') as f:
            data = pickle.load(f)
            self.lsh = LSH(table=data)

    def load_tfidf(self):
        '''
            Loads the TF-IDF object from the file.
        '''
        with open(self.TFIDF_FILE, 'rb') as f:
            self.idf = pickle.load(f)
