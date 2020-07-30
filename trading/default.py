from kiwoom.tr.tr import *
from kiwoom.real.real import *
from kiwoom.order.order import *
from kiwoom.slot.slot import *
from kiwoom.other.standard import *
from PyQt5.QtTest import *
from kiwoom.data.mystock import *
from kiwoom.data.notconcludedstock import *
from kiwoom.disconnect.disconnect import Disconnect
from PyQt5.QAxContainer import *


class DefaultTrading(Ocx, OnEvent):
    def __init__(self):
        super().__init__()
        self.logging = Logging()
        Ocx.getInstance(self)
        OnReceiveMsg.connect(self)
        OnEvent.connect(self)
        Login.request(self)

        AccountNum.receive(self)
        AccountInfo.request(self, accountNum=AccountNum.getAccountNum(self))



