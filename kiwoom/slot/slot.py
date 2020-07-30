from config.errorCode import *
from PyQt5.QAxContainer import *
from line.line import *
from abc import *
from kiwoom.tr.tr import *

class ConnectSlotBase(QAxWidget):


    def connect(self, receiveSlot):
        pass

class OnEvent(ConnectSlotBase):
    def connect(self, receiveSlot):
        self.OnEventConnect.connect(receiveSlot)

class OnReceiveTr(ConnectSlotBase):
    def connect(self, receiveSlot):
        self.OnReceiveTrData.connect(receiveSlot)

class OnReceiveMsg(ConnectSlotBase):
    def connect(self, receiveSlot):
        self.OnReceiveMsg.connect(receiveSlot)

class OnReceiveRealData(ConnectSlotBase):
    def connect(self, receiveSlot):
        self.OnReceiveRealData.connect(receiveSlot)

class OnReceiveChejanData(ConnectSlotBase):
    def connect(self, receiveSlot):
        self.OnReceiveChejanData.connect(receiveSlot)

class OnReceiveConditionVer(ConnectSlotBase):
    def connect(self, receiveSlot):
        self.OnReceiveConditionVer.connect(receiveSlot)

class OnReceiveTrCondition(ConnectSlotBase):
    def connect(self, receiveSlot):
        self.OnReceiveTrCondition.connect(receiveSlot)

class OnReceiveRealCondition(ConnectSlotBase):
    def connect(self, receiveSlot):
        self.OnReceiveRealCondition.connect(receiveSlot)

class LoginSlot(Line, Login):
    def receive(self, errCode):
        errCode = str(errors(errCode))
        self.logging.logger.debug("로그인 처리결과 %s" % (errCode))
        Line.sendMessage(self, "로그인 처리결과 %s" % (errCode))
        Login.exitEventLoop(self)

class MsgSlot():
    def __init__(self):
        self.logging = Logging()
    def receive(self, sScrNo, sRQName, sTrCode, msg):
        self.logging.logger.debug("스크린: %s, 요청이름: %s, tr코드: %s --- %s" % (sScrNo, sRQName, sTrCode, msg))


class TrDataSlotBase(metaclass=ABCMeta):
    @abstractmethod
    def receive(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext):
        if sRQName == "예수금상세현황요청":
            pass
        elif sRQName == "계좌평가잔고내역요청":
            pass
        elif sRQName == "실시간미체결요청":
            pass
        elif sRQName == "주식일봉차트조회":
            pass

class RealDataSlotBase(metaclass=ABCMeta):
    @abstractmethod
    def receive(self, sCode, sRealType, sRealData):
        if sRealType == "장시작시간":
            pass
        elif sRealType == "주식체결":
            pass
        elif sRealType == '주식호가잔량':
            pass


class ChejanSlotBase(metaclass=ABCMeta):
    @abstractmethod
    def receive(self, sGubun, nItemCnt, sFidList):
        if int(sGubun) == 0:  # 주문체결
            pass
        elif int(sGubun) == 1:  # 잔고
            pass

class ConditionNameSlot(metaclass=ABCMeta):
    @abstractmethod
    def receive(self, lRet, sMsg):
        pass

class ConditionTrSlot(metaclass=ABCMeta):
    @abstractmethod
    def receive(self, sScrNo, strCodeList, strConditionName, index, nNext):
        pass

class ConditionRealSlot(metaclass=ABCMeta):
    @abstractmethod
    def receive(self, strCode, strType, strConditionName, strConditionIndex):
        pass

class Slot(OnEvent, OnReceiveTr, OnReceiveMsg, OnReceiveRealData,
           OnReceiveChejanData, OnReceiveConditionVer, OnReceiveTrCondition,
           OnReceiveRealCondition, LoginSlot, MsgSlot):
    pass