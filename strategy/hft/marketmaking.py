from trading.default import *
import pandas
from strategy.hft.dataframe.notconcludedmedostockdata import *
from strategy.hft.dataframe.notconcludedmesustockdata import *
from strategy.hft.dataframe.hogapricedata import *
from strategy.hft.dataframe.hogareceivedata import *
import threading



class AllMedoStock(StockData):
    def medoAllStock(self):
        mystock = self.myStockData.returnData()
        for i in range(mystock):
            code = mystock['종목코드'].iloc[i]
            code = Code.standard(self, code)
            quantity = mystock['보유수량'].iloc[i]
            SijangMedoOrder.request(self, sCode=code, medoStockNum=quantity)

class TransactionNumber:
    def __init__(self):
        self.defaultTransactionNumber = 0
        self.nowTransactionNumber = 0

    def getNowNumber(self):
        return self.nowTransactionNumber

    def getDefaultNumber(self):
        return self.defaultTransactionNumber

    def setDefaultNumber(self, trasactionNumber):
        self.defaultTransactionNumber = trasactionNumber

    def addNowNumber(self):
        self.nowTransactionNumber += 1

    def isOutofNumber(self):
        return self.nowTransactionNumber > self.defaultTransactionNumber

class ShotUpStrategy(StockData, TrRequestBase):
    def request(self):
        index, conditionName = self.conditionData.findData(0)
        RealCondition.request(self, index=index, conditionName=conditionName)

class MarketMakingData():
    def __init__(self):
        self.notConMesuDf = NotConcludedMesuStockData()
        self.notConMedoDf = NotConcludedMedoStockData()
        self.hogaPriceDf = HogaPriceData()
        self.hogaReceiveDf = HogaReceiveData()
        self.trasaction = TransactionNumber()
        self.defaultOrderQuantity = 2
        self.defaultMesuHogaIndex = 10
        self.defaultMedoHogaIndex = 9



class InCondition(MarketMakingData):
    def conditionIn(self, code):
        if not self.isHogaReceiveDf.hasData(code):
            self.isHogaReceiveDf.inputDefaultData(code)
            SijangMesuOrder.request(self, sCode=code, mesuStockNum=self.defaultOrderQuantity)
            Hoga.request(self, code)
            self.trasaction.addNowNumber()

class JijungHogaMesuOrder(MarketMakingData):
    def request(self, code, mesuIndex, mesuStockNum):




class MarketMaking(DefaultTrading, AllMedoStock, MarketMakingData, InCondition):
    def __init__(self):
        super().__init__()
        self.trasaction.setDefaultNumber(5)

        JangCheck.request(self)


    def receiveOnReceiveReal(self, sCode, sRealType, sRealData):
        if sRealType == "장시작시간":
            status = JangStatus.receive(self,sCode, sRealType)
            if status == '0':
                self.logging.logger.debug('장 시작 전')

            elif status == '3':
                self.logging.logger.debug('장 시작')
                Line.sendMessage(self, '장 시작')
                ShotUpStrategy.request(self)



            elif status == '2':
                self.logging.logger.debug('장 종료후 동시호가')

            elif status == '4':
                self.logging.logger.debug('3시 30분 장 종료')


        elif sRealType == "주식체결":
            pass
        elif sRealType == '주식호가잔량':
            hogaList = HogaPrice.receive(self, sCode = sCode, sRealType=sRealType)
            self.hogaPriceDf.appendColumnData(hogaList= hogaList)
            if not self.hogaReceiveDf.isReceive(code=sCode):
                self.hogaReceiveDf.modifyIsHogaReceiveTrue(code=sCode)

    def receiveOnReceiveChejan(self, sGubun, nItemCnt, sFidList):
        if int(sGubun) == 0:  # 주문체결
            pass
        elif int(sGubun) == 1:  # 잔고
            pass


    def receiveOnReceiveRealCondition(self, strCode, strType, strConditionName, strConditionIndex):
        code, type = self.receiveConditionRealStock(strCode, strType, strConditionName, strConditionIndex)
        if type == 'I':
            self.logging.logger.debug("조건 편입: "+ code)
            if not self.trasaction.isOutofNumber():
                self.conditionIn(code = code)


        elif type == 'D':
            pass

