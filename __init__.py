from PyQt5.QtWidgets import *
from trading.default import *
from strategy.scalping.scalping import *
sys.path.append("C:/Users/PC/PycharmProjects/systemtrading_platform/")
class Main():
    def __init__(self):
        print("메인 시작")


        self.app = QApplication(sys.argv)
        DefaultTrading()
        self.app.exec_()


if __name__ == "__main__":


    Main()
