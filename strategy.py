import talib
import pandas as pd
import numpy as np

def Data(df):
    df['RSI1'] = talib.RSI(df['close'], timeperiod=13)
    df['RSI2'] = talib.RSI(df['close'], timeperiod=21)
    return df

#len(df) > 555555
df = pd.read_csv('m15_candle.csv')
for i in range(0, len(df)):
    t = df.at[i, 'time']
    if t.hour == 0 and t.minute == 0:
        df = df[i:]
        break

df = df.set_index('time')
ohlc = {
    'open': 'first',
    'high': 'max',
    'low': 'min',
    'close': 'last'
}

rsi1 = [0]*len(df)
rsi2 = [0]*len(df)
for i in range(100000, len(df)):
    h1 = Data(df[:i].resample("1h", offset=0).apply(ohlc).dropna())
    rsi1[i] = h1.iloc[-1]['RSI1'] 
    rsi2[i] = h1.iloc[-1]['RSI2'] 

df['RSI1_h1'] = rsi1
df['RSI2_h1'] = rsi2
df = df.reset_index()
df.to_csv("data.csv", index = False)
