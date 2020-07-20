from trading.trading import *
from kiwoom.other.basictradinginformation import *
import pandas as pd
import sys


class VolatilityBreakthroughStrategy(Trading): # 변동성 돌파전략

    def __init__(self):
        super().__init__()
        BasicTradingInformation.setDeposit(self, Tr.getDeposit(self))
        BasicTradingInformation.setMarginRate(self, 40)
        BasicTradingInformation.setTradingNumber(self, 4)
        BasicTradingInformation.calculateTradingNumberUsingMargin(self)
        BasicTradingInformation.calculateOneTradingDeposit(self)


        # 변동성 전략에 맞는 종목 30개 데이터프레임으로 불러오기
        self.todayTradingCompanyDataFrame = pd.read_csv('C:/Users/PC/PycharmProjects/systemtrading_platform/db/변동성돌파전략수익률.csv')
        self.todayTradingCompanyDataFrame = self.todayTradingCompanyDataFrame[self.todayTradingCompanyDataFrame['거래량'] > 1000000]
        self.todayTradingCompanyDataFrame = self.todayTradingCompanyDataFrame.head(30)


        self.setTodayAllTradingDefaultStatus()
        self.changeTodayTradingMesuStatus()
        Real.requestRealJangCheck(self)

        # 장시간에 에러 났을떄 실시간 시세를 등록하기위해 사용
        self.requestAllRealChegualPrice()







    # Override
    def receiveRealdataSlot(self, sCode, sRealType, sRealData):
        if sRealType == "장시작시간":
            status = Real.receiveJangStatus(self, sCode, sRealType)
            if status == '0':
                self.logging.logger.debug('장 시작 전')

            elif status == '3':
                self.logging.logger.debug('장 시작')
                Line.sendMessage(self, '장 시작')
                self.medoAllStock()
                self.requestAllRealChegualPrice()


            elif status == '2':
                self.logging.logger.debug('장 종료후 동시호가')
                #self.medo_all_stock()

            elif status == '4':
                self.logging.logger.debug('3시 30분 장 종료')
                sys.exit()

        elif sRealType == "주식체결":
            chegul_time, now_price, spread, spread_rate, medo_ho_ga, mesu_ho_ga, volume, volume_sum, high, start, low = Real.receiveChegulPrice(self, sCode, sRealType)

            # self.logging.logger.debug("종목코드: %s  체결시간: %s 현재가: %s 등락: %s 등락률: %s 매도호가: %s 매수호가: %s 거래량: %s 거래량합:%s 고가: %s 시가: %s 저가: %s " %(sCode, chegul_time, now_price, spread, spread_rate, medo_ho_ga, mesu_ho_ga, volume, volume_sum, high, start, low))
            if self.isMesuTiming(sCode, start, now_price):
                if self.tradingStatus.isMesuData(sCode):
                    BasicTradingInformation.setNowTradingNumber(self, len(self.myStock.returnData()))
                    self.logging.logger.debug("현재 거래종목수: %s 증거금이용 거래가능 종목수: %s" % (BasicTradingInformation.getNowTradingNumber(self), BasicTradingInformation.getTradingNumberUsingMargin(self)))
                    if BasicTradingInformation.getNowTradingNumber(self) <= BasicTradingInformation.getTradingNumberUsingMargin(self):

                        Order.requestSijangMesuOrder(self, sCode, BasicTradingInformation.getHowManyStockMesu(self, now_price))
                        self.logging.logger.debug('종목코드: %s 주문수량: %s ' % (sCode, BasicTradingInformation.getHowManyStockMesu(self, now_price)))

                        self.tradingStatus.modifyMesuData(sCode, mesu=False)
                        self.tradingStatus.modifyMedoData(sCode, medo=True)



            # if self.isSonJeolTiming(sCode, now_price, high):
            #     if self.myStock.hasData(sCode):
            #         medo_stock_num = self.myStock.findStockQuantitiyData(sCode)
            #         self.requestSijangMedoOrder(sCode, medo_stock_num)
            #         self.tradingStatus.modifyMedoData(sCode, medo=False)


    # Override
    def receiveChejanSlot(self, sGubun, nItemCnt, sFidList):
        if int(sGubun) == 0: #주문체결
            code, code_nm, order_no, origin_order_number, order_status, order_price, order_gubun, not_quantity, ok_quantity = Real.receiveNotConcludedAccount(self)
            self.notConcludedStock.appendData(code, code_nm, order_no, origin_order_number, order_status, order_price, order_gubun, not_quantity, ok_quantity)
        elif int(sGubun) == 1: #잔고
            code, code_nm, stock_quantity, total_buy_price = Real.receiveMystock(self)
            self.myStock.appendData(code, code_nm, stock_quantity, total_buy_price)

    def medoAllStock(self):
        mystock = self.myStock.returnData()
        for i in range(len(mystock)):
            code = mystock['종목코드'].iloc[i]
            code = self.standard.standardCode(code)
            quantity = mystock['보유수량'].iloc[i]
            Order.requestSijangMedoOrder(self, code, quantity)


    def changeTodayTradingMesuStatus(self):
        for code in self.todayTradingCompanyDataFrame['종목코드']:
            code = self.standard.standardCode(code)
            self.tradingStatus.modifyMesuData(code, mesu=True)


    def setTodayAllTradingDefaultStatus(self):
        for index in range(len(self.todayTradingCompanyDataFrame)):
            code = self.todayTradingCompanyDataFrame['종목코드'].iloc[index]
            company = self.todayTradingCompanyDataFrame['기업명'].iloc[index]
            code = self.standard.standardCode(code)
            Line.sendMessage(self, "거래종목 %s %s" % (code, company))
            self.tradingStatus.appendData(code)

        mystock = self.myStock.returnData()
        for i in range(len(mystock)):
            code = mystock['종목코드'].iloc[i]
            company = mystock['종목명'].iloc[i]
            Line.sendMessage(self, "거래종목 %s %s" % (code, company))
            self.tradingStatus.appendData(code)



    def requestAllRealChegualPrice(self):
        for code in self.todayTradingCompanyDataFrame['종목코드']:
            code = self.standard.standardCode(code)
            Real.requestRealChegulPrice(self, code)






    # 매수 타이밍인지 확인
    def isMesuTiming(self, sCode, start, now_price):
        nowSpread = now_price - start
        sCode = self.standard.standardCode(sCode)
        for i in range(len(self.todayTradingCompanyDataFrame)):
            code = self.todayTradingCompanyDataFrame['종목코드'].iloc[i]
            code = self.standard.standardCode(code)
            spread = self.todayTradingCompanyDataFrame['매수등락가'].iloc[i]
            if code == sCode:
                if nowSpread > spread:
                    self.logging.logger.debug('기준통과 종목코드: %s 현재등락률: %s 기준등락률: %s' % (code, nowSpread, spread))
                    return True
                else:
                    return False

    # 손절 타이밍인지 확인
    def isSonJeolTiming(self, code, now_price, high):
        code = self.standard.standardCode(code)
        sonJeolPrice = 0.98 * high # 2% 떨어지면 손절
        # 종목상태가 매도인지 확인
        if self.tradingStatus.isMedoData(code):
            if now_price < sonJeolPrice:
                self.logging.logger.debug("손절타이밍 종모코드: %s 현재가: %s 손절가: %s " % (code, now_price, sonJeolPrice))
                return True
            else:
                return False
