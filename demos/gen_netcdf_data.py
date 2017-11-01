
""" Generate a bunch of netcdf data to work with """


import numpy as np
from scipy.io import netcdf

time = np.arange(0, 10, 0.01)
s1 = 5 * np.sin(time*2) + 2
s2 = 3 * np.cos(time*4) - 1

# print(time, time.shape, s1, s1.shape)


with netcdf.netcdf_file('woot.netcdf', 'w') as f:
    f.createDimension('time', time.shape[0])
    time_var = f.createVariable('time', np.float64, ('time',))
    time_var.units = 'seconds since yesterday'
    time_var[:] = time
    s1_var = f.createVariable('s1', np.float64, ('time',))
    s1_var[:] = s1
    s2_var = f.createVariable('s2', np.float64, ('time',))
    s2_var[:] = s2


