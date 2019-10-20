import pickle
import math


class TFIDF:
    def __init__(self, docs):
        self.df = {}
        self.N = len(docs)
        self.vectors = {}

        self._get_basis(docs)
        for doc in docs:
            self.vectors[doc] = self.to_vector(docs[doc])

    def _get_basis(self, docs):
        self.basis = set()
        for doc in docs:
            for word in docs[doc]:
                self.basis.add(word)
                self.df[word] = 1

        self.basis = list(self.basis)

    def __compare(self, v1, v2):
        return self.cosine(v1, v2)

    def find_similar(self, doc):
        vector = self._to_vector(doc)

    def to_vector(self, doc):
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
        score = 0
        for i in range(len(self.basis)):
            score += vector1[i] * vector2[i] * \
                math.log(self.N / (1 + self.df[self.basis[i]]))

        return score
