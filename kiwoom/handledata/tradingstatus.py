import pandas as pd
from config.log_class import *


class TradingStatus():
    def __init__(self):
        self.tradingStatusDataFrame = pd.DataFrame(columns=['종목코드', '매수', '매도'])



    def appendData(self, code, mesu = False, medo = False):
        tmpList = [[code, mesu, medo]]
        tmpDataFrame = pd.DataFrame(tmpList, index=[code], columns=['종목코드', '매수', '매도'])
        self.tradingStatusDataFrame = self.tradingStatusDataFrame.append(tmpDataFrame)
        self.tradingStatusDataFrame.drop_duplicates(['종목코드'], keep='last', inplace=True)
        self.saveData()

    def saveData(self):
        self.tradingStatusDataFrame.to_csv("C:/Users/PC/PycharmProjects/systemtrading_platform/db/mystock/거래상태.csv", mode="w")

    def hasData(self, code):
        try:
            self.tradingStatusDataFrame.loc[code]
            return True
        except:
            return False

    def findData(self, code):
        mesu = self.tradingStatusDataFrame['매수'].loc[code]
        medo = self.tradingStatusDataFrame['매도'].loc[code]
        return mesu, medo

    def modifyMesuData(self, code, mesu = None):
        self.tradingStatusDataFrame['매수'].loc[code] = mesu
        self.saveData()

    def modifyMedoData(self, code, medo=None):
        self.tradingStatusDataFrame['매도'].loc[code] = medo
        self.saveData()

    def isMesuData(self, code):
        status = self.tradingStatusDataFrame['매수'].loc[code]
        return status

    def isMedoData(self, code):
        status = self.tradingStatusDataFrame['매도'].loc[code]
        return status



