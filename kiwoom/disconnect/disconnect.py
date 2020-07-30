from PyQt5.QAxContainer import *
from abc import *


class DisconnectBase(QAxWidget):
    def __init__(self):
        super().__init__()

    def disconnect(self, sScrNo=None):
        pass

class Screen(DisconnectBase):
    def disconnect(self, sScrNo=None):
        self.dynamicCall("DisconnectRealData(QString)", sScrNo)

class RealData(DisconnectBase):
    def disconnect(self, sScrNo=None, code=None):
        self.dynamicCall("SetRealRemove(QString,QString)", sScrNo, code)


class Disconnect(Screen, RealData):
    def __init__(self):
        super().__init__()