from abc import *

class appendDataBase(metaclass=ABCMeta):
    @abstractmethod
    def append(self):
        pass


class saveDataBase(metaclass=ABCMeta):
    @abstractmethod
    def save(self, dataFrame, savePath):
        pass