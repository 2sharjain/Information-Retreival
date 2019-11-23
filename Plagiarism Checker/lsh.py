from zlib import crc32


class Hashtable:
    '''
        Class representing a hashtable which hashes docs to a bucket.
    '''
    buckets = 100

    def __init__(self):
        self._arr = [[]] * self.buckets

    def __getitem__(self, index):
        return self._arr[index]

    def insert(self, element_id, element):
        bucket = self.get_bucket(element)

        self._arr[bucket] = self._arr[bucket] or []
        self._arr[bucket].append(element_id)

    @classmethod
    def get_bucket(cls, element):
        return crc32(bytes(element, 'utf-8')) % cls.buckets


class LSH:
    '''
        Builds the LSH from the given minhashes. Also Finds the elements in the same bucket for 
        a given minhash vector.
    '''

    def __init__(self, minhash_index=None, table=None):
        self.index = {}

        self.hash_tables = []
        if table is None and minhash_index is not None:
            self.process(minhash_index)
        else:
            self.hash_tables = table

    def show(self):
        for band in self.hash_tables:
            for bucket in band:
                print(bucket)

    def process(self, minhash_index):
        '''
            Hashes elements in different bands to buckets.
        '''
        band_size = 4
        pos = 0
        dim = 100

        while pos < dim // band_size:
            table = Hashtable()

            for doc in minhash_index:
                current_doc = minhash_index[doc]
                band = "".join(
                    map(str, current_doc[pos*band_size: pos*band_size + band_size]))

                table.insert(doc, band)

            pos += 1
            self.hash_tables.append(table)

    def get_similar(self, vector):
        # TODO: Refactor this method

        result = []
        pos = 0
        dim = 100
        band_size = 4

        while pos < dim // band_size:
            band = "".join(
                map(str, vector[pos*band_size: pos*band_size + band_size]))

            bucket = Hashtable.get_bucket(band)
            elems = self.hash_tables[pos][bucket]

            if elems is not None:
                result.extend(elems)

            pos += 1

        return set(result)
