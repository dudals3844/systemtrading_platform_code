import pandas as pd
from config.log_class import *
from line.line import *
from kiwoom.data.data import *

class Condition(Line):
    def __init__(self):
        self.logging = Logging()
        self.conditionDataFrame = pd.DataFrame(columns=['조건식번호', '조건식이름'])

    def conditionNameListToConditionDataFrame(self, conditionNameList):
        conditionNameList = conditionNameList.split(";")[:-1]
        for unitCondition in conditionNameList:

            index = unitCondition.split("^")[0]
            index = int(index)
            conditionName = unitCondition.split("^")[1]
            self.logging.logger.debug("조건식 분리 번호: %s, 이름: %s" % (index, conditionName))
            tmpList = [[index, conditionName]]
            tmpDataFrame = pd.DataFrame(tmpList, columns=['조건식번호', '조건식이름'])
            self.conditionDataFrame = self.conditionDataFrame.append(tmpDataFrame)
        DataFrameToCSV.saveData(self, dataFrame=self.conditionDataFrame, savePath='C:/Users/PC/PycharmProjects/systemtrading_platform/db/mystock/조건식명단.csv')

    def getConditionDataFrame(self):
        conditionDataFrame = self.conditionDataFrame
        return conditionDataFrame

    def findData(self, index):
        idx = self.conditionDataFrame['조건식번호'].iloc[index]
        conditionName = self.conditionDataFrame['조건식이름'].iloc[index]
        return idx, conditionName

