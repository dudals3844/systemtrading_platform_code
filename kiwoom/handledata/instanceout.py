import pandas as pd
from config.log_class import *


class InstanceOut:
    def __init__(self):
        self.logging = Logging()
        self.instanceOutDataFrame = pd.DataFrame(columns=['즉시이탈'])

    def appendData(self, code):
        if not self.hasData(code):
            tmpDataFrame = pd.DataFrame([[False]], columns=['즉시이탈'], index=[code])
            self.instanceOutDataFrame = self.instanceOutDataFrame.append(tmpDataFrame)
            self.saveData()
            return True
        elif self.hasData(code):
            return False

    def hasData(self,code):
        try:
            self.instanceOutDataFrame.loc[code]
            return True
        except:
            return False

    def isInstanceOut(self,code):
        status = self.instanceOutDataFrame['즉시이탈'].loc[code]
        return status

    def modifyInstanceOutTrue(self, code):
        self.instanceOutDataFrame['즉시이탈'].loc[code] = True
        self.saveData()

    def modifyInstanceOutFalse(self, code):
        self.instanceOutDataFrame['즉시이탈'].loc[code] = False
        self.saveData()

    def saveData(self):
        self.instanceOutDataFrame.to_csv("C:/Users/PC/PycharmProjects/systemtrading_platform/db/mystock/즉시이탈.csv", mode="w")

    def deleteData(self,code):
        self.instanceOutDataFrame.drop([code], inplace=True)
        self.saveData()