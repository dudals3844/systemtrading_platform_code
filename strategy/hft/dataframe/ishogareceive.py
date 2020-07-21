import pandas as pd
from kiwoom.other.standard import *

class IsHogaReceive():
    def __init__(self):
        self.isHogaReceiveDataFrame = pd.DataFrame(columns=['종목코드', '호가도착'])
        self.standardCode = Standard()
        self.saveData()

    def inputDefaultData(self, code):
        if not self.hasData(code):
            code = self.standardCode.standardCode(code)
            tmpDataFrame = pd.DataFrame([[code,False]], columns=['종목코드', '호가도착'], index=[code])
            self.isHogaReceiveDataFrame = self.isHogaReceiveDataFrame.append(tmpDataFrame)
            self.isHogaReceiveDataFrame.drop_duplicates(['종목코드'], keep='last', inplace=True)
            self.saveData()

    def hasData(self, code):
        try:
            self.isHogaReceiveDataFrame.loc[code]
            return True
        except:
            return False

    def isReceive(self, code):
        status = self.isHogaReceiveDataFrame['호가도착'].loc[code]
        return status

    def getDataFrame(self):
        return self.isHogaReceiveDataFrame

    def modifyIsHogaReceiveTrue(self, code):
        self.isHogaReceiveDataFrame['호가도착'].loc[code] = True

    def saveData(self):
        self.isHogaReceiveDataFrame.to_csv("C:/Users/PC/PycharmProjects/systemtrading_platform/strategy/hft/호가도착.csv",mode='w')
