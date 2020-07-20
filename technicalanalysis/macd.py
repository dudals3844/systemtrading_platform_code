import pandas as pd
import sqlite3
from kiwoom.other.standard import *

class MovingAverageConvergenceDivergence:
    def __int__(self, code):
        self.con = sqlite3.connect('db/TickPrice.db')
        code = Standard.standardCode(code)
        self.tickPriceDataFrame = self.readTickData(code)
        ema9 = self.calculateExponentialMovingAverage(self.tickPriceDataFrame, 9)
        ema26 = self.calculateExponentialMovingAverage(self.tickPriceDataFrame, 26)
        self.macd = ema9 - ema26
        self.signal = self.calculateExponentialMovingAverage(self.macd, 13)



    def calculateExponentialMovingAverage(self, priceDataFrame, day):
        exponetialMovingAverage = priceDataFrame.ewm(day).mean()
        return exponetialMovingAverage

    def readTickData(self, code):
        TickDataFrame = pd.read_sql('select * from'+code, con = self.con)
        return TickDataFrame

    def getMACD(self):
        return self.macd

    def getSignal(self):
        return self.signal