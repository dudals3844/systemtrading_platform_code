import pandas as pd
from config.log_class import *

class NotConcludedMedoStockData():
    def __init__(self):
        self.notConcludedMedoDataFrame = pd.DataFrame(
            columns=['종목코드', '종목명', '주문번호', '원주문번호', '주문상태', '주문가격', '주문구분', '미체결수량', '체결량'])
        self.logging = Logging()
        self.saveData()

    def appnedData(self, code, codeName, orderNo, originOrderNumber, orderStatus, orderPrice, orderGubun, notQuantity,
                   okQuantity):
        if orderGubun == '매도':
            tmpList = [
                [code, codeName, orderNo, originOrderNumber, orderStatus, orderPrice, orderGubun, notQuantity,
                 okQuantity]]
            tmpDataFrame = pd.DataFrame(tmpList,
                                        columns=['종목코드', '종목명', '주문번호', '원주문번호', '주문상태', '주문가격', '주문구분', '미체결수량',
                                                 '체결량'],
                                        index=[orderNo])
            self.notConcludedMedoDataFrame = self.notConcludedMedoDataFrame.append(tmpDataFrame)
            self.notConcludedMedoDataFrame.drop_duplicates(['주문번호'], keep='last', inplace=True)
            if notQuantity == 0:
                self.notConcludedMedoDataFrame = self.notConcludedMedoDataFrame.drop([orderNo])
            self.logging.logger.debug(
                "매도 미체결 종목코드: %s 종목명: %s 주문번호: %s 주문상태: %s 원주문번호: %s 주문가격: %s 주문구분: %s 미체결수량: %s 체결량: %s"
                % (code, codeName, orderNo, orderStatus, originOrderNumber, orderPrice, orderGubun, notQuantity,
                   okQuantity))
            self.saveData()

    def findNotConcludedOrderNumberList(self, code):
        tmpList = []
        for i in range(len(self.notConcludedMedoDataFrame)):
            _code = self.notConcludedMedoDataFrame['종목코드'].iloc[i]
            okQuantity = self.notConcludedMedoDataFrame['체결량'].iloc[i]
            orderNumber = self.notConcludedMedoDataFrame['주문번호'].iloc[i]
            orderStatus = self.notConcludedMedoDataFrame['주문상태'].iloc[i]
            if orderStatus == '접수' or okQuantity == 0 and code == _code:
                orderNumber = self.standardOrderNumber(orderNumber)
                tmpList.append(orderNumber)
        return tmpList


    def findNotConcludedNumber(self):
        sum = self.notConcludedMedoDataFrame['미체결수량'].sum(axis=0)
        return sum

    def getDataFrame(self):
        return self.notConcludedMedoDataFrame

    def standardOrderNumber(self, orderNumber):
        orderNumber = "{0:0>7}".format(orderNumber)  # 오류안나게 종목코드 6자리 맞춰줌
        return orderNumber

    def deleteRow(self, orderNum):
        try:
            self.notConcludedMedoDataFrame.drop([orderNum], inplace=True)
        except:
            pass


    def saveData(self):
        self.notConcludedMedoDataFrame.to_csv(
            "C:/Users/PC/PycharmProjects/systemtrading_platform/strategy/hft/현재매도체결상태.csv", mode="w")