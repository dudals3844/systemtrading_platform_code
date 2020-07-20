import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

#124p
class DoubleExponentialMovingAverage:
    def __init__(self, code, day):
        self.con = sqlite3.connect('C:/Users/PC/PycharmProjects/systemtrading_platform/db/DayPrice.db')
        self.code = code
        self.priceDataFrame = self.readPriceDataFrame()
        # 최근 날짜가 제일 밑으로 다시 정렬
        self.priceDataFrame = self.priceDataFrame.sort_index(ascending=False)
        self.priceDataFrame.reset_index(drop=True, inplace=True)

        self.day = day
        self.firstExponentialMovingAverage = self.calculateExponentialMovingAverage(self.priceDataFrame['종가'])
        self.secondExponentialMovingAverage = self.calculateExponentialMovingAverage(self.firstExponentialMovingAverage)
        self.doubleExponentialMovingAverage = self.calculateDoubleExponentialMovingAverage()

        # plt.plot(self.doubleExponentialMovingAverage,color = 'red')
        # plt.plot(self.priceDataFrame['종가'])
        # plt.show()

    def readPriceDataFrame(self):
        code = "DAY_"+self.code+"_TB"
        priceDataFrame = pd.read_sql('select * from '+code, con=self.con)
        return priceDataFrame

    def calculateExponentialMovingAverage(self, priceDataFrame):
        exponetialMovingAverage = priceDataFrame.ewm(self.day).mean()
        return exponetialMovingAverage

    def calculateDoubleExponentialMovingAverage(self):
        doubleExponentialMovingAverage = 2 * self.firstExponentialMovingAverage - self.secondExponentialMovingAverage
        return doubleExponentialMovingAverage

    def getDoubleExponentialMovingAverage(self):
        return self.doubleExponentialMovingAverage


if __name__ == '__main__':
    DoubleExponentialMovingAverage('005930', 20)