from config.errorCode import *
from PyQt5.QAxContainer import *
from line.line import *
from abc import *
from kiwoom.tr.tr import *




# 무조건 상속
class OnEvent(Line):
    def connectOnEvent(self, receiveSlot):
        self.OnEventConnect.connect(receiveSlot)

    def receiveOnEvent(self, errCode):
        errCode = str(errors(errCode))
        self.logging.logger.debug("로그인 처리결과 %s" % (errCode))
        Line.sendMessage(self, "로그인 처리결과 %s" % (errCode))
        Login.exitEventLoop(self)

class OnReceiveTrBase():
    def connectOnReceiveTr(self, receiveSlot):
        self.OnReceiveTrData.connect(receiveSlot)

    def receiveOnReceiveTr(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext):
        if sRQName == "예수금상세현황요청":
            pass
        elif sRQName == "계좌평가잔고내역요청":
            pass
        elif sRQName == "실시간미체결요청":
            pass
        elif sRQName == "주식일봉차트조회":
            pass

class OnReceiveMsg():

    def connectOnReceiveMsg(self, receiveSlot):
        self.OnReceiveMsg.connect(receiveSlot)

    def receiveOnReceiveMsg(self, sScrNo, sRQName, sTrCode, msg):
        self.logging = Logging()
        self.logging.logger.debug( "스크린: %s, 요청이름: %s, tr코드: %s --- %s" % (sScrNo, sRQName, sTrCode, msg))


class OnReceiveRealBase():
    def connectOnReceiveReal(self, receiveSlot):
        self.OnReceiveRealData.connect(receiveSlot)

    def receiveOnReceiveReal(self, sCode, sRealType, sRealData):
        if sRealType == "장시작시간":
            pass
        elif sRealType == "주식체결":
            pass
        elif sRealType == '주식호가잔량':
            pass

class OnReceiveChejanBase():
    def connectOnReceiveChejan(self, receiveSlot):
        self.OnReceiveChejanData.connect(receiveSlot)

    def receiveOnReceiveChejan(self, sGubun, nItemCnt, sFidList):
        if int(sGubun) == 0:  # 주문체결
            pass
        elif int(sGubun) == 1:  # 잔고
            pass

class OnReceiveConditionVerBase():
    def connectOnReceiveConditionVer(self, receiveSlot):
        self.OnReceiveConditionVer.connect(receiveSlot)

    def receiveOnReceiveConditionVer(self, lRet, sMsg):
        pass

class OnReceiveTrConditionBase():
    def connectOnReceiveTrCondition(self, receiveSlot):
        self.OnReceiveTrCondition.connect(receiveSlot)

    def receiveOnReceiveTrCondition(self, sScrNo, strCodeList, strConditionName, index, nNext):
        pass

class OnReceiveRealConditionBase():
    def connectOnReceiveRealCondition(self, receiveSlot):
        self.OnReceiveRealCondition.connect(receiveSlot)

    def receiveOnReceiveRealCondition(self, strCode, strType, strConditionName, strConditionIndex):
        pass

