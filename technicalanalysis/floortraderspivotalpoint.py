import pandas as pd
import matplotlib.pyplot as plt
## 책 115p
class FloorTradersPivotalPoint:
    def __init__(self, companyName, high, low, nowPrice):
        self.companyName = companyName
        self.high = high
        self.low = low
        self.nowPrice = nowPrice
        self.priceDataFrame = self.readPriceDataFrame()
        # 최근 날짜가 제일 밑으로 다시 정렬
        self.priceDataFrame = self.priceDataFrame.sort_index(ascending=False)
        self.priceDataFrame.reset_index(drop=True, inplace=True)

        self.pivotalPoint = self.calculatePivotalPoint()
        self.firstResistanceLine = self.calculateFirstResistanceLine()
        self.firstSupportLine = self.calculateFirstSupportLine()
        self.secondResistanceLine = self.calculateSecondResistanceLine()
        self.secondSupportLine = self.calculateSecondSupportLine()

    def readPriceDataFrame(self):
        priceDataFrame = pd.read_excel('C:/Users/PC/PycharmProjects/systemtrading_platform/db/price/'+self.companyName+'.xlsx')
        return priceDataFrame

    def calculatePivotalPoint(self):
        pivotalPoint = (self.high + self.low + self.nowPrice) / 3
        return pivotalPoint

    def calculateFirstResistanceLine(self):
        firstResistanceLine = 2 * self.pivotalPoint - self.priceDataFrame['저가'].iloc[0]
        return firstResistanceLine

    def calculateFirstSupportLine(self):
        firstSupportLine = 2 * self.pivotalPoint - self.priceDataFrame['고가'].iloc[0]
        return firstSupportLine

    def calculateSecondResistanceLine(self):
        secondResistanceLine = self.pivotalPoint + (self.priceDataFrame['고가'].iloc[0] - self.priceDataFrame['저가'].iloc[0])
        return secondResistanceLine

    def calculateSecondSupportLine(self):
        secondSupportLine = self.pivotalPoint - (self.priceDataFrame['고가'].iloc[0] - self.priceDataFrame['저가'].iloc[0])
        return  secondSupportLine


    def getFirstResistanceLine(self):
        return self.firstResistanceLine

    def getFirstSupportLine(self):
        return self.firstSupportLine

    def getSecondResistanceLine(self):
        return self.secondResistanceLine

    def getSecondSupportLine(self):
        return self.secondSupportLine



