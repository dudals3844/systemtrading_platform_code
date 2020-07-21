import pandas as pd
from config.log_class import *


class NotConcludedMesuStock():
    def __init__(self):
        self.notConcludedMesuDataFrame = pd.DataFrame(columns=['종목코드', '종목명', '주문번호', '원주문번호', '주문상태', '주문가격', '주문구분', '미체결수량', '체결량'])
        self.logging = Logging()
        self.saveData()

    def appnedData(self, code, codeName, orderNo, originOrderNumber, orderStatus, orderPrice, orderGubun, notQuantity, okQuantity):
        if orderGubun == '매수':
            tmpList = [
                [code, codeName, orderNo, originOrderNumber, orderStatus, orderPrice, orderGubun, notQuantity,
                 okQuantity]]
            tmpDataFrame = pd.DataFrame(tmpList,
                                        columns=['종목코드', '종목명', '주문번호', '원주문번호', '주문상태', '주문가격', '주문구분', '미체결수량', '체결량'],
                                        index=[orderNo])
            self.notConcludedMesuDataFrame = self.notConcludedMesuDataFrame.append(tmpDataFrame)
            self.notConcludedMesuDataFrame.drop_duplicates(['주문번호'], keep='last', inplace=True)
            if notQuantity == 0:
                self.notConcludedMesuDataFrame = self.notConcludedMesuDataFrame.drop([orderNo])
            self.logging.logger.debug(
                "미체결 매수 종목코드: %s 종목명: %s 주문번호: %s 주문상태: %s 원주문번호: %s 주문가격: %s 주문구분: %s 미체결수량: %s 체결량: %s"
                % (code, codeName, orderNo, orderStatus, originOrderNumber, orderPrice, orderGubun, notQuantity,
                   okQuantity))
            self.saveData()

    def findNotConcludedOrderNumberList(self, code):
        tmpList = []
        for i in range(len(self.notConcludedMesuDataFrame)):
            _code = self.notConcludedMesuDataFrame['종목코드'].iloc[i]
            okQuantity = self.notConcludedMesuDataFrame['체결량'].iloc[i]
            orderNumber = self.notConcludedMesuDataFrame['주문번호'].iloc[i]
            orderStatus = self.notConcludedMesuDataFrame['주문상태'].iloc[i]
            if orderStatus == '접수' and okQuantity == 0 and code == _code:
                orderNumber = self.standardOrderNumber(orderNumber)
                tmpList.append(orderNumber)

        return tmpList

    def findNotConcludedNumber(self):
        sum = self.notConcludedMesuDataFrame['미체결수량'].sum(axis=0)
        return sum

    def getDataFrame(self):
        return self.notConcludedMesuDataFrame


    def deleteRow(self, orderNum):
        try:
            self.notConcludedMesuDataFrame.drop([orderNum], inplace=True)
        except:
            pass


    def standardOrderNumber(self, orderNumber):
        orderNumber = "{0:0>7}".format(orderNumber)  # 오류안나게 종목코드 6자리 맞춰줌
        return orderNumber


    def saveData(self):
        self.notConcludedMesuDataFrame.to_csv(
            "C:/Users/PC/PycharmProjects/systemtrading_platform/strategy/hft/현재매수체결상태.csv", mode="w")


if __name__ == '__main__':
    nt = NotConcludedMesuStock()
    nt.standardOrderNumber(orderNumber=816)