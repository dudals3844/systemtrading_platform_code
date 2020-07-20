import requests
import sqlite3
from bs4 import BeautifulSoup as bs
import re
import pandas as pd

class CrawlingAlpha():
    def __init__(self):
        # self.con = sqlite3.connect('C:/Users/PC/PycharmProjects/systemtrading_platform/db/Alpha.db')
        self.companyDataFrame = self.readCompanyDataFrame()
        self.crawlingData()

    def readCompanyDataFrame(self):
        companyDataFrame = pd.read_excel("C:/Users/PC/PycharmProjects/systemtrading_platform/db/kosdaq상장회사.xls")
        tmpDataFrame = pd.read_excel("C:/Users/PC/PycharmProjects/systemtrading_platform/db/kospi상장회사.xls")
        companyDataFrame = pd.concat([companyDataFrame, tmpDataFrame], axis=0)
        return companyDataFrame

    def standard_code(self, code):
        code = "{0:0>6}".format(code)  # 오류안나게 종목코드 6자리 맞춰줌
        return code

    def crawlingData(self):
        betaList = []
        for i in range(len(self.companyDataFrame)):
            try:
                companyName = self.companyDataFrame['기업명'].iloc[i]
                code = self.companyDataFrame['종목코드'].iloc[i]
                code = self.standard_code(code)
                url = 'https://navercomp.wisereport.co.kr/v2/company/c1010001.aspx?cmp_cd={}'.format(code)
                source = requests.get(url)
                sour = bs(source.content, 'html.parser')
                key = sour.select('#cTB11 > tbody > tr:nth-child(6) > td')
                key = str(key)
                key = re.sub('<.+?>', '', key, 0)
                key = key.replace(" ", "")
                key = ''.join(key.split())
                key = key[1:5]
                key = float(key)
                tmpList = [code, companyName, key]
                print(tmpList)
                betaList.append(tmpList)
            except:
                pass

        betaDataFrame = pd.DataFrame(betaList, columns=['종목코드', '기업명', '베타'])
        # self.saveDataBase(tableName='Alpha_TB', dataFrame=alphaDataFrame)
        betaDataFrame.to_csv('C:/Users/PC/PycharmProjects/systemtrading_platform/db/베타.csv')

    def saveDataBase(self, tableName, dataFrame):
        dataFrame.to_sql(tableName, self.con)



if __name__ == '__main__':
    crawling = CrawlingAlpha()