from PyQt5.QAxContainer import *
from config.log_class import *
from kiwoom.tr.tr import *
from kiwoom.order.order import *
from kiwoom.real.real import *
from kiwoom.other.standard import *
from kiwoom.slot.slot import *
from kiwoom.disconnect.disconnect import *
from kiwoom.handledata.mystock import *
from kiwoom.handledata.notconcludedstock import *
from kiwoom.handledata.condition import *
from kiwoom.handledata.tradingstatus import *
from kiwoom.handledata.minuteprice import *
from kiwoom.handledata.tickprice import *
from config.errorCode import *
from PyQt5.QtTest import *
import threading

class Trading(Tr, Real, Order ,Slot, Disconnect, Line):
    def __init__(self):
        super().__init__()
        self.standard = Standard()
        self.logging = Logging()
        self.myStock = MyStock()
        self.notConcludedStock = NotConcludedStock()
        self.condition = Condition()
        self.minutePrice = MinutePrice()
        self.tickprice = TickPrice()
        self.tradingStatus = TradingStatus()

        self.connectTrSlots()
        self.connectRealSlots()
        self.connectConditionSlots()
        Tr.requestLoginCommConnect(self)
        Tr.receiveAccountNum(self)
        Tr.requestAccountInfo(self, account_num=Tr.getAccountNum(self))
        Tr.requestAccountInfo(self, account_num=Tr.getAccountNum(self))
        Tr.requestAccountMystock(self, accountNum=Tr.getAccountNum(self))
        QTest.qWait(1000)
        Tr.requestNotConcludedAccount(self, account_num=Tr.getAccountNum(self))
        Tr.requestCondition(self)
        self.accountNum = Tr.getAccountNum(self)


    def connectTrSlots(self):
        Slot.connectOnEventConnect(self, receive_slot=self.receiveLoginSlot)
        Slot.connectOnReceiveTrData(self, receive_slot=self.receiveTrdataSlot)
        Slot.connectOnReceiveMsg(self, receive_slot= self.receiveMsgSlot)

    def connectRealSlots(self):
        Slot.connectOnReceiveRealData(self, receive_slot=self.receiveRealdataSlot)
        Slot.connectOnReceiveChejanData(self, receive_slot=self.receiveChejanSlot)

    def connectConditionSlots(self):
        Slot.connectOnReceiveConditionVer(self, receive_slot=self.receiveConditionNameSlot)
        Slot.connectOnReceiveTrCondition(self, receive_slot=self.receiveConditionTrSlot)
        Slot.connectOnReceiveRealCondition(self, receive_slot=self.receiveConditionRealSlot)

    def receiveTrdataSlot(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext):
        if sRQName == "예수금상세현황요청":
            # pass
            Tr.receiveDeposit(self, sRQName, sTrCode)
            Disconnect.disconnectScreen(self, sScrNo)
            Tr.exitAccountInfo(self)
        elif sRQName == "계좌평가잔고내역요청":
            # pass
            Tr.receiveTotalBuyMoney(self, sRQName, sTrCode)
            Tr.receiveTotalProfitLossMoney(self, sRQName, sTrCode)
            Tr.receiveTotalProfitLossRate(self, sRQName, sTrCode)
            Tr.receiveNumberOfMystock(self, sRQName, sTrCode)
            index = Tr.getNumberOfMystock(self)
            for i in range(index):
                code, code_nm, stock_quantity, total_chegual_price = Tr.receiveMystock(self, sRQName, sTrCode, sPrevNext, i)
                self.myStock.appendData(code, code_nm, stock_quantity, total_chegual_price)
            if sPrevNext == '2':
                Tr.requestAccountMystock(self, sPrevNext, Tr.getAccountNum(self))
            else:
                Tr.exitAccountMystock(self)
        elif sRQName == "실시간미체결요청":
            # pass
            Tr.receiveNumberOfNotConcludedStock(self, sRQName, sTrCode)
            index = Tr.getNumberOfNotConcludedStock(self)
            for i in range(index):
                code, code_nm, origin_order_number, order_no, order_status, order_price, order_gubun, not_quantity, ok_quantity = Tr.receiveNotConcludedAccount(self, sRQName, sTrCode, i)
                self.notConcludedStock.appendData(code, code_nm, origin_order_number, order_no,order_status, order_price, order_gubun, not_quantity, ok_quantity)

            Tr.exitRequestNotConcludedAccount(self)


        elif sRQName == "주식분봉차트조회":
            sPrevNext, code, data = Tr.receiveMinutePriceData(self, sRQName, sTrCode, sPrevNext)
            code = self.standard.standardCode(code)
            self.minutePrice.setPriceArray(priceArray=data, code=code)
            Tr.exitMinutePriceData(self)


        elif sRQName == "주식틱차트조회":
            sPrevNext, code, data = Tr.receiveTickPriceData(self, sRQName, sTrCode, sPrevNext)
            code = self.standard.standardCode(code)
            self.tickprice.setPriceArray(priceArray=data, code=code)
            Tr.exitTickPriceData(self)


    def receiveConditionNameSlot(self, lRet, sMsg):

        nameList = Tr.receiveConditionNameList(self, lRet, sMsg)
        self.condition.conditionNameListToConditionDataFrame(nameList)
        Tr.exitCondition(self)

    def receiveConditionTrSlot(self, sScrNo, strCodeList, strConditionName, index, nNext):
        stockList = Tr.receiveConditionStockTr(self, sScrNo, strCodeList, strConditionName, index, nNext)
