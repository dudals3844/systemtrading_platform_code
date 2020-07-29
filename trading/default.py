from kiwoom.tr.tr import *
from kiwoom.real.real import *
from kiwoom.order.order import *
from kiwoom.slot.slot import *
from kiwoom.other.standard import *
from PyQt5.QtTest import *
from kiwoom.data.mystock import *
from kiwoom.data.notconcludedstock import *
from kiwoom.disconnect.disconnect import Disconnect


class DefaultTrading(Tr, Real, Order,Slot, Disconnect, Line):
    def __init__(self):
        super().__init__()
        self.logging = Logging()

        Login.request(self)
        AccountNum.receive(self)
        AccountInfo.request(self, accountNum=AccountNum.getAccountNum(self))
