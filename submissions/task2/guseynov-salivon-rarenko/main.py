# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
import matplotlib.pylab as plt
from matplotlib.pylab import rcParams
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.stattools import acf, pacf

rcParams['figure.figsize'] = 15, 6


def dateparse(dates):
    return pd.datetime.strptime(dates, '%Y-%m-%d')


data1 = pd.read_csv('training.csv', parse_dates=['Date'], index_col='Date',
                    date_parser=dateparse)
data2 = pd.read_csv('testing.csv', parse_dates=['Date'], index_col='Date',
                    date_parser=dateparse)


ts = data1['Value']
plt.plot(ts)


def test_stationarity(timeseries):
    # Определяем скользящее среднее
    rolmean = pd.rolling_mean(timeseries, window=12)
    rolstd = pd.rolling_std(timeseries, window=12)

    plt.plot(timeseries, color='blue', label='Original')
    plt.plot(rolmean, color='red', label='Rolling Mean')
    plt.plot(rolstd, color='black', label='Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show(block=False)

    # Тест Дики - Фуллера:
    print('Results of Dickey-Fuller Test:')
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4],
                         index=['Test Statistic', 'p-value',
                                '#Lags Used',
                                'Number of Observations Used'])

    for key, value in dftest[4].items():
        dfoutput['Critical Value (%s)' % key] = value

    if dftest[0] > dftest[4]['5%']:
        print('NO')
        return 'NO'
    else:
        print('YES')
        return 'YES'

test_stationarity(ts)

# Разложение ряда на тренд, сезональность и остаток


decomposition = seasonal_decompose(ts)

trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

plt.subplot(411)
plt.plot(ts, label='Original')
plt.legend(loc='best')

plt.subplot(412)
plt.plot(trend, label='Trend')
plt.legend(loc='best')

plt.subplot(413)
plt.plot(seasonal, label='Seasonality')
plt.legend(loc='best')

plt.subplot(414)
plt.plot(residual, label='Residuals')
plt.legend(loc='best')

plt.tight_layout()

# Проверка на стационарность тренда
ts_t = trend
ts_t.dropna(inplace=True)
test_stationarity(ts_t)

ts_s = seasonal
ts_s.dropna(inplace=True)
test_stationarity(ts_s)

ts_r = residual
ts_r.dropna(inplace=True)
test_stationarity(ts_r)


def intK(timeseries):
    s = test_stationarity(timeseries)
    i = 0
    err = 1000
    while s == 'NO' and err:
        i += 1
        timeseries = timeseries.diff(periods=1).dropna()
        s = test_stationarity(timeseries)
        err -= 1
    if not err:
        return -1
    else:
        return i

k = intK(ts)
print(k)

# Логарифмируем ряд

ts_log = np.log(ts)
ts_log_diff = ts_log - ts_log.shift()

lag_acf = acf(ts_log_diff, nlags=20)
lag_pacf = pacf(ts_log_diff, nlags=20, method='ols')

# Plot ACF
plt.subplot(121)
plt.plot(lag_acf)
plt.axhline(y=0, linestyle='--', color='gray')
plt.axhline(y=-1.96 / np.sqrt(len(ts_log_diff)), linestyle='--', color='gray')
plt.axhline(y=1.96 / np.sqrt(len(ts_log_diff)), linestyle='--', color='gray')
plt.title('Autocorrelation Function')

# Plot PACF:

plt.subplot(122)
plt.plot(lag_pacf)
plt.axhline(y=0, linestyle='--', color='gray')
plt.axhline(y=-1.96 / np.sqrt(len(ts_log_diff)), linestyle='--', color='gray')
plt.axhline(y=1.96 / np.sqrt(len(ts_log_diff)), linestyle='--', color='gray')
plt.title('Partial Autocorrelation Function')
plt.tight_layout()

q = int(lag_acf[0])
p = int(lag_pacf[0])

# Применяем модель ARIMA

model = ARIMA(ts_log, order=(p, k, q))
results_ARIMA = model.fit(disp=-1)
plt.plot(ts_log_diff)
plt.plot(results_ARIMA.fittedvalues, color='red')
plt.title('RSS: %.4f' % sum((results_ARIMA.fittedvalues - ts_log_diff) ** 2))
