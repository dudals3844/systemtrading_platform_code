from config.log_class import *
from line.line import *

class Margin(Line):
    def __init__(self):
        self.marginRate = None

    def setRate(self, marginRate):
        Line.sendMessage(self, "증거금률: %s" % (self.marginRate))

    def getRate(self):
        return self.marginRate

class Transaction():
    def __init__(self):
        self.tradingNumber = None

    def setNumber(self, tradingNumber):
        self.tradingNumber = tradingNumber

    def getNumber(self):
        return self.tradingNumber