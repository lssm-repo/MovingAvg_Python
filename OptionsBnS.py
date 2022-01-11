# Kelvin NO 講投資
# Python 教學 期權計算機 個人期權策略公開 VHSI 恆指 Python 程式交易 分析 Option Calculator using Python Python 好好用 EP5
# https://www.youtube.com/watch?v=hKwKYEQgTIw&list=PLMT0fZzvcXJBiZLblsT_G18OxkXHtKe5x&index=5

import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader.data as web

import numpy as np
import scipy.stats as ss
import time 

'''
Black and Scholes
'''
def d1(S0, K, r, sigma, T):
    return (np.log(S0/K) + (r + sigma**2 / 2) * T)/(sigma * np.sqrt(T))
 
def d2(S0, K, r, sigma, T):
    return (np.log(S0 / K) + (r - sigma**2 / 2) * T) / (sigma * np.sqrt(T))
 
def BlackScholes(type,S0, K, r, sigma, T):
    if type=="C":
        return S0 * ss.norm.cdf(d1(S0, K, r, sigma, T)) - K * np.exp(-r * T) * ss.norm.cdf(d2(S0, K, r, sigma, T))
    else:
       return K * np.exp(-r * T) * ss.norm.cdf(-d2(S0, K, r, sigma, T)) - S0 * ss.norm.cdf(-d1(S0, K, r, sigma, T))


# EDIT  csv obtain from investing.com 
data = pd.read_csv('vhsi_test.csv') 

data['Target'] = 0
data['Oprice'] = 0.0
data['Danger'] = ""


for i in range (0,len(data)-30):
    Target = data['Close'].values[i]/200
    Target = int(Target) * 200

    S0 = data['Close'].values[i]
    #K = Target # ENTER later
    r= 0.0021-0.0383
    sigma = data['VHSI'].values[i] * 1.2 / 100
    T = 40/365 
    Otype='P' 
# EDIT  P for Put, C for Call 

    for p in range (0,25):
        Oprice = BlackScholes(Otype,S0, Target, r, sigma, T)
        
# EDIT  modify 30 改期權金 
        if Oprice > 30:
                data['Target'].values[i] = Target
                data['Oprice'].values[i] = Oprice
                Target = Target - 200
    lowestclose = 100000.0
# EDIT 30 個交易日 MODIFY
    for q in range (0,30):
        todayprice = data['Close'].values[i+q]
        if Target > todayprice and todayprice < lowestclose:
                lowestclose = todayprice
                data ['Danger'].values[i] = "Danger " + str(int(lowestclose))


print(data.head(10))
data.to_csv('vhsi_final.csv')
