import talib
import pandas as pd

def Data(df):
    df['RSI1'] = talib.RSI(df['close'], timeperiod=13)
    df['RSI2'] = talib.RSI(df['close'], timeperiod=21)
    df['RSI3'] = talib.RSI(df['close'], timeperiod=34)
    df['RSI4'] = talib.RSI(df['close'], timeperiod=55)
    df['RSI5'] = talib.RSI(df['close'], timeperiod=89)
    return df

#len(df) > 100000
df = pd.read_csv('m15_candle.csv')
for i in range(0, len(df)):
    t = df.at[i, 'time']
    if t.hour == 0:
        df = df[i:]
        break

df = df.set_index('time')

ohlc = {
    'open': 'first',
    'high': 'max',
    'low': 'min',
    'close': 'last'
}

signal = [0]*len(df)

for i in range(0, len(df)):
    h1 = Data(df[:i].resample('1h', offset=0).apply(ohlc).dropna())
    h4 = Data(df[:i].resample('4h', offset=0).apply(ohlc).dropna())
    d1 = Data(df[:i].resample('d', offset=0).apply(ohlc).dropna())
    w1 = Data(df[:i].resample('w', offset=0).apply(ohlc).dropna())
    if (all(w1.iloc[-1][col] > 80 for col in ['RSI1', 'RSI2', 'RSI3', 'RSI4', 'RSI5'])
        and all(h1.iloc[-1][col] > 80 for col in ['RSI1', 'RSI2', 'RSI3', 'RSI4', 'RSI5'])
        and all(h4.iloc[-1][col] > 80 for col in ['RSI1', 'RSI2', 'RSI3', 'RSI4', 'RSI5'])
        and all(d1.iloc[-1][col] > 80 for col in ['RSI1', 'RSI2', 'RSI3', 'RSI4', 'RSI5'])):
            signal[i] = 1
    elif (all(w1.iloc[-1][col] < 20 for col in ['RSI1', 'RSI2', 'RSI3', 'RSI4', 'RSI5'])
        and all(h1.iloc[-1][col] < 20 for col in ['RSI1', 'RSI2', 'RSI3', 'RSI4', 'RSI5'])
        and all(h4.iloc[-1][col] < 20 for col in ['RSI1', 'RSI2', 'RSI3', 'RSI4', 'RSI5'])
        and all(d1.iloc[-1][col] < 20 for col in ['RSI1', 'RSI2', 'RSI3', 'RSI4', 'RSI5'])):
            signal[i] = 2

df['signal'] = signal
df = df.reset_index()
df.to_csv("data.csv", index = False)
