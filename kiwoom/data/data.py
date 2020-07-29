from abc import *
import pandas as pd

class appendDataBase(metaclass=ABCMeta):
    @abstractmethod
    def appendData(self):
        pass


class saveDataBase(metaclass=ABCMeta):
    @abstractmethod
    def saveData(self, dataFrame, savePath):
        pass


class findDataBase(metaclass=ABCMeta):
    @abstractmethod
    def findData(self):
        pass

    @abstractmethod
    def hasData(self):
        pass

class returnDataBase(metaclass=ABCMeta):
    @abstractmethod
    def returnData(self, dataFrame):
        pass


class Data(appendDataBase, findDataBase, returnDataBase):
    pass

class DataFrameToCSV(saveDataBase):
    def saveData(self, dataFrame, savePath):
        dataFrame.to_csv(savePath, mode='w')