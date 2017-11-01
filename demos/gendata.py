
import h5py
import numpy as np

f = h5py.File('noize.hdf5', 'w')
dset = f.create_dataset('first', (100,), dtype='f')

dset[...] = np.arange(100)
print(dset)
print(dset[4])

