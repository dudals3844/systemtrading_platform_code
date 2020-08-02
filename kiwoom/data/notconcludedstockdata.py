from kiwoom.data.data import *
import pandas as pd
from config.log_class import *
from kiwoom.other.standard import *
from line.line import *

class NotConcludedStockData(Line, Data):
    def __init__(self):
        self.logging = Logging()
        self.notConcludedAccountDataFrame = pd.DataFrame(
            columns=['종목코드', '종목명', '주문번호', '원주문번호', '주문상태', '주문가격', '주문구분', '미체결수량', '체결량'])


    def appendData(self, notConcludedStockInformationList):
        [code, codeName, originOrderNumber, orderNo, orderStatus, orderPrice, orderGubun, notQuantity, okQuantity] = notConcludedStockInformationList
        tmpDataFrame = pd.DataFrame(notConcludedStockInformationList,
                                    columns=['종목코드', '종목명', '주문번호', '원주문번호', '주문상태', '주문가격', '주문구분', '미체결수량', '체결량'],
                                    index=[code])
        self.logging.logger.debug(
            "종목코드: %s 종목명: %s 주문번호: %s 주문상태: %s 원주문번호: %s 주문가격: %s 주문구분: %s 미체결수량: %s 체결량: %s"
            % (code, codeName, orderNo, orderStatus, originOrderNumber, orderPrice, orderGubun, notQuantity,
               okQuantity))
        Line.sendMessage(self,
                         "\n종목코드: %s\n종목명: %s\n주문번호: %s\n주문상태: %s\n원주문번호: %s\n주문가격: %s\n주문구분: %s\n미체결수량: %s\n체결량: %s"
                         % (
                         code, codeName, orderNo, orderStatus, originOrderNumber, orderPrice, orderGubun, notQuantity,
                         okQuantity))
        self.notConcludedAccountDataFrame = self.notConcludedAccountDataFrame.append(tmpDataFrame)
        self.notConcludedAccountDataFrame.drop_duplicates(['종목명'], keep='last', inplace=True)
        DataFrameToCSV.saveData(self, dataFrame=self.notConcludedAccountDataFrame, savePath="C:/Users/PC/PycharmProjects/systemtrading_platform/db/mystock/미체결종목.csv")

    def hasData(self, code):
        try:
            self.notConcludedAccountDataFrame.loc[code]
            return True
        except:
            return False

    def findData(self, code) -> list:
        if self.hasData(code):
            code = self.notConcludedAccountDataFrame['종목코드'].loc[code]
            codeName = self.notConcludedAccountDataFrame['종목명'].loc[code]
            originOrderNumber = self.notConcludedAccountDataFrame['원주문번호'].loc[code]
            orderNo = self.notConcludedAccountDataFrame['주문번호'].loc[code]
            orderStatus = self.notConcludedAccountDataFrame['주문상태'].loc[code]
            orderPrice = self.notConcludedAccountDataFrame['주문가격'].loc[code]
            orderGubun = self.notConcludedAccountDataFrame['주문구분'].loc[code]
            notQuantity = self.notConcludedAccountDataFrame['미체결수량'].loc[code]
            okQuantity = self.notConcludedAccountDataFrame['체결량'].loc[code]
            return [code, codeName, originOrderNumber, orderNo, orderStatus, orderPrice, orderGubun, notQuantity, okQuantity]

    def returnData(self):
        return self.notConcludedAccountDataFrame

    def countData(self):
        countData = len(self.notConcludedAccountDataFrame)
        return countData