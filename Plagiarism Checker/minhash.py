import random
import os
import pickle


class Minhash:
    '''
        Represents a Minhash vector. Creates a minhash vector from a given vector.
        Also used to find similar vectors using jaccard metric.
    '''
    _N = 100
    _PRIME = 4294967311

    @staticmethod
    def _get_hash_vals():
        '''
            Generates 100 random hash function weights.
        '''
        if not os.path.exists('hashes.pkl'):
            hashes = []
            for _ in range(100):
                hashes.append((random.randrange(0, (2**32)),
                               random.randrange(0, (2**32))))

            with open('hashes.pkl', 'wb') as f:
                pickle.dump(hashes, f)
        else:
            with open('hashes.pkl', 'rb') as f:
                hashes = pickle.load(f)

        return hashes

    _HASHES = _get_hash_vals.__func__()

    def __init__(self, input_vector):
        self.__vector = [float('inf')] * self._N
        self._minhash(input_vector)

    def __getitem__(self, given):
        if (isinstance(given, slice)):
            return self.__vector[given.start:given.stop:given.step]

        return self.__vector[given]

    def size(self):
        return len(self.__vector)

    def _minhash(self, input_vector):
        '''
            Creates minhash from the given vector and the 100 hash functions.
        '''
        for element in input_vector:
            assert (isinstance(element, int))

            for i, weights in enumerate(self._HASHES):
                a, b = weights
                output = (a * element + b) % self._PRIME

                self.__vector[i] = min(self.__vector[i], output)

    def compare(self, other):
        '''
            Returns jaccard score for two vectors
        '''
        assert (isinstance(other, Minhash))

        similarity = 0
        for i in range(self._N):
            similarity += 1 if self[i] == other[i] else 0

        similarity = round(similarity / self._N, 3)
        return similarity
