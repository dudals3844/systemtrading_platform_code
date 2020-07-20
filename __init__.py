from PyQt5.QtWidgets import *
from strategy.volatilitybreakthroughstrategy import *
from crawling.tickpricedata import *
from strategy.movingaveragebreakthroughstrategy import *
from strategy.scalping.scalping import *
from strategy.hft.marketmaking import *
from backtest.volatilitybreakthroughtest import *
sys.path.append("C:/Users/PC/PycharmProjects/systemtrading_platform/")
class Main():
    def __init__(self):
        print("메인 시작")


        self.app = QApplication(sys.argv)
        #self.trading = Trading()
        #self.volatilitybreakthroughStrategy = VolatilityBreakthroughStrategy()
        #self.movingaveragebreakthrough = MovingAverageBreakThroughStrategy()
        #self.shotUp = ShotUpStrategy()
        # self.minutePrice = MinutePriceData()
        # self.tickPrice = TickPriceData()
        #self.scalping = Scalping()
        try:
            self.marketMaking = MarketMaking()
        except Exception as e:
            print(e)
        self.app.exec_()


if __name__ == "__main__":

    #VolatilityBreakthroughTest()
    Main()
