

import pandas as pd
import numpy as np


r = pd.date_range(start='1/1/2018', periods=1000, freq='S')
ts = pd.Series(np.random.randn(len(r)), index=r)


