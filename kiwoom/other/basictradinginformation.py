from config.log_class import *
from line.line import *

class BasicTradingInformation(Line):
    def __init__(self):
        self.deposit = None
        self.oneTradingDeposit = None
        # 거래종목수
        self.tradingNumber= None
        # 증거금률
        self.marginRate= None
        # 증거금을 이용한 종목수
        self.tradingNumberUsingMargin= None
        # 현재 거래 종목수
        self.nowTradingNumber = 0

    def setDeposit(self, deposit):
        self.deposit = deposit

    def setTradingNumber(self, tradingNumber):
        self.tradingNumber = tradingNumber
        Line.sendMessage(self, "오늘 최대 거래종목수: %s" % (self.tradingNumber))


    def setMarginRate(self, marginRate):
        self.marginRate = marginRate
        Line.sendMessage(self, "증거금률: %s" % (self.marginRate))

    def setNowTradingNumber(self, nowTradingNumber):
        self.nowTradingNumber = nowTradingNumber

    def getTradingNumber(self):
        tradingNumber = self.tradingNumber
        return tradingNumber

    def getNowTradingNumber(self):
        nowTradingNumber = self.nowTradingNumber
        return nowTradingNumber

    def getTradingNumberUsingMargin(self):
        tradingNumberUsingMargin = self.tradingNumberUsingMargin
        return tradingNumberUsingMargin

    def calculateOneTradingDeposit(self):
        self.oneTradingDeposit = int(self.deposit) / int(self.tradingNumber)


    def calculateTradingNumberUsingMargin(self):
        self.tradingNumberUsingMargin = int(100 / self.marginRate * self.tradingNumber)


    def getHowManyStockMesu(self, nowPrice):
        numberofStock = int(self.oneTradingDeposit / nowPrice)
        return numberofStock

    def getHowManyStockMedo(self, mystockNum):
        return mystockNum

