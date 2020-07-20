from trading.trading import *
from kiwoom.other.basictradinginformation import *
from kiwoom.handledata.instanceout import *
import threading
import time

class MovingAverageBreakThroughStrategy(Trading):
    def __init__(self):
        super().__init__()

        self.numofTrading = BasicTradingInformation()
        self.numofTrading.setDeposit(self.getDeposit())
        self.numofTrading.setTradingNumber(10)
        self.numofTrading.setMarginRate(40)
        self.instanceOut = InstanceOut()
        self.numofTrading.calculateOneTradingDeposit()
        self.numofTrading.calculateTradingNumberUsingMargin()

        self.requestMovingAverageBreakthroughStrategy()
        self.requestRealJangCheck()

        self.tmp_code = None

    def requestMovingAverageBreakthroughStrategy(self):
        index, condition_nm = self.condition.isReceive(1)
        self.requestRealCondition(index, condition_nm)




    def receiveRealdataSlot(self, sCode, sRealType, sRealData):
        if sRealType == "장시작시간":
            status = self.receiveJangStatus(sCode, sRealType)
            if status == '0':
                self.logging.logger.debug('장 시작 전')

            elif status == '3':
                self.logging.logger.debug('장 시작')
                self.medo_all_stock()



            elif status == '2':
                self.logging.logger.debug('장 종료후 동시호가')
                self.medo_all_stock()


            elif status == '4':
                self.logging.logger.debug('3시 30분 장 종료')

        elif sRealType == "주식체결":
            chegul_time, now_price, spread, spread_rate, medo_ho_ga, mesu_ho_ga, volume, volume_sum, high, start, low = self.receiveChegulPrice(sCode, sRealType)
            if self.tradingStatus.isMesuData(sCode) == True:
                self.requestSijangMesuOrder(sCode, self.numofTrading.getHowManyStockMesu(now_price))
                self.tradingStatus.modifyMesuData(sCode, mesu=False)
                self.tradingStatus.modifyMedoData(sCode, medo=True)

    def medo_all_stock(self):
        mystock = self.myStock.returnData()
        for i in range(len(mystock)):
            code = mystock['종목코드'].iloc[i]
            code = self.standard.standardCode(code)
            quantity = mystock['보유수량'].iloc[i]
            self.requestSijangMedoOrder(code, quantity)


    def receiveChejanSlot(self, sGubun, nItemCnt, sFidList):
        if int(sGubun) == 0: #주문체결
            code, code_nm, order_no, origin_order_number, order_status, order_price, order_gubun, not_quantity, ok_quantity = Real.receiveNotConcludedAccount(self)
            self.notConcludedStock.appendData(code, code_nm, order_no, origin_order_number, order_status, order_price, order_gubun, not_quantity, ok_quantity)
        elif int(sGubun) == 1: #잔고
            code, code_nm, stock_quantity, total_buy_price = Real.receiveMystock(self)
            self.myStock.appendData(code, code_nm, stock_quantity, total_buy_price)

    def receiveConditionTrSlot(self, sScrNo, strCodeList, strConditionName, index, nNext):
        self.receiveConditionStockTr(sScrNo, strCodeList, strConditionName, index, nNext)

    def inCondition(self,code):
        time.sleep(10)
        if not self.instanceOut.isInstanceOut(code):
            if self.tradingStatus.hasData(code) == False:
                self.tradingStatus.appendData(code)
                self.tradingStatus.modifyMesuData(code, mesu=True)
                self.requestRealChegulPrice(code)


        elif self.instanceOut.isInstanceOut(code):
            self.logging.logger.debug("종목코드: %s 즉시 이탈입니다" %(code))
            self.instanceOut.deleteData(code)

    def receiveConditionRealSlot(self, strCode, strType, strConditionName, strConditionIndex):
        code, type = self.receiveConditionRealStock(strCode, strType, strConditionName, strConditionIndex)
        if type == 'I':
            status = self.instanceOut.appendData(code)
            if status == True:
                th = threading.Thread(target=self.inCondition, args=(code, ))
                th.start()
        elif type == 'D':
            if self.instanceOut.hasData(code):
                self.instanceOut.modifyInstanceOutTrue(code)
                if self.myStock.hasData(code) == True:
                    if self.tradingStatus.isMedoData(code) == True:
                        medo_num = self.myStock.findStockQuantitiyData(code)
                        self.requestSijangMedoOrder(code, medo_num)
                        self.tradingStatus.modifyMedoData(code, medo= False)
                        self.instanceOut.deleteData(code)


