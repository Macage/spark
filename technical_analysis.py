import pandas as pd
import numpy as np
import tushare as ts
import matplotlib.pyplot as plt

hs300 = pd.read_csv('hs300.csv')
hs300 = hs300.set_index('date')
hs300.sort_index(inplace=True)
#print(hs300.info())
hs300['42d'] = np.round(pd.rolling_mean(hs300['close'], window=30), 2)
hs300['252d'] = np.round(pd.rolling_mean(hs300['close'], window=60), 2)
hs300['42-252'] = hs300['42d'] - hs300['252d']
hs300['Regime'] = np.where(hs300['42-252'] > 50, 1, 0)
hs300['Regime'] = np.where(hs300['42-252'] < -50, -1, hs300['Regime'])
print(hs300['Regime'].value_counts())
hs300['Market'] = np.log(hs300['close'] / hs300['close'].shift(1))
hs300['Strategy'] = hs300['Regime'].shift(1) * hs300['Market']
hs300[['Market', 'Strategy']].cumsum().apply(np.exp).plot(grid=True, figsize=(8, 5))
#hs300[['close', '42d', '252d']].plot(grid=True, figsize=(8, 5))
#hs300['Regime'].plot(lw=1.5)
#plt.ylim([-1.1, 1.1])
plt.show()
