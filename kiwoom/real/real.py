from abc import *
from PyQt5.QAxContainer import *
from config.log_class import *
from config.kiwoomType import *

class RealReceiveBase(QAxWidget):
    def __init__(self):
        super().__init__()
        self.logging = Logging()


    def receive(self, sCode, sRealType):
        pass


class RealRequestBase(QAxWidget):
    def __init__(self):
        super().__init__()
        self.logging = Logging()

    def request(self):
        pass



class MyStock(RealReceiveBase):
    def receive(self):
        codeName = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['잔고']['종목명'])
        codeName = codeName.strip()

        code = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['잔고']['종목코드'])[1:]

        stockQuantity = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['잔고']['보유수량'])
        stockQuantity = int(stockQuantity)

        totalBuyPrice = self.dynamicCall("GetChejanData(int)",
                                         self.realType.REALTYPE['잔고']['총매입가'])  # 계좌에 있는 종목의 총매입가
        totalBuyPrice = int(totalBuyPrice)

        return code, codeName, stockQuantity, totalBuyPrice

class NotConcludedAccount(RealReceiveBase):
    def receive(self) -> list:
        code = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['주문체결']['종목코드'])[1:]

        codeName = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['주문체결']['종목명'])
        codeName = codeName.strip()

        orderNo = self.dynamicCall("GetChejanData(int)",
                                   self.realType.REALTYPE['주문체결']['주문번호'])  # 출럭: 0115061 마지막 주문번호
        originOrderNumber = self.dynamicCall("GetChejanData(int)",
                                             self.realType.REALTYPE['주문체결']['원주문번호'])  # 출력 : defaluse : "000000"

        orderStatus = self.dynamicCall("GetChejanData(int)",
                                       self.realType.REALTYPE['주문체결']['주문상태'])  # 출력: 접수, 확인, 체결

        orderPrice = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['주문체결']['주문가격'])  # 출력: 21000
        orderPrice = int(orderPrice)

        orderGubun = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['주문체결']['주문구분'])  # 출력: -매도, +매수
        orderGubun = orderGubun.strip().lstrip('+').lstrip('-')

        notQuantity = self.dynamicCall("GetChejanData(int)",
                                       self.realType.REALTYPE['주문체결']['미체결수량'])  # 출력: 15, default: 0
        notQuantity = int(notQuantity)

        okQuantity = self.dynamicCall("GetChejanData(int)",
                                      self.realType.REALTYPE['주문체결']['체결량'])
        if okQuantity != '':
            okQuantity = int(okQuantity)
        else:
            okQuantity = 0

        return [code, codeName, orderNo, originOrderNumber, orderStatus, orderPrice, orderGubun, notQuantity, okQuantity]

class ChegulPrice(RealReceiveBase):
    def receive(self, sCode, sRealType) -> list:
        chegulTime = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                      self.realType.REALTYPE[sRealType]['체결시간'])  # 출력 HHMMSS
        nowPrice = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                    self.realType.REALTYPE[sRealType]['현재가'])  # 출력 : +(-)2520
        nowPrice = abs(int(nowPrice))

        spread = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                  self.realType.REALTYPE[sRealType]['전일대비'])  # 출력 : +(-)2520
        spread = int(spread)

        spreadRate = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                      self.realType.REALTYPE[sRealType]['등락율'])  # 출력 : +(-)12.98
        spreadRate = float(spreadRate)

        medoHoGa = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                    self.realType.REALTYPE[sRealType]['(최우선)매도호가'])  # 출력 : +(-)2520
        medoHoGa = abs(int(medoHoGa))

        mesuHoGa = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                    self.realType.REALTYPE[sRealType]['(최우선)매수호가'])  # 출력 : +(-)2515
        mesuHoGa = abs(int(mesuHoGa))

        volume = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                  self.realType.REALTYPE[sRealType]['거래량'])  # 출력 : +240124  매수일때, -2034 매도일 때
        volume = abs(int(volume))

        volumeSum = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                     self.realType.REALTYPE[sRealType]['누적거래량'])  # 출력 : 240124
        volumeSum = abs(int(volumeSum))

        high = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                self.realType.REALTYPE[sRealType]['고가'])  # 출력 : +(-)2530
        high = abs(int(high))

        start = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                 self.realType.REALTYPE[sRealType]['시가'])  # 출력 : +(-)2530
        start = abs(int(start))

        low = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                               self.realType.REALTYPE[sRealType]['저가'])  # 출력 : +(-)2530
        low = abs(int(low))

        return [chegulTime, nowPrice, spread, spreadRate, medoHoGa, mesuHoGa, volume, volumeSum, high, start, low]

class HogaPrice(RealReceiveBase):
    def receive(self, sCode, sRealType) -> list:
        hogaTime = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                    self.realType.REALTYPE[sRealType]['호가시간'])
        medo_1 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                  self.realType.REALTYPE[sRealType]['매도호가1'])
        medo_1 = int(medo_1)
        medo_1_Quantity = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                           self.realType.REALTYPE[sRealType]['매도호가수량1'])

        mesu_1 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                  self.realType.REALTYPE[sRealType]['매수호가1'])
        mesu_1 = int(mesu_1)
        mesu_1_Quantity = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                           self.realType.REALTYPE[sRealType]['매수호가수량1'])

        medo_2 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                  self.realType.REALTYPE[sRealType]['매도호가2'])
        medo_2 = int(medo_2)
        medo_2_Quantity = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                           self.realType.REALTYPE[sRealType]['매도호가수량2'])
        mesu_2 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                  self.realType.REALTYPE[sRealType]['매수호가2'])
        mesu_2 = int(mesu_2)
        mesu_2_Quantity = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                           self.realType.REALTYPE[sRealType]['매수호가수량2'])

        medo_3 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                  self.realType.REALTYPE[sRealType]['매도호가3'])
        medo_3 = int(medo_3)
        medo_3_Quantity = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                           self.realType.REALTYPE[sRealType]['매도호가수량3'])
        mesu_3 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                  self.realType.REALTYPE[sRealType]['매수호가3'])
        mesu_3 = int(mesu_3)
        mesu_3_Quantity = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                           self.realType.REALTYPE[sRealType]['매수호가수량3'])

        medo_4 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                  self.realType.REALTYPE[sRealType]['매도호가4'])
        medo_4 = int(medo_4)
        medo_4_Quantity = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                           self.realType.REALTYPE[sRealType]['매도호가수량4'])
        mesu_4 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                  self.realType.REALTYPE[sRealType]['매수호가4'])
        mesu_4 = int(mesu_4)
        mesu_4_Quantity = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                           self.realType.REALTYPE[sRealType]['매수호가수량4'])

        medo_5 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                  self.realType.REALTYPE[sRealType]['매도호가5'])
        medo_5 = int(medo_5)
        medo_5_Quantity = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                           self.realType.REALTYPE[sRealType]['매도호가수량5'])
        mesu_5 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                  self.realType.REALTYPE[sRealType]['매수호가5'])
        mesu_5 = int(mesu_5)
        mesu_5_Quantity = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                           self.realType.REALTYPE[sRealType]['매수호가수량5'])

        medo_6 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                  self.realType.REALTYPE[sRealType]['매도호가6'])
        medo_6 = int(medo_6)
        medo_6_Quantity = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                           self.realType.REALTYPE[sRealType]['매도호가수량6'])
        mesu_6 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                  self.realType.REALTYPE[sRealType]['매수호가6'])
        mesu_6 = int(mesu_6)
        mesu_6_Quantity = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                           self.realType.REALTYPE[sRealType]['매수호가수량6'])

        medo_7 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                  self.realType.REALTYPE[sRealType]['매도호가7'])
        medo_7 = int(medo_7)
        medo_7_Quantity = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                           self.realType.REALTYPE[sRealType]['매도호가수량7'])
        mesu_7 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                  self.realType.REALTYPE[sRealType]['매수호가7'])
        mesu_7 = int(mesu_7)
        mesu_7_Quantity = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                           self.realType.REALTYPE[sRealType]['매수호가수량7'])

        medo_8 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                  self.realType.REALTYPE[sRealType]['매도호가8'])
        medo_8 = int(medo_8)
        medo_8_Quantity = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                           self.realType.REALTYPE[sRealType]['매도호가수량8'])
        mesu_8 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                  self.realType.REALTYPE[sRealType]['매수호가8'])
        mesu_8 = int(mesu_8)
        mesu_8_Quantity = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                           self.realType.REALTYPE[sRealType]['매수호가수량8'])

        medo_9 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                  self.realType.REALTYPE[sRealType]['매도호가9'])
        medo_9 = int(medo_9)
        medo_9_Quantity = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                           self.realType.REALTYPE[sRealType]['매도호가수량9'])
        mesu_9 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                  self.realType.REALTYPE[sRealType]['매수호가9'])
        mesu_9 = int(mesu_9)
        mesu_9_Quantity = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                           self.realType.REALTYPE[sRealType]['매수호가수량9'])

        medo_10 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                   self.realType.REALTYPE[sRealType]['매도호가10'])
        medo_10 = int(medo_10)
        medo_10_Quantity = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                            self.realType.REALTYPE[sRealType]['매도호가수량10'])
        mesu_10 = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                   self.realType.REALTYPE[sRealType]['매수호가10'])
        mesu_10 = int(mesu_10)
        mesu_10_Quantity = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                            self.realType.REALTYPE[sRealType]['매수호가수량10'])

        totalMedoHoga = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                         self.realType.REALTYPE[sRealType]['매도호가총잔량'])
        totalMesuHoga = self.dynamicCall("GetCommRealData(QString, int)", sCode,
                                         self.realType.REALTYPE[sRealType]['매수호가총잔량'])

        return [sCode, hogaTime, mesu_1, medo_1, mesu_1_Quantity, medo_1_Quantity, mesu_2, medo_2, mesu_2_Quantity, medo_2_Quantity, mesu_3, medo_3, mesu_3_Quantity, medo_3_Quantity, mesu_4, medo_4, mesu_4_Quantity, medo_4_Quantity, mesu_5, medo_5, mesu_5_Quantity, medo_5_Quantity,
                mesu_6, medo_6, mesu_6_Quantity, medo_6_Quantity, mesu_7, medo_7, mesu_7_Quantity, medo_7_Quantity, mesu_8, medo_8, mesu_8_Quantity, medo_8_Quantity, mesu_9, medo_9, mesu_9_Quantity, medo_9_Quantity, mesu_10, medo_10, mesu_10_Quantity, medo_10_Quantity, totalMesuHoga, totalMedoHoga]

class JangStatus(RealReceiveBase):
    def receive(self, sCode, sRealType):
        fid = self.realType.REALTYPE[sRealType]['장운영구분']
        value = self.dynamicCall("GetCommRealData(QString,int)", sCode, fid)
        return value

class ConditionRealStock(RealReceiveBase):
    def receive(self, strCode, strType, strConditionName, strConditionIndex):
        self.logging.logger.debug(
            "종목코드: %s, 이벤트종류: %s, 조건식이름: %s, 조건명인덱스: %s" % (strCode, strType, strConditionName, strConditionIndex))

        if strType == "I":
            self.logging.logger.debug("종목코드: %s, 종목편입: %s" % (strCode, strType))
            return strCode, strType

        elif strType == "D":
            self.logging.logger.debug("종목코드: %s, 종목이탈: %s" % (strCode, strType))
            return strCode, strType

class JangCheck(RealRequestBase):
    def __init__(self):
        self.screenStartStopReal = '1000'

    def request(self):
        self.dynamicCall("SetRealReg(QString,QString,QString,QString)", self.screenStartStopReal, '',
                         self.realType.REALTYPE['장시작시간']['장운영구분'], "0")

class Chegul(RealRequestBase):
    def __init__(self):
        self.screenRealChegulPrice = '3000'

    def request(self, code):
        fids = self.realType.REALTYPE['주식체결']['체결시간']
        code = self.standard.standardCode(code)
        self.dynamicCall('SetRealReg(QString,QString,QString,QString)', self.screenRealChegulPrice, code, fids, "1")

class Hoga(RealRequestBase):
    def __init__(self):
        self.screenHoga = '9009'

    def request(self, code):
        fids = self.realType.REALTYPE['주식호가잔량']['매도호가1']
        code = self.standard.standardCode(code)
        self.dynamicCall('SetRealReg(QString,QString,QString,QString)', self.screenHoga, code, fids, "1")

class RealCondition(RealRequestBase):
    def request(self, index, conditionName):
        ok = self.dynamicCall("SendCondition(QString, QString, int, int)", "0156", conditionName, index,
                              1)  # 조회요청 + 실시간 조회
        self.logging.logger.debug("조회 성공여부 %s " % ok)

class Real(MyStock, NotConcludedAccount, ChegulPrice, HogaPrice, JangStatus,
           ConditionRealStock, JangCheck, Chegul, Hoga, RealCondition):
    def __init__(self):
        super().__init__()