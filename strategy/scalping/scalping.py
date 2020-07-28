from trading.trading import *
from kiwoom.other.transaction import *
import time
from line.line import *
import sys

class Scalping(Trading):
    def __init__(self):
        super().__init__()
        BasicTradingInformation.setDeposit(self, Tr.getDeposit(self))
        BasicTradingInformation.setMarginRate(self, 40)
        BasicTradingInformation.setTradingNumber(self, 100)
        BasicTradingInformation.calculateTradingNumberUsingMargin(self)
        BasicTradingInformation.calculateOneTradingDeposit(self)
        self.conditionList = []
        Real.requestRealJangCheck(self)
        #self.requestIncreaseVolumeCondition()
        self.requestMovingAverageBreakthroughCondition()
        self.startSpreadRate = None



    def requestIncreaseVolumeCondition(self):
        index, conditionName = self.condition.isReceive(5)
        self.requestRealCondition(index, conditionName)

    def requestMovingAverageBreakthroughCondition(self):
        index, conditionName = self.condition.isReceive(1)
        self.requestRealCondition(index, conditionName)

    # Override
    def receiveRealdataSlot(self, sCode, sRealType, sRealData):
        if sRealType == "장시작시간":
            status = Real.receiveJangStatus(self, sCode, sRealType)
            if status == '0':
                self.logging.logger.debug('장 시작 전')

            elif status == '3':
                self.logging.logger.debug('장 시작')
                Line.sendMessage(self, '장 시작')
                self.medoAllStock()



            elif status == '2':
                self.logging.logger.debug('장 종료후 동시호가')
                self.medoAllStock()

            elif status == '4':
                self.logging.logger.debug('3시 30분 장 종료')
                sys.exit()

        elif sRealType == "주식체결":

            chegulTime, nowPrice, spread, spreadRate, medoHoGa, mesuHoGa, volume, volumeSum, high, start, low  = Real.receiveChegulPrice(self, sCode, sRealType)

            self.mesu(sCode,nowPrice, spreadRate)
            self.ikJeol(sCode, spreadRate)
            self.sonJeol(sCode, spreadRate)




    def receiveConditionRealSlot(self, strCode, strType, strConditionName, strConditionIndex):
        code, type = self.receiveConditionRealStock(strCode, strType, strConditionName, strConditionIndex)
        if type == 'I':
            code = self.standard.standardCode(code)
            if not self.hasConditionList(code):
                self.conditionList.append(code)
                #self.removeDuplicateConditionList()
                Real.requestRealChegulPrice(self, self.conditionList[0])
                self.tradingStatus.appendData(code,mesu=True)


        elif type == 'D':
            self.deleteConditionList(code)
            if self.myStock.hasData(code):
                medoNum = self.myStock.findStockQuantitiyData(code)
                Order.requestSijangMedoOrder(self, code, medoNum)
                self.tradingStatus.modifyMesuData(code, mesu=False)
                self.tradingStatus.modifyMedoData(code, medo=False)
            Disconnect.disconnectRealData(self, self.screenRealChegulPrice, code=code)

    def removeDuplicateConditionList(self):
        self.conditionList = list(set(self.conditionList))

    def hasConditionList(self,code):
        if code in self.conditionList:
            return True
        else:
            return False

    def deleteConditionList(self,code):
        try:
            idx = self.conditionList.index(code)
            del self.conditionList[idx]
        except:
            pass

    def mesu(self, sCode, nowPrice, spreadRate):
        if self.tradingStatus.isMesuData(sCode):
            if self.hasConditionList(sCode):
                Order.requestSijangMesuOrder(self, sCode, BasicTradingInformation.getHowManyStockMesu(self, nowPrice))
                self.startSpreadRate = spreadRate
                Line.sendMessage(self, "\n종목코드: %s\n시작등락률: %s"%(sCode, spreadRate))
                self.logging.logger.debug("종목코드: %s 시작등락률: %s"%(sCode, spreadRate))
                self.tradingStatus.modifyMesuData(sCode, mesu=False)
                self.tradingStatus.modifyMedoData(sCode, medo=True)


    def sonJeol(self, code, spreadRate):
        self.logging.logger.debug("손절: %s" % (spreadRate - self.startSpreadRate))

        if spreadRate - self.startSpreadRate <= -0.6:
            if self.tradingStatus.isMedoData(code):
                if self.myStock.hasData(code):
                    Line.sendMessage(self,
                                     "\n 손절 종목코드: %s\n시작등락률: %s\n현재등락률: %s" % (code, self.startSpreadRate, spreadRate))
                    self.logging.logger.debug(
                        "손절 종목코드: %s 시작등락률: %s 현재등락률: %s" % (code, self.startSpreadRate, spreadRate))

                    medoStockNumber = self.myStock.findStockQuantitiyData(code)
                    Order.requestSijangMedoOrder(self, code, medoStockNumber)
                    self.tradingStatus.modifyMedoData(code, medo=False)
                    self.tradingStatus.modifyMesuData(code, mesu=True)

    def ikJeol(self, code,spreadRate):
        self.logging.logger.debug("익절: %s"%(spreadRate - self.startSpreadRate))
        if spreadRate - self.startSpreadRate >= 0.8:
            if self.tradingStatus.isMedoData(code):
                if self.myStock.hasData(code):
                    Line.sendMessage(self,
                                     "\n 익절 종목코드: %s\n시작등락률: %s\n현재등락률: %s" % (code, self.startSpreadRate, spreadRate))
                    self.logging.logger.debug(
                        "익절 종목코드: %s 시작등락률: %s 현재등락률: %s" % (code, self.startSpreadRate, spreadRate))

                    medoStockNumber = self.myStock.findStockQuantitiyData(code)
                    Order.requestSijangMedoOrder(self, code, medoStockNumber)
                    self.tradingStatus.modifyMedoData(code, medo=False)
                    self.tradingStatus.modifyMesuData(code, mesu=True)


    def medoAllStock(self):
        mystock = self.myStock.returnData()
        for i in range(len(mystock)):
            code = mystock['종목코드'].iloc[i]
            code = self.standard.standardCode(code)
            quantity = mystock['보유수량'].iloc[i]
            Order.requestSijangMedoOrder(self, code, quantity)
