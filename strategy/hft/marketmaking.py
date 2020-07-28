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

        self.mesu2HogaIndex = 11
        self.medo2HogaIndex = 8
        self.maxMesuIndex = 13




        # self.stdDataFrame = pd.read_csv('C:/Users/PC/PycharmProjects/systemtrading_platform/db/전종목표준편차.csv')
        # code = self.stdDataFrame['종목코드'].iloc[0]
        # code = '061040'
        # self.code = self.standard.standardCode(code)
        # self.tradingStatus.appendData(code=code, mesu=True, medo=False)


        # self.requestShotUpStrategy()

        Real.requestRealJangCheck(self)



        # self.medoAllStock()

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
                self.cancleAllMesuOrder()
                self.cancleAllMedoOrder()
                self.medoAllStock()

            elif status == '4':
                self.logging.logger.debug('3시 30분 장 종료')

        elif sRealType == '주식호가잔량':
            sCode, hogaTime, mesu_1, medo_1, mesu_1_Quantity, medo_1_Quantity, mesu_2, medo_2, mesu_2_Quantity,medo_2_Quantity,mesu_3,medo_3,mesu_3_Quantity,medo_3_Quantity,mesu_4,medo_4,mesu_4_Quantity,medo_4_Quantity,mesu_5,medo_5,mesu_5_Quantity,medo_5_Quantity,mesu_6,medo_6,mesu_6_Quantity,medo_6_Quantity,mesu_7,medo_7,mesu_7_Quantity,medo_7_Quantity,mesu_8,medo_8,mesu_8_Quantity,medo_8_Quantity,mesu_9, medo_9,mesu_9_Quantity,medo_9_Quantity, mesu_10,medo_10,mesu_10_Quantity,medo_10_Quantity,totalMesuHoga,totalMedoHoga = Real.receiveHoga(self, sCode, sRealType)
            self.hogaPriceDF.appendColumnData(sCode, hogaTime, mesu_1, medo_1, mesu_1_Quantity, medo_1_Quantity, mesu_2, medo_2, mesu_2_Quantity,medo_2_Quantity,mesu_3,medo_3,mesu_3_Quantity,medo_3_Quantity,mesu_4,medo_4,mesu_4_Quantity,medo_4_Quantity,mesu_5,medo_5,mesu_5_Quantity,medo_5_Quantity,mesu_6,medo_6,mesu_6_Quantity,medo_6_Quantity,mesu_7,medo_7,mesu_7_Quantity,medo_7_Quantity,mesu_8,medo_8,mesu_8_Quantity,medo_8_Quantity,mesu_9, medo_9,mesu_9_Quantity,medo_9_Quantity, mesu_10,medo_10,mesu_10_Quantity,medo_10_Quantity,totalMesuHoga,totalMedoHoga)
            # 시작할때 매수 2호가에 주문

            sCode = self.standard.standardCode(sCode)
            if not self.ishogaReceiveDF.isReceive(code=sCode):
                self.jijungMesuHogaOrder(code=sCode, mesuIndex=self.mesu2HogaIndex, mesuStockNum=self.TradingStockNumber)
                self.ishogaReceiveDF.modifyIsHogaReceiveTrue(code=sCode)

            self.mesuReposition(code=sCode)




        elif sRealType == "주식체결":
            chegul_time, now_price, spread, spread_rate, medo_ho_ga, mesu_ho_ga, volume, volume_sum, high, start, low = Real.receiveChegulPrice(self, sCode, sRealType)



    # Override
    def receiveChejanSlot(self, sGubun, nItemCnt, sFidList):
        if int(sGubun) == 0:  # 주문체결
            code, codeName, orderNo, originOrderNumber, orderStatus, orderPrice, orderGubun, notQuantity, okQuantity = Real.receiveNotConcludedAccount(
                self)
            self.notConMesuDF.appnedData(code, codeName, orderNo, originOrderNumber, orderStatus, orderPrice, orderGubun, notQuantity, okQuantity)
            self.notConMedoDF.appnedData(code, codeName, orderNo, originOrderNumber, orderStatus, orderPrice, orderGubun, notQuantity, okQuantity)
            if self.ishogaReceiveDF.hasData(code=code):
                self.orderCheguel(code = code, orderStatus=orderStatus, orderGubun=orderGubun, notQuantity=notQuantity, okQuantity=okQuantity)

        elif int(sGubun) == 1:  # 잔고
            code, code_nm, stock_quantity, total_buy_price = Real.receiveMystock(self)
            print('잔고 도착: '+code)
            self.myStock.appendData(code, code_nm, stock_quantity, total_buy_price)


    def jijungMesuHogaOrder(self, code, mesuIndex, mesuStockNum):
        hogaDataFrame = self.hogaPriceDF.getDataFrame(code = code)
        mesu2Hoga = hogaDataFrame.iloc[mesuIndex]
        mesu2Hoga = int(mesu2Hoga)
        Order.requestJijungMesuOrder(self, sCode=code, mesuStockNum=mesuStockNum, mesuPrice=mesu2Hoga)


    def jijungMedoHogaOrder(self, code, medoIndex, medoStockNum):
        hogaDataFrame = self.hogaPriceDF.getDataFrame(code=code)
        medo2Hoga = hogaDataFrame.iloc[medoIndex]
        medo2Hoga = int(medo2Hoga)
        Order.requestJijunhMedoOrder(self, sCode=code, medoStockNum=medoStockNum, medoPrice=medo2Hoga)




    def orderCheguel(self, code, orderStatus, orderGubun, notQuantity, okQuantity):
        if orderGubun == '매수' and orderStatus == '체결' and notQuantity == 0:
            if self.myStock.findStockQuantitiyData(code) >= self.TradingStockNumber:
                self.cancleMesuOrder(code)
                self.cancleMedoOrder(code)
                medoSum = self.myStock.findStockQuantitiyData(code)
                self.logging.logger.debug('미체결 매도 수량: %s' % (medoSum))
                mesuIndex = self.changeMesuHogaIndex(totalNotConcludedMedo=medoSum)
                mesuIndex = int(mesuIndex)
                self.logging.logger.debug('매수 인덱스: %s'%(mesuIndex) )
                self.jijungMesuHogaOrder(code=code, mesuIndex=mesuIndex, mesuStockNum=self.TradingStockNumber)
                self.jijungMedoHogaOrder(code=code, medoIndex=self.medo2HogaIndex, medoStockNum=self.TradingStockNumber)
            else:
                self.jijungMesuHogaOrder(code=code, mesuIndex=self.mesu2HogaIndex, mesuStockNum=self.TradingStockNumber)

        elif orderGubun == '매도' and orderStatus == '체결' and notQuantity == 0:
            self.cancleMesuOrder(code)
            self.cancleMedoOrder(code)
            medoSum = self.myStock.findStockQuantitiyData(code)
            self.logging.logger.debug('미체결 매도 수량: %s' % (medoSum))
            mesuIndex = self.changeMesuHogaIndex(totalNotConcludedMedo=medoSum)
            mesuIndex = int(mesuIndex)

            self.logging.logger.debug('매수 인덱스: %s' % (mesuIndex))
            self.jijungMesuHogaOrder(code=code, mesuIndex=mesuIndex, mesuStockNum=self.TradingStockNumber)
            self.jijungMedoHogaOrder(code=code, medoIndex=self.medo2HogaIndex, medoStockNum=self.TradingStockNumber)

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
                self.logging.logger.debug('매수 인덱스: %s'%(str(self.mesu2HogaIndex+spread)))
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

    def cancleMesuOrder(self, code):
        notConcludedMesuList = self.notConMesuDF.findNotConcludedOrderNumberList(code=code)
        for orderNumber in notConcludedMesuList:
            Order.requestMesuCancelOrder(self, sCode=code, orderNum=orderNumber)
            self.notConMesuDF.deleteRow(orderNumber)


    def cancleMedoOrder(self, code):
        notConcludedMedoList = self.notConMedoDF.findNotConcludedOrderNumberList(code=code)
        for orderNumber in notConcludedMedoList:
            Order.requestMedoCancelOrder(self, sCode=code, orderNum=orderNumber)
            self.notConMedoDF.deleteRow(orderNumber)

    def cancleAllMesuOrder(self):
        tmpdf = self.ishogaReceiveDF.getDataFrame()
        for i in range(len(tmpdf)):
            code = tmpdf['종목코드'].iloc[i]
            code = self.standard.standardCode(code)
            try:
                notConcludedMesuList = self.notConMesuDF.findNotConcludedOrderNumberList(code=code)
                for orderNumber in notConcludedMesuList:
                    Order.requestMesuCancelOrder(self, sCode=code, orderNum=orderNumber)
                    self.notConMesuDF.deleteRow(orderNumber)
            except:
                self.logging.logger.debug("매수 취소 오류")

    def cancleAllMedoOrder(self):
        tmpdf = self.ishogaReceiveDF.getDataFrame()
        for i in range(len(tmpdf)):
            code = tmpdf['종목코드'].iloc[i]
            code = self.standard.standardCode(code)
            try:
                notConcludedMedoList = self.notConMedoDF.findNotConcludedOrderNumberList(code=code)
                for orderNumber in notConcludedMedoList:
                    Order.requestMedoCancelOrder(self, sCode=code, orderNum=orderNumber)
                    self.notConMedoDF.deleteRow(orderNumber)
            except:
                self.logging.logger.debug("매도 취소 오류")




    def medoAllStock(self):
        mystock = self.myStock.returnData()
        for i in range(len(mystock)):
            code = mystock['종목코드'].iloc[i]
            code = self.standard.standardCode(code)
            quantity = mystock['보유수량'].iloc[i]
            Order.requestSijangMedoOrder(self, code, quantity)



    def requestShotUpStrategy(self):
        index, condition_nm = self.condition.findData(0)
        self.requestRealCondition(index, condition_nm)



    def receiveConditionRealSlot(self, strCode, strType, strConditionName, strConditionIndex):
        code, type = self.receiveConditionRealStock(strCode, strType, strConditionName, strConditionIndex)
        if type == 'I':
            print('조건 편입: '+code)
            if self.nowCompanyNumber <= self.maxCompanyNumber:
                if not self.ishogaReceiveDF.hasData(code):
                    self.ishogaReceiveDF.inputDefaultData(code)
                    Real.requestHoga(self, code)
                    self.nowCompanyNumber += 1

        elif type == 'D':
            pass


    def mesuReposition(self, code):
        if not self.myStock.hasData(code):
            tmpDF = self.notConMesuDF.getDataFrame()
            for i in range(len(tmpDF)):
                tmpcode = tmpDF['종목코드'].iloc[i]
                tmpcode = self.standard.standardCode(tmpcode)
                price = tmpDF['주문가격'].iloc[i]
                orderNumber = tmpDF['주문번호'].iloc[i]
                if tmpcode == code and self.hogaPriceDF.findIndex(code=code, price= price) > self.maxMesuIndex:
                    self.notConMesuDF.deleteRow(orderNum=orderNumber)
                    Order.requestMesuCancelOrder(self, code, orderNumber)
                    self.jijungMesuHogaOrder(code = code, mesuIndex= self.mesu2HogaIndex, mesuStockNum=self.TradingStockNumber)




    def standardOrderNumber(self, code):
        orderNumber = "{0:0>7}".format(code)  # 오류안나게 종목코드 6자리 맞춰줌
        return orderNumber


