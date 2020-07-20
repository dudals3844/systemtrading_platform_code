from trading.trading import *
from kiwoom.other.basictradinginformation import *
import pandas
from strategy.hft.dataframe.notconcludedmedostock import *
from strategy.hft.dataframe.notconcludedmesustock import *
from strategy.hft.dataframe.hogaprice import *
from strategy.hft.dataframe.ishogareceive import *
import threading

class MarketMaking(Trading):
    def __init__(self):
        super().__init__()
        BasicTradingInformation.setDeposit(self, Tr.getDeposit(self))
        BasicTradingInformation.setMarginRate(self, 100)
        BasicTradingInformation.setTradingNumber(self, 100)
        BasicTradingInformation.calculateTradingNumberUsingMargin(self)
        BasicTradingInformation.calculateOneTradingDeposit(self)

        #고정
        self.nowCompanyNumber = 0
        #예산에 따라 조절
        self.maxCompanyNumber = 3

        #한번 거래할때 몇주 살건지
        self.TradingStockNumber = 2


        self.notConcludedMesuNum = None
        self.notConcludedMedoNum = None

        self.notConMesuDF = NotConcludedMesuStock()
        self.notConMedoDF = NotConcludedMedoStock()
        self.hogaPriceDF = HogaPrice()
        self.ishogaReceiveDF = IsHogaReceive()


        # self.stdDataFrame = pd.read_csv('C:/Users/PC/PycharmProjects/systemtrading_platform/db/전종목표준편차.csv')
        # code = self.stdDataFrame['종목코드'].iloc[0]
        # code = '061040'
        # self.code = self.standard.standardCode(code)
        # self.tradingStatus.appendData(code=code, mesu=True, medo=False)



        Real.requestRealJangCheck(self)



        # self.medoAllStock()
        # Real.requestHoga(self, self.code)
        # self.requestShotUpStrategy()

    def receiveRealdataSlot(self, sCode, sRealType, sRealData):
        if sRealType == "장시작시간":
            status = Real.receiveJangStatus(self, sCode, sRealType)
            if status == '0':
                self.logging.logger.debug('장 시작 전')

            elif status == '3':
                self.logging.logger.debug('장 시작')
                Line.sendMessage(self, '장 시작')
                self.medoAllStock()
                self.requestShotUpStrategy()

            elif status == '2':
                self.logging.logger.debug('장 종료후 동시호가')
                self.cancleAllMedoOrder()
                self.cancleAllMesuOrder()
                self.medoAllStock()

            elif status == '4':
                self.logging.logger.debug('3시 30분 장 종료')

        elif sRealType == '주식호가잔량':
            self.hogaPriceDF.appendColumnData(Real.receiveHoga(self, sCode, sRealType))
            # 시작할때 매수 2호가에 주문
            if not self.ishogaReceiveDF.isReceive(code=sCode):
                self.jijungMesuHogaOrder(mesuIndex=self.mesu2HogaIndex, mesuStockNum=self.TradingStockNumber)


            self.ishogaReceive = True


        elif sRealType == "주식체결":
            chegul_time, now_price, spread, spread_rate, medo_ho_ga, mesu_ho_ga, volume, volume_sum, high, start, low = Real.receiveChegulPrice(self, sCode, sRealType)



    # Override
    def receiveChejanSlot(self, sGubun, nItemCnt, sFidList):
        if int(sGubun) == 0:  # 주문체결
            code, codeName, orderNo, originOrderNumber, orderStatus, orderPrice, orderGubun, notQuantity, okQuantity = Real.receiveNotConcludedAccount(
                self)
            self.notConMesuDF.appnedData(code, codeName, orderNo, originOrderNumber, orderStatus, orderPrice, orderGubun, notQuantity, okQuantity)
            self.notConMedoDF.appnedData(code, codeName, orderNo, originOrderNumber, orderStatus, orderPrice, orderGubun, notQuantity, okQuantity)
            if self.ishogaReceive:
                self.orderCheguel(orderStatus=orderStatus, orderGubun=orderGubun, notQuantity=notQuantity, okQuantity=okQuantity)

        elif int(sGubun) == 1:  # 잔고
            code, code_nm, stock_quantity, total_buy_price = Real.receiveMystock(self)
            print('잔고 도착: '+code)
            self.myStock.appendData(code, code_nm, stock_quantity, total_buy_price)


    def jijungMesuHogaOrder(self, code, mesuIndex, mesuStockNum):
        hogaDataFrame = self.hogaDataFrame
        mesu2Hoga = hogaDataFrame['호가'].iloc[mesuIndex]
        Order.requestJijungMesuOrder(self, sCode=code, mesuStockNum=mesuStockNum, mesuPrice=mesu2Hoga)


    def jijungMedoHogaOrder(self, code, medoIndex, medoStockNum):
        hogaDataFrame = self.hogaDataFrame
        medo2Hoga = hogaDataFrame['호가'].iloc[medoIndex]
        Order.requestJijunhMedoOrder(self, sCode=code, medoStockNum=medoStockNum, medoPrice=medo2Hoga)




    def orderCheguel(self, orderStatus, orderGubun, notQuantity, okQuantity):
        if orderGubun == '매수' and orderStatus == '체결' and notQuantity == 0:
            if self.myStock.findStockQuantitiyData(self.code) >= self.TradingStockNumber:
                # self.threadCancleAllMesuOrder()
                # self.threadCancleAllMedoOrder()
                self.cancleAllMesuOrder()
                self.cancleAllMedoOrder()
                medoSum = self.myStock.findStockQuantitiyData(self.code)
                self.logging.logger.debug('미체결 매도 수량: %s' % (medoSum))
                mesuIndex = self.changeMesuHogaIndex(totalNotConcludedMedo=medoSum)
                mesuIndex = int(mesuIndex)

                self.logging.logger.debug('매수 인덱스: %s'%(mesuIndex) )
                # self.threadJijungMedoHogaOrder(medoIndex=self.medo2HogaIndex, medoStockNum=self.oneTradingStock)
                # self.threadJijungMesuHogaOrder(mesuIndex=mesuIndex, mesuStockNum=self.oneTradingStock)
                self.jijungMesuHogaOrder(mesuIndex=mesuIndex, mesuStockNum=self.TradingStockNumber)
                self.jijungMedoHogaOrder(medoIndex=self.medo2HogaIndex, medoStockNum=self.TradingStockNumber)
            else:
                self.jijungMesuHogaOrder(mesuIndex=self.mesu2HogaIndex, mesuStockNum=self.TradingStockNumber)
                # self.threadJijungMesuHogaOrder(mesuIndex=self.mesu2HogaIndex, mesuStockNum=self.oneTradingStock)
        elif orderGubun == '매도' and orderStatus == '체결' and notQuantity == 0:
            #
            # self.threadCancleAllMesuOrder()
            # self.threadCancleAllMedoOrder()
            self.cancleAllMesuOrder()
            self.cancleAllMedoOrder()
            medoSum = self.myStock.findStockQuantitiyData(self.code)
            self.logging.logger.debug('미체결 매도 수량: %s' % (medoSum))
            mesuIndex = self.changeMesuHogaIndex(totalNotConcludedMedo=medoSum)
            mesuIndex = int(mesuIndex)

            self.logging.logger.debug('매수 인덱스: %s' % (mesuIndex))
            # self.threadJijungMedoHogaOrder(medoIndex=self.medo2HogaIndex, medoStockNum=self.oneTradingStock)
            # self.threadJijungMesuHogaOrder(mesuIndex=mesuIndex, mesuStockNum=self.oneTradingStock)
            self.jijungMesuHogaOrder(mesuIndex=mesuIndex, mesuStockNum=self.TradingStockNumber)
            self.jijungMedoHogaOrder(medoIndex=self.medo2HogaIndex, medoStockNum=self.TradingStockNumber)

    def changeMedoHogaIndex(self, totalNotConcludedMesu):
        if totalNotConcludedMesu/self.TradingStockNumber >= 3:
            spread = totalNotConcludedMesu / self.TradingStockNumber - 2
            if int(self.medo2HogaIndex - spread) >= 6:
                return int(self.medo2HogaIndex - spread)
            else:
                return 6
        else:
            return int(self.medo2HogaIndex)

    def changeMesuHogaIndex(self, totalNotConcludedMedo):
        if totalNotConcludedMedo/self.TradingStockNumber >= 3:
            spread = totalNotConcludedMedo / self.TradingStockNumber - 2
            if int(self.mesu2HogaIndex + spread) <= self.maxMesuIndex:
                self.logging.logger("매수 인덱스: %s" %(str(self.mesu2HogaIndex+spread)))
                return int(self.mesu2HogaIndex + spread)
            else:
                return self.maxMesuIndex
        else:
            return int(self.mesu2HogaIndex)


    def hogaRange(self, price):
        if price < 1000:
            return 1
        elif 1000 <= price and price < 5000:
            return 5
        elif 5000 <= price and price < 10000:
            return 10
        elif 10000 <= price and price < 500000:
            return 50
        elif 50000 <= price and price < 100000:
            return 100
        elif 100000 <= price and price < 500000:
            return 500
        else:
            return 1000

    def cancleAllMesuOrder(self):
        notConcludedMesuList = self.notConMesuDF.findNotConcludedOrderNumberList()
        for orderNumber in notConcludedMesuList:
            Order.requestMesuCancelOrder(self, sCode=self.code, orderNum=orderNumber)
            self.notConMesuDF.deleteRow(orderNumber)


    def cancleAllMedoOrder(self):
        notConcludedMedoList = self.notConMedoDF.findNotConcludedOrderNumberList()
        for orderNumber in notConcludedMedoList:
            Order.requestMedoCancelOrder(self, sCode=self.code, orderNum=orderNumber)
            self.notConMedoDF.deleteRow(orderNumber)


    def medoAllStock(self):
        mystock = self.myStock.returnData()
        for i in range(len(mystock)):
            code = mystock['종목코드'].iloc[i]
            code = self.standard.standardCode(code)
            quantity = mystock['보유수량'].iloc[i]
            Order.requestSijangMedoOrder(self, code, quantity)

    # def threadMesuMedoReposition(self):
    #     print("10초마다 실행되고있당")
    #     tmpMesuDataFrame = self.notConMesuDF.getDataFrame()
    #     for i in range(len(tmpMesuDataFrame)):
    #         price = tmpMesuDataFrame['주문가격'].iloc[i]
    #         if self.findHogaIndex(price) > self.maxMesuIndex:
    #             self.logging.logger.debug('매수호가에서 너무 멀어져서 다시 매수 2호가로 재주문')
    #             self.cancleAllMesuOrder()
    #             medoSum = self.myStock.findStockQuantitiyData(self.code)
    #             self.logging.logger.debug('미체결 매도 수량: %s' % (medoSum))
    #             mesuIndex = self.changeMesuHogaIndex(totalNotConcludedMedo=medoSum)
    #             mesuIndex = int(mesuIndex)
    #             self.jijungMesuHogaOrder(mesuIndex=mesuIndex, mesuStockNum=self.TradingStockNumber)
    #             break
    #
    #     tmpMedoDataFrame = self.notConMedoDF.getDataFrame()
    #
    #     for i in range(len(tmpMedoDataFrame)):
    #         price = tmpMedoDataFrame['주문가격'].iloc[i]
    #         if self.findHogaIndex(price) < 6:
    #             self.logging.logger.debug('매도호가에서 너무 멀어져서 다시 매수 2호가로 재주문')
    #             self.cancleAllMedoOrder()
    #             self.jijungMedoHogaOrder(medoIndex=self.medo2HogaIndex, medoStockNum=self.TradingStockNumber)
    #             break


        # if not self.myStock.hasData(self.code):
        #
        #     self.cancleAllMesuOrder()
        #     self.jijungMesuHogaOrder(mesuIndex=self.mesu2HogaIndex, mesuStockNum=self.oneTradingStock)
        # elif self.myStock.hasData(self.code):
        #     if self.myStock.findStockQuantitiyData(self.code) <= 4:
        #         self.cancleAllMesuOrder()
        #         self.jijungMesuHogaOrder(mesuIndex=self.mesu2HogaIndex, mesuStockNum=self.oneTradingStock)

        # else:
        #     tmpMesuDataFrame = self.notConMesuDF.getDataFrame()
        #     for i in range(len(tmpMesuDataFrame)):
        #         price = tmpMesuDataFrame['주문가격'].iloc[i]
        #         if self.findHogaIndex(price) > 13:
        #             self.logging.logger.debug('매수호가에서 너무 멀어져서 다시 매수 2호가로 재주문')
        #             self.cancleAllMesuOrder()
        #             self.jijungMesuHogaOrder(mesuIndex=self.mesu2HogaIndex, mesuStockNum=self.oneTradingStock)
        #             break
        #
        #     tmpMedoDataFrame = self.notConMedoDF.getDataFrame()
        #
        #     for i in range(len(tmpMedoDataFrame)):
        #         price = tmpMedoDataFrame['주문가격'].iloc[i]
        #         if self.findHogaIndex(price) < 6:
        #             self.logging.logger.debug('매도호가에서 너무 멀어져서 다시 매수 2호가로 재주문')
        #             self.cancleAllMedoOrder()
        #             self.jijungMedoHogaOrder(medoIndex=self.medo2HogaIndex, medoStockNum=self.oneTradingStock)
        #             break

        threading.Timer(10, self.threadMesuMedoReposition).start()


    def requestShotUpStrategy(self):
        index, condition_nm = self.condition.isReceive(0)
        self.requestRealCondition(index, condition_nm)



    def receiveConditionRealSlot(self, strCode, strType, strConditionName, strConditionIndex):
        code, type = self.receiveConditionRealStock(strCode, strType, strConditionName, strConditionIndex)
        if type == 'I':
            if self.nowCompanyNumber <= self.maxCompanyNumber:
                if not self.ishogaReceiveDF.hasData(code):
                    self.ishogaReceiveDF.inputDefaultData(code)
                    Real.requestHoga(self, code)
                    self.nowCompanyNumber += 1

        elif type == 'D':
            pass



    # def mesuReposition(self):
    #
    #
    #     tmpMesuDataFrame = self.notConMesuDF.getDataFrame()
    #     for i in range(len(tmpMesuDataFrame)):
    #         price = tmpMesuDataFrame['주문가격'].iloc[i]
    #         if self.findHogaIndex(price) > 13:
    #             self.logging.logger.debug('매수호가에서 너무 멀어져서 다시 매수 2호가로 재주문')
    #             self.cancleAllMesuOrder()
    #             QTest.qWait(1000)
    #             break
    #     if len(tmpMesuDataFrame) == 0:
    #         # self.jijungMesuHogaOrder(mesuIndex=self.mesu2HogaIndex, mesuStockNum=self.oneTradingStock)
    #         self.threadJijungMesuHogaOrder(mesuIndex=self.mesu2HogaIndex, mesuStockNum=self.oneTradingStock)
    #         QTest.qWait(1000)
    # def medoReposition(self):
    #     try:
    #         tmpMedoDataFrame = self.notConMedoDF.getDataFrame()
    #
    #         for i in range(len(tmpMedoDataFrame)):
    #             price = tmpMedoDataFrame['주문가격'].iloc[i]
    #             notQuantity = tmpMedoDataFrame['미체결수량'].iloc[i]
    #             orderNumber = tmpMedoDataFrame['주문번호'].iloc[i]
    #             if self.findHogaIndex(price) < 6:
    #                 self.logging.logger.debug('매도호가에서 너무 멀어져서 다시 매수 2호가로 재주문')
    #                 self.logging.logger.debug("미체결 매도 데이터\n"+tmpMedoDataFrame)
    #                 orderNumber = self.standardOrderNum(orderNumber)
    #                 Order.requestMedoCancelOrder(self, sCode=self.code, orderNum=orderNumber)
    #                 self.jijungMedoHogaOrder(medoIndex=self.medo2HogaIndex, medoStockNum=self.standardOrderNum)
    #
    #
    #     except:
    #         pass



    def standardOrderNumber(self, code):
        orderNumber = "{0:0>7}".format(code)  # 오류안나게 종목코드 6자리 맞춰줌
        return orderNumber


