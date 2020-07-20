import pandas as pd
import sqlite3

class TickPrice:
    def __init__(self):
        self.con = sqlite3.connect('db/TickPrice.db')

    def setPriceArray(self, priceArray, code):
        try:
            tickPriceDataFrame = pd.DataFrame(columns=['현재가', '거래량', '체결시간', '시가', '고가', '저가'])
            for i in range(len(priceArray)-1,-1, -1):
                nowPrice = priceArray[i][0]
                nowPrice = abs(int(nowPrice))
                volume = priceArray[i][1]
                time = priceArray[i][2]
                start = priceArray[i][3]
                start = abs(int(start))
                high = priceArray[i][4]
                high = abs(int(high))
                low = priceArray[i][5]
                low = abs(int(low))
                tmpList = [[nowPrice, volume, time, start, high, low]]
                tmpDataFrame = pd.DataFrame(tmpList, columns=['현재가', '거래량', '체결시간', '시가','고가','저가'])
                tickPriceDataFrame = tickPriceDataFrame.append(tmpDataFrame)

            code = code.replace(" ","")
            tickPriceDataFrame.reset_index(drop=True, inplace=True)
            # tickPriceDataFrame.to_csv('C:/Users/PC/PycharmProjects/systemtrading_platform/db/tickprice/'+code+'.csv')
            self.saveDataBase(tableName='TIC_'+code+'_TB', dataFrame=tickPriceDataFrame)

        except:
            pass


    def saveDataBase(self, tableName, dataFrame):
        dataFrame.to_sql(tableName, self.con)

    def disConnectDataBase(self):
        self.con.close()