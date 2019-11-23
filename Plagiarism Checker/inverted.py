import pickle
import math


class TFIDF:
    '''
        Creates TFIDF index from a given dict of docs and their word frequency.
    '''

    def __init__(self, docs):
        self.df = {}  # doc frequency for words present in the corpus

        self.N = len(docs)  # number of docs
        self.vectors = {}   # vectors generated from the given corpus

        self._get_basis(docs)
        for doc in docs:
            self.vectors[doc] = self.to_vector(docs[doc])

    def _get_basis(self, docs):
        '''
            Finds the dimensions by analyzing every document.
        '''
        self.basis = set()
        for doc in docs:
            for word in docs[doc]:
                self.basis.add(word)
                self.df[word] = self.df.get(word, 0) + 1    # inc doc frequency

        self.basis = list(self.basis)

    def __compare(self, v1, v2):
        return self.cosine(v1, v2)

    def find_similar(self, doc):
        vector = self._to_vector(doc)

    def to_vector(self, doc):
        '''
            Creates a vector of the given document using the basis.
        '''
        vector = []
        magnitude = 0

        for word in self.basis:
            freq = doc.get(word, 0)
            vector.append(freq)
            magnitude += freq ** 2

        magnitude = magnitude**0.5

        vector = [x/magnitude for x in vector]  # unit vector
        return vector

    def cosine(self, vector1, vector2):
        '''
            Calculates cosine distance
        '''
        score = 0
        for i in range(len(self.basis)):
            score += vector1[i] * vector2[i] * \
                math.log(self.N / (1 + self.df[self.basis[i]]))

        return score
