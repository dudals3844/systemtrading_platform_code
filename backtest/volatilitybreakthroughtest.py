import pandas as pd
import numpy as np
import sqlite3


class VolatilityBreakthroughTest():

    def __init__(self):
        self.alphaList = []
        self.con = sqlite3.connect('db/DayPrice.db')

        companyDataFrame = self.readCompanyDataFrame()
        for i in range(len(companyDataFrame)):
            companyName = companyDataFrame['기업명'].iloc[i]
            code = companyDataFrame['종목코드'].iloc[i]
            code = self.standardCode(code)
            priceDataFrame = self.readCompanyPrice(code)
            totalAlpha = self.calculateAlphaMonth(priceDataFrame)
            spread = self.calculateMesuSpread(priceDataFrame)
            volume = self.calculateVolume(priceDataFrame)
            self.alphaList.append([code, companyName, totalAlpha, spread, volume])
            print(code,' ', companyName, totalAlpha, ' ', spread, ' ', volume)


        self.allCompanyAlphaDataFrame = pd.DataFrame(self.alphaList, columns=['종목코드', '기업명', '수익률', '매수등락가', '거래량'])
        self.allCompanyAlphaDataFrame.dropna(inplace=True)
        self.allCompanyAlphaDataFrame.sort_values(by=['수익률'], axis=0, ascending=False, inplace=True)
        self.allCompanyAlphaDataFrame.to_csv("C:/Users/PC/PycharmProjects/systemtrading_platform/db/변동성돌파전략수익률.csv")



    def standardCode(self, code):
        code = "{0:0>6}".format(code)  # 오류안나게 종목코드 6자리 맞춰줌
        return code



    def readCompanyDataFrame(self):
        companyDataFrame = pd.read_excel("C:/Users/PC/PycharmProjects/systemtrading_platform/db/kosdaq상장회사.xls")
        tmpDataFrame = pd.read_excel("C:/Users/PC/PycharmProjects/systemtrading_platform/db/kospi상장회사.xls")
        companyDataFrame = pd.concat([companyDataFrame, tmpDataFrame], axis=0)
        return companyDataFrame


    def readCompanyPrice(self, code):
        try:
            #priceDataFrame = pd.read_excel('C:/Users/PC/PycharmProjects/systemtrading_platform/db/price/' + companyName + '.xlsx')
            code = 'DAY_'+code+'_TB'
            priceDataFrame = pd.read_sql('select * from '+ code, con=self.con)
            return priceDataFrame
        except:
            pass

    def calculateAlphaMonth(self, priceDataFrame):
        try:
            if len(priceDataFrame) > 31:
                tmpList = []
                for i in range(0, 30):
                    todayStart = priceDataFrame['시가'].iloc[i]
                    todayEnd = priceDataFrame['종가'].iloc[i]
                    todayHigh = priceDataFrame['고가'].iloc[i]
                    yesterdayHigh = priceDataFrame['고가'].iloc[i + 1]
                    yesterdayLow = priceDataFrame['저가'].iloc[i + 1]
                    spread = yesterdayHigh - yesterdayLow
                    standard = todayStart + spread * 0.5
                    if todayHigh > standard and todayStart != 0:
                        profit = todayEnd - standard
                        alpha = profit / todayStart
                        tmpList.append(alpha + 1)


                alphaArray = np.array(tmpList)
                totalAlpha = np.prod(alphaArray) - 1
                return totalAlpha


            else:
                print('상장된지 얼마 안됨')
                return 0

        except:
            pass

    def calculateMesuSpread(self, priceDataFrame):
        try:
            high = priceDataFrame['고가'].iloc[0]
            low = priceDataFrame['저가'].iloc[0]
            spread = (high - low) * 0.5
            if spread == 0:
                spread = None
            return spread
        except:
            pass

    def calculateVolume(self, priceDataFrame):
        try:
            priceDataFrame = priceDataFrame.head(30)
            volume = priceDataFrame['거래량'].mean(axis=0)
            return volume
        except:
            pass

if __name__ == '__main__':
    VolatilityBreakthroughTest()