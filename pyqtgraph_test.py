
import pandas as pd
import numpy as np
import pyqtgraph as pg


r = pd.date_range(start='1/1/2018', periods=1000, freq='S')
ts = pd.Series(np.random.randn(len(r)), index=r)
ts2 = pd.Series(np.random.randn(len(r)), index=r)

p1 = pg.plot()
p1.plot(ts)
p1.plot(ts2)
pg.show()
pg.QtGui.QApplication.exec_()

