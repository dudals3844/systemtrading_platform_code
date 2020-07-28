from config.kiwoomType import *
from kiwoom.tr.tr import *
from abc import *

class OrderReqeustBase(metaclass=ABCMeta, QAxWidget, Line):
    def __init__(self):
        super().__init__()
        self.logging = Logging()
        self.realType = RealType()
        self.screenMemeStock = "6000"

    @abstractmethod
    def request(self):
        pass




class JijungMesuOrder(OrderReqeustBase):
    def request(self, sCode, mesuStockNum, mesuPrice):
        orderSuccess = self.dynamicCall("SendOrder(QString,QString,QString,int,QString,int,int,QString,QString)",
                                        ['신규매수', self.screenMemeStock, self.accountNum, 1, sCode, mesuStockNum,
                                         mesuPrice, self.realType.SENDTYPE['거래구분']['지정가'], ''])
        if orderSuccess == 0:
            self.logging.logger.debug('지정가 매수주문 전달 성공 종목코드: %s 수량: %s 매수가격: %s' % (sCode, mesuStockNum, mesuPrice))
            Line.sendMessage(self, '\n지정가 매수주문 전달 성공\n종목코드: %s\n수량: %s\n매수가격: %s' % (sCode, mesuStockNum, mesuPrice))
            return True
        else:
            self.logging.logger.debug('지정가 매수주문 전달 실패')
            return False

class MesuCancelOrder(OrderReqeustBase):
    def request(self, sCode, orderNum):
        orderSuccess = self.dynamicCall("SendOrder(QString,QString,QString,int,QString,int,int,QString,QString)",
                                        ['매수취소', self.screenMemeStock, self.accountNum, 3, sCode, 0,
                                         0, self.realType.SENDTYPE['거래구분']['지정가'], orderNum])
        if orderSuccess == 0:
            self.logging.logger.debug('지정가 매수취소 전달 성공 종목코드: %s 주문번호: %s' % (sCode, orderNum))
            Line.sendMessage(self, '지정가 매수취소 전달 성공\n종목코드: %s\n주문번호: %s' % (sCode, orderNum))
            return True
        else:
            self.logging.logger.debug('지정가 매수취소 전달 실패')
            return False

class SijangMesuOrder(OrderReqeustBase):
    def request(self, sCode, mesuStockNum):
        orderSuccess = self.dynamicCall("SendOrder(QString,QString,QString,int,QString,int,int,QString,QString)",
                                        ['신규매수', self.screenMemeStock, self.accountNum, 1, sCode, mesuStockNum,
                                         0, self.realType.SENDTYPE['거래구분']['시장가'], ''])
        if orderSuccess == 0:
            self.logging.logger.debug('시장가 매수주문 전달 성공 종목코드: %s 수량: %s ' % (sCode, mesuStockNum))
            Line.sendMessage(self, '\n시장가 매수주문 전달 성공\n종목코드: %s\n수량: %s ' % (sCode, mesuStockNum))
            return True
        else:
            self.logging.logger.debug('시장가 매수주문 전달 실패')
            return False

class JijunhMedoOrder(OrderReqeustBase):
    def request(self, sCode, medoStockNum, medoPrice):
        orderSuccess = self.dynamicCall("SendOrder(QString,QString,QString,int,QString,int,int,QString,QString)",
                                        ['신규매도', self.screenMemeStock, self.accountNum, 2, sCode, medoStockNum,
                                         medoPrice, self.realType.SENDTYPE['거래구분']['지정가'], ''])
        if orderSuccess == 0:
            self.logging.logger.debug('지정가 매도주문 전달 성공 종목코드: %s 수량: %s 매수가격: %s' % (sCode, medoStockNum, medoPrice))
            Line.sendMessage(self, '\n지정가 매도주문 전달 성공\n종목코드: %s\n수량: %s\n매수가격: %s' % (sCode, medoStockNum, medoPrice))
            return True
        else:
            self.logging.logger.debug('지정가 매도주문 전달 실패')
            return False

class MedoCancelOrder(OrderReqeustBase):
    def request(self, sCode, orderNum):
        orderSuccess = self.dynamicCall("SendOrder(QString,QString,QString,int,QString,int,int,QString,QString)",
                                        ['매도취소', self.screenMemeStock, self.accountNum, 4, sCode, 0,
                                         0, self.realType.SENDTYPE['거래구분']['지정가'], orderNum])
        if orderSuccess == 0:
            self.logging.logger.debug('지정가 매도취소 전달 성공 종목코드: %s  주문번호: %s' % (sCode, orderNum))
            Line.sendMessage(self, '\n지정가 매도취소 전달 성공\n종목코드: %s\n주문번호: %s' % (sCode, orderNum))
            return True
        else:
            self.logging.logger.debug('지정가 매도취소 전달 실패')
            return False

class SijangMedoOrder(OrderReqeustBase):
    def request(self, sCode, medoStockNum):
        orderSuccess = self.dynamicCall("SendOrder(QString,QString,QString,int,QString,int,int,QString,QString)",
                                        ['신규매도', self.screenMemeStock, self.accountNum, 2, sCode, medoStockNum,
                                         0, self.realType.SENDTYPE['거래구분']['시장가'], ''])
        if orderSuccess == 0:
            self.logging.logger.debug('시장가 매도주문 전달 성공 종목코드: %s 수량: %s' % (sCode, medoStockNum))
            Line.sendMessage(self, '\n시장가 매도주문 전달 성공\n종목코드: %s\n수량: %s' % (sCode, medoStockNum))
            return True
        else:
            self.logging.logger.debug('시장가 매도주문 전달 실패')
            return False

class Order(JijungMesuOrder, JijunhMedoOrder, MesuCancelOrder, MedoCancelOrder, SijangMesuOrder, SijangMedoOrder):
    def __init__(self):
        super().__init__()