from kiwoom.tr.tr import *
from kiwoom.real.real import *
from kiwoom.order.order import *
from kiwoom.slot.slot import *
from kiwoom.other.standard import *
from PyQt5.QtTest import *
from kiwoom.data.mystockdata import *
from kiwoom.data.notconcludedstockdata import *
from PyQt5.QAxContainer import *
from kiwoom.disconnect.disconnect import *
from kiwoom.data.mystockdata import *



class DefaultTrading(Ocx, OnEvent, OnReceiveTrBase, OnReceiveRealBase, OnReceiveChejanBase, OnReceiveConditionVerBase,
                     OnReceiveRealConditionBase, OnReceiveTrConditionBase, OnReceiveMsg):
    def __init__(self):
        super().__init__()
        self.logging = Logging()
        self.myStockData = MyStockData()
        self.notConcludedStockData = NotConcludedStockData()


        Ocx.getInstance(self)
        #슬롯들 연결

        self.connectTrSlots()
        super().connectOnReceiveReal(self.receiveOnReceiveReal)
        super().connectOnReceiveConditionVer(self.receiveOnReceiveConditionVer)


        Login.request(self)
        AccountNum.receive(self)
        AccountInfo.request(self, accountNum=AccountNum.getAccountNum(self))
        MyStock.request(self, accountNum=AccountNum.getAccountNum(self))
        NotConcludedAccount.request(self, accountNum=AccountNum.getAccountNum(self))

        Condition.request(self)

    def connectTrSlots(self):
        super().connectOnEvent(self.receiveOnEvent)
        super().connectOnReceiveTr(self.receiveOnReceiveTr)
        super().connectOnReceiveMsg(super().receiveOnReceiveMsg)



    def receiveOnEvent(self, errCode):
        errCode = str(errors(errCode))
        self.logging.logger.debug("로그인 처리결과 %s" % (errCode))
        Line.sendMessage(self, "로그인 처리결과 %s" % (errCode))
        Login.exitEventLoop(self)


    def receiveOnReceiveTr(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext):
        if sRQName == "예수금상세현황요청":
            Deposit.receive(self, sRQName, sTrCode)
            Screen.disconnect(self, sScrNo=sScrNo)
            AccountInfo.exitEventLoop(self)
        elif sRQName == "계좌평가잔고내역요청":
            TotalBuyMoney.receive(self, sRQName, sTrCode)
            TotalProfitLossMoney.receive(self, sRQName, sTrCode)
            TotalProfitLossRate.receive(self, sRQName, sTrCode)
            MyStockNumber.receive(self, sRQName, sTrCode)

            for i in range(MyStockNumber.getNumber(self)):
                self.myStockData.appendData(myStockInformationList=MyStock.receive(self, sRQName=sRQName, sTrCode=sTrCode, sPrevNext=sPrevNext, index=i))
            if sPrevNext == '2':
                MyStock.request(self, sPrevNext=sPrevNext, accountNum=AccountNum.getAccountNum(self))
            else:
                MyStock.exitEventLoop(self)



        elif sRQName == "실시간미체결요청":
            NumberOfNotConcludedStock.receive(self, sRQName=sRQName, sTrCode=sTrCode, sPrevNext=sPrevNext)
            for i in range(NumberOfNotConcludedStock.getNumber(self)):
                self.notConcludedStockData.appendData(NotConcludedStock.receive(self,sRQName=sRQName,sTrCode=sTrCode,sPrevNext=sPrevNext,index=i))

            NotConcludedAccount.exitEventLoop(self)



        elif sRQName == "주식일봉차트조회":
            pass


    def receiveOnReceiveReal(self, sCode, sRealType, sRealData):
        if sRealType == "장시작시간":
            pass
        elif sRealType == "주식체결":
            pass
        elif sRealType == '주식호가잔량':
            pass

    def receiveOnReceiveConditionVer(self, lRet, sMsg):
        ConditionName.receive(self, lRet=lRet, sMsg=sMsg)
