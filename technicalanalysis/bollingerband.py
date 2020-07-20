import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
from kiwoom.handledata.minuteprice import *

## 차트의 정석 109p
class BollingerBand:
    def __init__(self, code, day = 20):
        self.day = day
        #self.code = code
        #self.priceDataFrame = self.readPriceDataFrame()

        # 최근 날짜가 제일 밑으로 다시 정렬
        self.priceDataFrame = self.readPriceDataFrame()

        self.movingAverage = self.calculateMovingAverage()
        self.lowerBol = self.calculateLowerBol()
        self.upperBol = self.calculateUpperBol()

        plt.plot(self.priceDataFrame['현재가'])
        plt.plot(self.upperBol, color = 'red')
        plt.plot(self.lowerBol, color = 'blue')
        plt.show()

    def readPriceDataFrame(self):
        # priceDataFrame = pd.read_excel('C:/Users/PC/PycharmProjects/systemtrading_platform/db/price/'+self.companyName+'.xlsx')
        priceDataFrame = pd.read_csv("C:/Users/PC/PycharmProjects/systemtrading_platform/db/tickprice/014160.csv")
        return priceDataFrame

    def calculateMovingAverage(self):
        movingAverage = self.priceDataFrame['현재가'].rolling(window=self.day).mean()
        return movingAverage

    def calculateUpperBol(self):
        upperBol = self.movingAverage + 2 * self.priceDataFrame['현재가'].rolling(window=self.day).std()
        return upperBol

    def calculateLowerBol(self):
        lowerBol = self.movingAverage - 2 * self.priceDataFrame['현재가'].rolling(window=self.day).std()
        return lowerBol

    def getUpperBol(self):
        return self.upperBol

    def getLowerBol(self):
        return self.lowerBol


if __name__ == '__main__':
    BollingerBand("035470")