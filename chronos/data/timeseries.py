""" Time series database like structures.

Ideas from here: https://akumuli.org/
"""

import logging
logger = logging.getLogger('time-series')


class TimeSeries:
    """ A time series. """
    def __init__(self):
        self._root_node = Leaf()
    
    def __len__(self):
        return len(self._root_node)
    
    def append(self, sample):
        """ Add a sample to this time series. """
        if self._root_node.is_full:
            logger.debug('Root is full %s, creating new intermediate as new root', len(self._root_node))
            print(self._root_node)
            new_root = Intermediate(self._root_node.level + 1)
            new_root.add_chunk(self._root_node)
            self._root_node = new_root

        self._root_node.append(sample)

    def first_sample(self):
        """ Retrieve the first ever sample. """
        node = self._root_node
        while node.level > 0:
            node = node._sub_chunks[0]
        return node.samples[0]

    def last_sample(self):
        """ Retrieve the last sample in this series. """
        node = self._root_node
        while node.level > 0:
            node = node._sub_chunks[-1]
        return node.samples[-1]

    def get_leafs_in_range(self, timespan):
        """ Get all leaf nodes within the given range. """
        leafs = []
        for leaf in self._root_node.all_leafs():
            if leaf.is_empty:
                continue

            if leaf.end < timespan.begin:
                continue

            if timespan.end < leaf.begin:
                break
            
            leafs.append(leaf)
        return leafs

    def get_samples(self, timespan, max_samples=3000):
        """ Retrieve series of samples within the given timespan. """
        samples = []
        for leaf in self.get_leafs_in_range(timespan):
            samples.extend(leaf.samples)
            if len(samples) > max_samples:
                # Too much data! Plot will choke on this ...
                break
        return samples


class Intermediate:
    """ An intermediate level. """
    fanout = 13

    def __init__(self, level):
        self.level = level
        self._sub_chunks = []

    def __repr__(self):
        return 'Intermediate at level {}'.format(self.level)

    def __len__(self):
        return sum(len(c) for c in self._sub_chunks)

    def __iter__(self):
        for c in self._sub_chunks:
            for sample in c:
                yield sample

    def all_leafs(self):
        for chunk in self._sub_chunks:
            for leaf in chunk.all_leafs():
                yield leaf

    @property
    def is_full(self):
        return len(self._sub_chunks) >= self.fanout

    def append(self, sample):
        if self._sub_chunks:
            chunk = self._sub_chunks[-1]
            if chunk.is_full:
                # logger.debug('Chunk is full.')
                chunk = self.new_subchunk()
        else:
            chunk = self.new_subchunk()
        chunk.append(sample)

    def new_subchunk(self):
        new_level = self.level - 1
        if new_level == 0:
            # logger.debug('creating new leaf')
            chunk = Leaf()
        else:
            # logger.debug('creating new intermediate')
            chunk = Intermediate(new_level)
        self.add_chunk(chunk)
        return chunk

    def add_chunk(self, chunk):
        # logger.debug('Adding chunk at level %s', self.level)
        self._sub_chunks.append(chunk)


class Leaf:
    """ A chunk which actually contains samples.
    """
    capacity = 700

    def __init__(self):
        self.level = 0
        self.begin = None
        self.end = None
        self.samples = []

        # Aggregates:
        # TODO!
        # self.max_value

    @property
    def is_empty(self):
        return len(self.samples) == 0

    @property
    def is_full(self):
        return len(self.samples) >= self.capacity

    def __len__(self):
        return len(self.samples)

    def __iter__(self):
        for sample in self.samples:
            yield sample

    def all_leafs(self):
        yield self

    def append(self, sample):
        if not self.samples:
            self.begin = sample.timestamp
        self.samples.append(sample)
        self.end = sample.timestamp


__all__ = ['TimeSeries']