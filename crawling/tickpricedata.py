from trading.trading import *
from kiwoom.other.transaction import *
import pandas as pd
import sys
from kiwoom.other.standard import *
from crawling.minutepricedata import *

class TickPriceData(MinutePriceData):
    def __init__(self):
        super().__init__()
        self.requestAllStockTickData()



    def requestAllStockTickData(self):
        companyDataFrame = pd.read_excel("C:/Users/PC/PycharmProjects/systemtrading_platform/db/kosdaq상장회사.xls")
        tmpDataFrame = pd.read_excel("C:/Users/PC/PycharmProjects/systemtrading_platform/db/kospi상장회사.xls")
        companyDataFrame = pd.concat([companyDataFrame, tmpDataFrame], axis=0)

        for code in companyDataFrame['종목코드']:
            QTest.qWait(3600)
            code = Standard.standardCode(self, code)
            print(code)
            Tr.requestTickPriceData(self, code)

        QTest.qWait(10000)
