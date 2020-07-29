import pandas as pd

class HogaPrice():
    def __init__(self):
        # self.hogaDataFrame = pd.DataFrame(columns=['종목코드','호가시간','매수1호가','매도1호가','매수1호가수량','매도1호가수량','매수2호가','매도2호가','매수2호가수량','매도2호가수량','매수3호가','매도3호가','매수3호가수량','매도3호가수량','매수4호가','매도4호가','매수4호가수량','매도4호가수량','매수5호가','매도5호가','매수5호가수량','매도5호가수량','매수6호가','매도6호가','매수6호가수량','매도6호가수량','매수7호가','매도7호가','매수7호가수량','매도7호가수량','매수8호가','매도8호가','매수8호가수량','매도8호가수량','매수9호가','매도9호가','매수9호가수량','매도9호가수량','매수10호가','매도10호가','매수10호가수량','매도10호가수량','총매수호가','총매도호가'])
        self.hogaPriceDataFrame = pd.DataFrame()


    def appendColumnData(self, sCode, hogaTime, mesu_1, medo_1, mesu_1_Quantity, medo_1_Quantity, mesu_2, medo_2, mesu_2_Quantity,medo_2_Quantity,mesu_3,medo_3,mesu_3_Quantity,medo_3_Quantity,mesu_4,medo_4,mesu_4_Quantity,medo_4_Quantity,mesu_5,medo_5,mesu_5_Quantity,medo_5_Quantity,mesu_6,medo_6,mesu_6_Quantity,medo_6_Quantity,mesu_7,medo_7,mesu_7_Quantity,medo_7_Quantity,mesu_8,medo_8,mesu_8_Quantity,medo_8_Quantity,mesu_9, medo_9,mesu_9_Quantity,medo_9_Quantity, mesu_10,medo_10,mesu_10_Quantity,medo_10_Quantity,totalMesuHoga,totalMedoHoga):
        tmpList = [medo_10, medo_9, medo_8, medo_7, medo_6, medo_5, medo_4, medo_3, medo_2, medo_1, mesu_1, mesu_2, mesu_3, mesu_4, mesu_5, mesu_6, mesu_7, mesu_8, mesu_9, mesu_10]
        self.hogaPriceDataFrame[sCode] = tmpList
        self.saveData()

    def hasData(self, code):
        try:
            self.hogaPriceDataFrame[code]
            return True
        except:
            return False

    def findIndex(self, code, price):
        try:
            for i in range(len(self.hogaPriceDataFrame[code])):
                tmpPrice = self.hogaPriceDataFrame[code].iloc[i]
                if tmpPrice == price:
                    return i
        except:
            return -1
    def getDataFrame(self, code):
        return self.hogaPriceDataFrame[code]

    def saveData(self):
        self.hogaPriceDataFrame.to_csv("C:/Users/PC/PycharmProjects/systemtrading_platform/strategy/hft/호가가격.csv",mode='w')