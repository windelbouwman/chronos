
import h5py

def load_data(filename):
    f = h5py.File(filename, 'r')
    data = f['first']
    f.close()
    return data