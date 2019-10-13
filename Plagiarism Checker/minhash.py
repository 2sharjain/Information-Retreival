import random
import os

_N = 100
_HASHES = []
_PRIME = 4294967311

# CHANGE ALL OF THIS


def _generate_random():
    for _ in range(100):
        _HASHES.append((random.randrange(0, (2**32)),
                        random.randrange(0, (2**32))))


def _get_hash_vals():
    if not os.path.exists('hashes'):
        _generate_random()

        with open('hashes', 'w') as f:
            for pair in _HASHES:
                f.writelines('{} {}\n'.format(*pair))

    else:
        with open('hashes', 'r') as f:
            lines = f.readlines()
            for i in range(100):
                _HASHES.append(list(map(int, lines[i].split())))


_get_hash_vals()

# END CHANGE


class Minhash:
    def __init__(self, input_vector):
        self.__vector = [float('inf')] * _N
        self._minhash(input_vector)

    def __getitem__(self, given):
        if (isinstance(given, slice)):
            return self.__vector[given.start:given.stop:given.step]

        return self.__vector[given]

    def size(self):
        return len(self.__vector)

    def _minhash(self, input_vector):
        for element in input_vector:
            assert (isinstance(element, int))

            for i, weights in enumerate(_HASHES):
                a, b = weights
                output = (a * element + b) % _PRIME

                self.__vector[i] = min(self.__vector[i], output)

    def compare(self, other):
        assert (isinstance(other, Minhash))

        similarity = 0
        for i in range(_N):
            similarity += 1 if self[i] == other[i] else 0

        similarity = round(similarity / _N, 3)
        return similarity
