from django.shortcuts import render
import requests
import numpy as np
import pandas as pd

def homepage(request):

    headers = {'Content-Type': 'application/json'}
    ticker = "spy"
    token = "2275a827410dd3dd64a3ba53e96ab66e77436939"
    startDate = "1993-01-22"
    requestResponse = requests.get(f"https://api.tiingo.com/tiingo/daily/{ticker}/prices?startDate={startDate}&token={token}",
                                   headers=headers)

    x = []
    for i in requestResponse.json():
        x.append(i)

    df = pd.DataFrame(x)
    returns = np.log(df['adjClose'][1:]/df['adjClose'].shift(1)[1:])
    u = np.log(df['adjHigh']/df['adjOpen'])
    d = np.log(df['adjLow']/df['adjOpen'])
    c = np.log(df['adjClose']/df['adjOpen'])
    Volatility_target = returns.var()
    Volatility_20D = returns.rolling(window=20).var()
    Volatility_21D = returns.rolling(window=21).var()
    Average_20D = returns.rolling(window=20).mean()
    Mth_hedge = (Volatility_target/Volatility_20D)
    Mth_hedge_AfterHours = (Volatility_target/Volatility_21D)**0.5

    context = {'Volatility_target': Volatility_target,
               'Volatility_20D': Volatility_20D.to_numpy()[-1],
               'Average_20D': Average_20D.to_numpy()[-1],
               'Mth_hedge': Mth_hedge.to_numpy()[-1],
               'Mth_hedge_AfterHours': np.round(Mth_hedge_AfterHours.to_numpy()[-1],2),
               }

    return render(request,
                  'main/home.html',
                  context)

