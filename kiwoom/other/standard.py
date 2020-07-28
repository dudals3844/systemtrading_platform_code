from abc import *


class StandardBase(metaclass=ABCMeta):
    @abstractmethod
    def standard(self):
        pass

class Code(StandardBase):
    def standard(self, code):
        code = "{0:0>6}".format(code)  # 오류안나게 종목코드 6자리 맞춰줌
        return code

class OrderNumber(StandardBase):
    def standard(self,  orderNumber):
        orderNumber = "{0:0>7}".format(orderNumber)
        return orderNumber