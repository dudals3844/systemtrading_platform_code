from PyQt5.QAxContainer import *
from config.log_class import *
from PyQt5.QtCore import *
from line.line import *
from abc import *
from PyQt5.QtCore import *

class TrReceiveBase(Logging, Line):
    def __init__(self):
        super().__init__()
        self.logging = Logging()


    def receive(self, sRQName, sTrCode, sPrevNext):
        pass



class TrRequestBase(Logging, Line):
    def __init__(self):
        super().__init__()
        self.logging = Logging()


    def request(self, sPrevNext ="0"):
        pass

    def exitEventLoop(self):
        pass



class AccountNum(TrReceiveBase):

    def receive(self):
        self.logging = Logging()
        accountList = self.dynamicCall("GetLoginInfo(QString)", "ACCNO")
        accountNum = accountList.split(';')[0]
        self.accountNum = accountNum
        self.logging.logger.debug("계좌번호: %s" % accountNum)

    def getAccountNum(self):
        accountNum = self.accountNum
        return accountNum


class Deposit(TrReceiveBase):

    def receive(self, sRQName, sTrCode):
        self.logging = Logging()
        deposit = self.dynamicCall("GetCommData(QString,QString,int,QString)", sTrCode, sRQName, 0, "예수금")
        self.deposit = int(deposit)
        self.logging.logger.debug("예수금 %s" % self.deposit)
        Line.sendMessage(self, "예수금 %s" % self.deposit)

    def getDeposit(self):
        return self.deposit


class TotalBuyMoney(TrReceiveBase):

    def receive(self, sRQName, sTrCode):
        totalBuyMoney = self.dynamicCall("GetCommData(QString,QString,int,QString)", sTrCode, sRQName, 0, "총매입금액")
        self.totalBuyMoney = int(totalBuyMoney.strip())
        self.logging.logger.debug('총매입금액: %s' % (self.totalBuyMoney))

    def getTotalBuyMoney(self):
        return self.totalBuyMoney


class TotalProfitLossMoney(TrReceiveBase):

    def receive(self, sRQName, sTrCode):
        totalProfitLossMoney = self.dynamicCall("GetCommData(QString,QString,int,QString)", sTrCode, sRQName, 0,
                                                "총평가손익금액")
        self.totalProfitLossMoney = int(totalProfitLossMoney.strip())
        self.logging.logger.debug('총평가손익금액: %s' % (self.totalProfitLossMoney))

    def getTotalProfitLossMoney(self):
        return self.totalProfitLossMoney


class TotalProfitLossRate(TrReceiveBase):

    def receive(self, sRQName, sTrCode):
        totalProfitLossRate = self.dynamicCall("GetCommData(QString,QString,int,QString)", sTrCode, sRQName, 0,
                                               "총수익률(%)")
        self.totalProfitLossRate = float(totalProfitLossRate.strip())
        self.logging.logger.debug('총수익률: %s' % (self.totalProfitLossRate))

    def getTotalProfitLossRate(self):
        return self.totalProfitLossRate


class MyStockNumber(TrReceiveBase):

    def receive(self, sRQName, sTrCode):
        self.numberOfMystock = self.dynamicCall("GetRepeatCnt(QString,QString)", sTrCode, sRQName)  # 종목개수

    def getNumber(self):
        return self.numberOfMystock


class MyStockReceive(TrReceiveBase):
    def receive(self, sRQName, sTrCode, sPrevNext, index):
        code = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, index,
                                "종목번호")  # 출력 : A039423 // 알파벳 A는 장내주식, J는 ELW종목, Q는 ETN종목
        codeName = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, index,
                                    "종목명")  # 출럭 : 한국기업평가
        stockQuantity = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, index,
                                         "보유수량")  # 보유수량 : 000000000000010
        totalChegualPrice = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName,
                                             index, "매입금액")
        code = code.strip()[1:]
        codeName = codeName.strip()
        stockQuantity = int(stockQuantity.strip())
        totalChegualPrice = int(totalChegualPrice.strip())

        self.logging.logger.debug("종목코드: %s - 종목명: %s - 보유수량: %s - 매입금액:%s"
                                  % (code, codeName, stockQuantity, totalChegualPrice))

        return [code, codeName, stockQuantity, totalChegualPrice]

class NumberOfNotConcludedStock(TrReceiveBase):

    def receive(self, sRQName, sTrCode, sPrevNext):
        self.numberOfNotConcludedStock = self.dynamicCall("GetRepeatCnt(QString,QString)", sTrCode, sRQName)

    def getNumber(self):
        return self.numberOfNotConcludedStock


class NotConcludedStock(TrReceiveBase):
    def receive(self, sRQName, sTrCode, sPrevNext, index):
        code = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, index, "종목코드")
        codeName = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, index, "종목명")
        orderNo = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, index, "주문번호")
        orderStatus = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, index,
                                       "주문상태")  # 접수,확인,체결
        orderPrice = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, index,
                                      "주문가격")
        orderGubun = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, index,
                                      "주문구분")  # -매도, +매수, -매도정정, +매수정정
        notQuantity = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, index,
                                       "미체결수량")
        okQuantity = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, index,
                                      "체결량")
        originOrderNumber = ''
        code = code.strip()

        codeName = codeName.strip()
        orderNo = int(orderNo.strip())
        orderStatus = orderStatus.strip()
        orderPrice = int(orderPrice.strip())
        orderGubun = orderGubun.strip().lstrip('+').lstrip('-')
        notQuantity = int(notQuantity.strip())
        okQuantity = int(okQuantity.strip())

        self.logging.logger.debug(
            "종목코드: %s 종목명: %s 주문번호: %s 주문상태: %s 원주문번호: %s 주문가격: %s 주문구분: %s 미체결수량: %s 체결량: %s"
            % (code, codeName, orderNo, orderStatus, originOrderNumber, orderPrice, orderGubun, notQuantity,
               okQuantity))

        return [code, codeName, originOrderNumber, orderNo, orderStatus, orderPrice, orderGubun, notQuantity, okQuantity]

class ConditionName(TrReceiveBase):
    def receive(self, lRet, sMsg):
        self.logging.logger.debug("호출 성공 여부 %s, 호출결과 메시지 %s" % (lRet, sMsg))
        conditionNameList = self.dynamicCall("GetConditionNameList()")
        self.logging.logger.debug("HTS의 조건검색식 이름 가져오기 %s" % conditionNameList)
        return conditionNameList

class ConditionStock(TrReceiveBase):
    def receive(self, sScrNo, strCodeList, strConditionName, index, nNext):
        self.logging.logger.debug("화면번호: %s, 종목코드 리스트: %s, 조건식 이름: %s, 조건식 인덱스: %s, 연속조회: %s" % (
            sScrNo, strCodeList, strConditionName, index, nNext))

        codeList = strCodeList.split(";")[:-1]
        self.logging.logger.debug("코드 종목 \n %s" % codeList)
        return codeList

class MinutePriceData(TrReceiveBase):
    def receive(self, sRQName, sTrCode, sPrevNext):
        code = self.dynamicCall("GetCommData(QString,QString,int,QString)", sTrCode, sRQName, 0, "종목코드")
        data = self.dynamicCall("GetCommDataEx(QString,QString)", sTrCode, sRQName)
        return sPrevNext, code, data

class TickPriceData(TrReceiveBase):
    def receive(self, sRQName, sTrCode, sPrevNext):
        code = self.dynamicCall("GetCommData(QString,QString,int,QString)", sTrCode, sRQName, 0, "종목코드")
        data = self.dynamicCall("GetCommDataEx(QString,QString)", sTrCode, sRQName)
        return sPrevNext, code, data

class Ocx(QAxWidget):
    def __init__(self):
        super().__init__()

    def getInstance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")


class Login(TrRequestBase):

    def request(self):
        self.loginEventLoop = QEventLoop()
        self.dynamicCall("CommConnect()")
        self.loginEventLoop.exec_()

    def exitEventLoop(self):
        self.loginEventLoop.exit()

class MyStockRequest(TrRequestBase):
    def request(self, sPrevNext ="0", accountNum = None):
        self.accountMystockLoop = QEventLoop()
        self.screenNumber = '1000'

        self.dynamicCall("SetInputValue(QString,QString)", "계좌번호", accountNum)
        self.dynamicCall("SetInputValue(QString,QString)", "비밀번호", "0000")
        self.dynamicCall("SetInputValue(QString,QString)", "비밀번호입력매체구분", "00")
        self.dynamicCall("SetInputValue(QString,QString)", "조회구분", "1")
        self.dynamicCall("CommRqData(QString,QString,int,QString)", "계좌평가잔고내역요청", "opw00018", sPrevNext,
                         self.screenNumber)

        self.accountMystockLoop.exec_()

    def exitEventLoop(self):
        self.accountMystockLoop.exit()

class AccountInfo(TrRequestBase):

    def request(self, sPrevNext ="0", accountNum = None):
        self.accountInfoLoop = QEventLoop()
        self.screenNumber = '1000'

        self.dynamicCall("SetInputValue(QString,QString)", "계좌번호", accountNum)
        self.dynamicCall("SetInputValue(QString,QString)", "비밀번호", "0000")
        self.dynamicCall("SetInputValue(QString,QString)", "비밀번호입력매체구분", "00")
        self.dynamicCall("SetInputValue(QString,QString)", "조회구분", "1")
        self.dynamicCall("CommRqData(QString,QString,int,QString)", "예수금상세현황요청", "opw00001", sPrevNext,
                         self.screenNumber)
        self.accountInfoLoop.exec_()

    def exitEventLoop(self):
        self.accountInfoLoop.exit()

class NotConcludedAccount(TrRequestBase):

    def request(self, sPrevNext ="0", accountNum = None):
        self.notConcludedAccountLoop = QEventLoop()
        self.screenNumber = '1000'
        self.logging.logger.debug("미체결 종목 요청")
        self.dynamicCall("SetInputValue(QString,QString)", '계좌번호', accountNum)
        self.dynamicCall("SetInputValue(QString,QString)", '체결구분', "1")
        self.dynamicCall("SetInputValue(QString,QString)", '매매구분', "0")
        self.dynamicCall("CommRqData(QString,QString,int,QString)", "실시간미체결요청", "opt10075", sPrevNext,self.screenNumber)
        self.notConcludedAccountLoop.exec_()

    def exitEventLoop(self):
        self.notConcludedAccountLoop.exit()


class Condition(TrRequestBase):

    def request(self):
        self.conditionLoop = QEventLoop()
        self.dynamicCall('GetConditionLoad()')
        self.conditionLoop.exec_()

    def exitEventLoop(self):
        self.conditionLoop.exit()


class MinutePrice(TrRequestBase):

    def request(self, code,sPrevNext ="0"):
        self.minutePriceLoop = QEventLoop()
        self.screenMinutePrice = '4000'
        self.dynamicCall("SetInputValue(QString, QString)", "종목코드", code)
        self.dynamicCall("SetInputValue(QString, QString)", "틱범위", "1")
        self.dynamicCall("SetInputValue(QString, QString)", "수정주가구분", "1")
        self.dynamicCall("CommRqData(QString,QString,int,QString)", "주식분봉차트조회", "opt10080", sPrevNext, self.screenMinutePrice)
        self.minutePriceLoop.exec_()

    def exitEventLoop(self):
        self.minutePriceLoop.exit()


class TickPrice(TrRequestBase):

    def request(self, code, sPrevNext ="0"):
        self.tickPriceLoop = QEventLoop()
        self.screenTickData = '8000'
        self.dynamicCall("SetInputValue(QString, QString)", "종목코드", code)
        self.dynamicCall("SetInputValue(QString, QString)", "틱범위", "1")
        self.dynamicCall("SetInputValue(QString, QString)", "수정주가구분", "1")
        self.dynamicCall("CommRqData(QString,QString,int,QString)", "주식틱차트조회", "opt10079", sPrevNext,
                         self.screenTickData)
        self.tickPriceLoop.exec_()

    def exitEventLoop(self):
        self.tickPriceLoop.exit()


class MyStock(MyStockReceive, MyStockRequest):
    pass


