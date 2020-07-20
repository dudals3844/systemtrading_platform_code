import pandas as pd
from config.log_class import *
from kiwoom.other.standard import *
from line.line import *

class MyStock(Line):
    def __init__(self):
        self.logging = Logging()
        self.standard = Standard()
        self.mystockDataFrame = pd.DataFrame(columns=['종목명', '종목코드', '보유수량', '총매입가'])


    def appendData(self, code, codeName, stockQuantity, totalChegualPrice):
        self.logging.logger.debug("종목코드: %s - 종목명: %s - 보유수량: %s - 매입금액:%s"
                                  % (code, codeName, stockQuantity, totalChegualPrice))
        Line.sendMessage(self, "\n종목코드: %s\n종목명: %s\n보유수량: %s\n매입금액:%s"
                         % (code, codeName, stockQuantity, totalChegualPrice))
        code = self.standard.standardCode(code)
        if stockQuantity != 0:
            tmpList = [[codeName, code, stockQuantity, totalChegualPrice]]
            tmpDataFrame = pd.DataFrame(tmpList, columns=['종목명', '종목코드', '보유수량', '총매입가'], index=[code])
            self.mystockDataFrame = self.mystockDataFrame.append(tmpDataFrame)
        elif stockQuantity == 0:
            self.mystockDataFrame.drop([code], inplace = True)

        self.mystockDataFrame.drop_duplicates(['종목명'], keep='last', inplace=True)
        self.saveData()

    def saveData(self):
        self.mystockDataFrame.to_csv('C:/Users/PC/PycharmProjects/systemtrading_platform/db/mystock/보유종목.csv', mode='w')

    def hasData(self, code):
        try:
            self.mystockDataFrame.loc[code]
            return True
        except:
            return False

    def findData(self, code):
        codeName = self.mystockDataFrame['종목명'].loc[code]
        code = self.mystockDataFrame['종목코드'].loc[code]
        stockQuantity = self.mystockDataFrame['보유수량'].loc[code]
        totalChegualPrice = self.mystockDataFrame['총매입가'].loc[code]

        return codeName, code, stockQuantity, totalChegualPrice

    def findStockQuantitiyData(self, code):
        try:
            code = self.standard.standardCode(code)
            stockQuantity = self.mystockDataFrame['보유수량'].loc[code]
            stockQuantity = int(stockQuantity)
            return stockQuantity
        except:
            return 0

    def returnData(self):
        return self.mystockDataFrame



