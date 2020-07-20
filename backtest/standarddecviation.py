import pandas as pd
import sqlite3

class StandardDeviation:
    def __init__(self):
        self.con = sqlite3.connect('C:/Users/PC/PycharmProjects/systemtrading_platform/db/DayPrice.db')

        stdList = []
        calculateDays = 75
        companyDataFrame = self.readCompanyDataFrame()
        for i in range(len(companyDataFrame)):
            companyName = companyDataFrame['기업명'].iloc[i]
            if '스팩'not in companyName and '바다로'not in companyName and '하이골드'not in companyName and '케이프이에스'not in companyName:
                code = companyDataFrame['종목코드'].iloc[i]
                code = self.standardCode(code)
                try:
                    priceDataFrame = self.readCompanyPrice(code)
                    priceDataFrame = priceDataFrame.tail(calculateDays)
                    rateList = []
                    for i in range(calculateDays - 1):
                        rate = (priceDataFrame['종가'].iloc[i+1] - priceDataFrame['종가'].iloc[i])/priceDataFrame['종가'].iloc[i]
                        rateList.append(rate)
                    rateDataFrame = pd.DataFrame(rateList, columns=['수익률'])

                    std = rateDataFrame['수익률'].std()

                    closeMean = priceDataFrame['종가'].mean()
                    volume = priceDataFrame['거래량'].mean()
                    if std != 0 and closeMean > 1400 and volume > 5000000:
                        print(code,companyName,std)
                        tmpList = [code, companyName, std]
                        stdList.append(tmpList)
                except:
                    pass


        self.stdDataFrame = pd.DataFrame(stdList,columns=['종목코드', '기업명', '표준편차'])
        self.stdDataFrame = self.stdDataFrame.sort_values(['표준편차'], ascending=True)
        self.stdDataFrame.to_csv("C:/Users/PC/PycharmProjects/systemtrading_platform/db/전종목표준편차.csv")

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

    def standardCode(self, code):
        code = "{0:0>6}".format(code)  # 오류안나게 종목코드 6자리 맞춰줌
        return code


if __name__ == '__main__':
    StandardDeviation()