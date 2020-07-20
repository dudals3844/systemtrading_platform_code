from PyQt5.QAxContainer import *
from config.errorCode import *
from kiwoom.tr.tr import *
from line.line import *

class Slot(QAxWidget, Line):
    def __init__(self):
        super().__init__()



    def connectOnEventConnect(self, receive_slot):
        self.OnEventConnect.connect(receive_slot)

    def connectOnReceiveTrData(self, receive_slot):
        self.OnReceiveTrData.connect(receive_slot)

    def connectOnReceiveMsg(self, receive_slot):
        self.OnReceiveMsg.connect(receive_slot)

    def connectOnReceiveRealData(self, receive_slot):
        self.OnReceiveRealData.connect(receive_slot)

    def connectOnReceiveChejanData(self, receive_slot):
        self.OnReceiveChejanData.connect(receive_slot)

    def connectOnReceiveConditionVer(self, receive_slot):
        self.OnReceiveConditionVer.connect(receive_slot)

    def connectOnReceiveTrCondition(self, receive_slot):
        self.OnReceiveTrCondition.connect(receive_slot)

    def connectOnReceiveRealCondition(self, receive_slot):
        self.OnReceiveRealCondition.connect(receive_slot)


    ############ Receive #############

    # 로그인 슬롯
    def receiveLoginSlot(self, errCode):
        errCode = str(errors(errCode))
        self.logging.logger.debug("로그인 처리결과 %s" % (errCode))
        Line.sendMessage(self, "로그인 처리결과 %s" % (errCode))
        self.loginEventLoop.exit()

    # Must Override
    def receiveTrdataSlot(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext):
        if sRQName == "예수금상세현황요청":
            pass
        elif sRQName == "계좌평가잔고내역요청":
            pass
        elif sRQName == "실시간미체결요청":
            pass
        elif sRQName == "주식일봉차트조회":
            pass

    # Must Override
    def receiveRealdataSlot(self, sCode, sRealType, sRealData):
        if sRealType == "장시작시간":
            pass
        elif sRealType == "주식체결":
            pass

    def receiveMsgSlot(self, sScrNo, sRQName, sTrCode, msg):
        self.logging.logger.debug("스크린: %s, 요청이름: %s, tr코드: %s --- %s" % (sScrNo, sRQName, sTrCode, msg))

    # Must Override
    def receiveChejanSlot(self, sGubun, nItemCnt, sFidList):
        if int(sGubun) == 0:  # 주문체결
            pass
        elif int(sGubun) == 1:  # 잔고
            pass

    # Must Override
    def receiveConditionNameSlot(self, lRet, sMsg):
        pass

    # Must Override
    def receiveConditionTrSlot(self, sScrNo, strCodeList, strConditionName, index, nNext):
        pass

    # Must Override
    def receiveConditionRealSlot(self, strCode, strType, strConditionName, strConditionIndex):
        pass

