from kiwoom.tr.tr import *
from kiwoom.real.real import *
from kiwoom.order.order import *
from kiwoom.slot.slot import *
from kiwoom.other.standard import *
from PyQt5.QtTest import *
from kiwoom.data.mystock import *
from kiwoom.data.notconcludedstock import *
from PyQt5.QAxContainer import *
from kiwoom.disconnect.disconnect import *


class OnReceiveTr(OnReceiveTrBase, Deposit, Disconnect):
    def connect(self):
        self.OnReceiveTrData.connect(self.receive)

    def receive(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext):
        if sRQName == "예수금상세현황요청":
            Deposit.receive(self, sRecordName, sTrCode)
            AccountInfo.exitEventLoop(self)
        elif sRQName == "계좌평가잔고내역요청":
            pass
        elif sRQName == "실시간미체결요청":
            pass
        elif sRQName == "주식일봉차트조회":
            pass

class DefaultTrading(Ocx, QAxWidget, OnEvent, AccountInfo, OnReceiveTr):
    def __init__(self):
        super().__init__()

        self.logging = Logging()
        # Ocx.getInstance(self)
        # OnEvent.connect(self)
        # OnReceiveMsg.connect(self)
        # Login.request(self)
        # OnReceiveTr.connect(self)
        # AccountNum.receive(self)
        # AccountInfo.request(self, accountNum=AccountNum.getAccountNum(self))


