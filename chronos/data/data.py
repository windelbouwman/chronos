import h5py
import pandas as pd
import numpy as np


def load_data(filename):
    f = h5py.File(filename, "r")
    data = f["first"]
    # print(data, type(data))
    f.close()

    r = pd.date_range(start="1/1/2018", periods=1000, freq="S")
    ts = pd.Series(np.random.randn(len(r)), index=r)

    data = ts
    return data
