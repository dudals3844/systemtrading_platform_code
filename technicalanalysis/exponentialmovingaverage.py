import  pandas as pd
import matplotlib.pyplot as plt

class ExponentialMovingAverage:
    def __init__(self, code, day):
        self.code = code
        self.priceDataFrame = self.readPriceDataFrame()
        # 최근 날짜가 제일 밑으로 다시 정렬
        self.priceDataFrame = self.priceDataFrame.sort_index(ascending=False)
        self.priceDataFrame.reset_index(drop=True, inplace=True)

        self.day = day
        self.exponentialMovingAverage = self.calculateExponentialMovingAverage()
        # self.day = 20
        # self.test = self.calculateExponetialMovingAverage()
        plt.plot(self.priceDataFrame['현재가'])
        plt.plot(self.exponentialMovingAverage, color = 'red')
        # plt.plot(self.test)
        plt.show()


    def readPriceDataFrame(self):
        #priceDataFrame = pd.read_excel('C:/Users/PC/PycharmProjects/systemtrading_platform/db/price/'+self.companyName+'.xlsx')
        priceDataFrame = pd.read_csv("C:/Users/PC/PycharmProjects/systemtrading_platform/db/tickprice/"+self.code+".csv")

        return priceDataFrame

    def calculateExponentialMovingAverage(self):
        exponetialMovingAverage = self.priceDataFrame['현재가'].ewm(self.day).mean()
        return exponetialMovingAverage

    def getExponentialMovingAverage(self):
        return self.exponentialMovingAverage


if __name__ == '__main__':
    ExponentialMovingAverage('005930', 5)