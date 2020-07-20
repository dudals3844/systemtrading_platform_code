import pandas as pd
import matplotlib.pyplot as plt

##189p
## 수정해야됨 실제 값이랑 다름!!
class CommodityChannelIndex:
    def __init__(self, companyName):
        self.companyName = companyName
        self.priceDataFrame = self.readPriceDataFrame()
        # 최근 날짜가 제일 밑으로 다시 정렬
        self.priceDataFrame = self.priceDataFrame.sort_index(ascending=False)
        self.priceDataFrame.reset_index(drop=True, inplace=True)
        self.cci = self.calculateCommodityChannenlIndex()
        plt.plot(self.cci)
        plt.show()
    def readPriceDataFrame(self):
        priceDataFrame = pd.read_excel('C:/Users/PC/PycharmProjects/systemtrading_platform/db/price/'+self.companyName+'.xlsx')
        return priceDataFrame

    def calculateCommodityChannenlIndex(self):
        m = self.priceDataFrame['종가'].rolling(window=20).mean()

        tmp = self.priceDataFrame['종가'].add(self.priceDataFrame['저가'])
        tmp_2 = tmp.add(self.priceDataFrame['고가'])
        M = tmp_2.div(3)


        tmp_d = M.sub(m)
        d_av = tmp_d.rolling(window=20).mean()
        d = abs(d_av)
        Mm_tmp = M.sub(m)
        cci = Mm_tmp.div(d)
        cci = cci.mul(0.15)
        print(cci)
        return cci

if __name__=='__main__':
    CommodityChannelIndex(companyName='sk')