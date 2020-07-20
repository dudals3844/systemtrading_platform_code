from selenium import webdriver
import os
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import xlsxwriter
import re
import datetime
import sys
from backtest.volatilitybreakthroughtest import *
sys.path.append('C:/Users/PC/PycharmProjects/systemtrading_platform/crawling/')

class CrawlingData():

    def __init__(self):
        # 테스트 속도를 위해 잠시 주석처리
        #self.delete_file(file_dr='C:/Users/PC/PycharmProjects/systemtrading_platform/db/상장회사.xls')
        #self.delete_file(file_dr="C:/Users/PC/Downloads/data.xls")
        #self.download_company_data()
        company_df = self.read_excel_to_dataframe('C:/Users/PC/PycharmProjects/systemtrading_platform/db/상장회사.xls')
        print(company_df)
        #self.crawling_all_company_price_data(company_df)
        self.crwling_all_company_price_data_update(company_df)
        #크롤링후 백테스트
        VolatilityBreakthroughTest()

    # 상장회사 엑셀 다운로드
    def download_company_data(self):
        driver = webdriver.Chrome("C:/Users/PC/PycharmProjects/systemtrading_platform/driver/chromedriver.exe")
        driver.implicitly_wait(2)
        driver.get('http://marketdata.krx.co.kr/mdi#document=040601')
        driver.find_element_by_xpath('//*[@id="6f4922f45568161a8cdf4ad2299f6d23"]/button[2]').click()
        # 다운될때까지 기다리기
        time.sleep(3)
        self.change_file_name_and_directory(origin_dr="C:/Users/PC/Downloads/data.xls",
                                            change_dr='C:/Users/PC/PycharmProjects/systemtrading_platform/db/상장회사.xls')

        driver.close()

    # 파일 삭제
    def delete_file(self, file_dr):
        if os.path.isfile(file_dr):
            os.remove(file_dr)

    # 코드번호 형식 맞추기
    def standard_code(self, code):
        code = "{0:0>6}".format(code)  # 오류안나게 종목코드 6자리 맞춰줌
        return code

    # 파일 이름과 폴더 경로 변경
    def change_file_name_and_directory(self, origin_dr, change_dr):
        os.rename(origin_dr, change_dr)

    # 엑셀 파일로 데이터 프레임 읽기
    def read_excel_to_dataframe(self, file_dr):
        df = pd.read_excel(file_dr)
        return df

    # 데이터 프레임을 엑셀로 저장
    def save_dataframe_as_excel(self, save_folder, dataframe,file_name):
        file_dr = save_folder + file_name + '.xlsx'
        writer = pd.ExcelWriter(file_dr, engine='xlsxwriter')
        dataframe.to_excel(writer, sheet_name='price')
        writer.close()

    # 상장된 회사들 전체 가격 저장
    def crwling_all_company_price_data(self, company_df):
        pattern = re.compile("(\d+)")
        for i in range(0, len(company_df)):
            stock = pd.DataFrame()
            code = self.standard_code(company_df['종목코드'][i])

            url = "https://finance.naver.com/item/sise_day.nhn?code={}&page={}"
            try:
                last = pattern.findall(
                    bs(requests.get(url.format(code, 1)).text, 'html.parser').find("td",class_='pgRR').find("a")['href'])[-1]
            except:
                last = 1
            for cnt in range(1, int(last) + 1):
                data = pd.read_html(url.format(code,cnt))[0].dropna()
                stock = stock.append(data)

            stock.reset_index(drop=True, inplace=True)
            self.save_dataframe_as_excel(save_folder='C:/Users/PC/PycharmProjects/systemtrading_platform/db/price/',
                                         file_name=company_df['기업명'][i],
                                         dataframe=stock)

    def crwling_all_company_price_data_update(self, company_df):
        for i in range(0, len(company_df)):
            stock_df = pd.read_excel('C:/Users/PC/PycharmProjects/systemtrading_platform/db/price/'+company_df['기업명'][i]+'.xlsx')
            tmp_df = None

            code = self.standard_code(company_df['종목코드'][i])
            url = "https://finance.naver.com/item/sise_day.nhn?code={}"

            tmp_df = pd.read_html(url.format(code))[0].dropna()


            tmp_df = tmp_df.append(stock_df)
            tmp_df.drop(['Unnamed: 0'],axis='columns', inplace=True)
            tmp_df.drop_duplicates(['날짜'], inplace=True)
            tmp_df.reset_index(drop=True, inplace=True)
            tmp_df.dropna(axis = 'columns', inplace = True)
            self.save_dataframe_as_excel(save_folder='C:/Users/PC/PycharmProjects/systemtrading_platform/db/price/',
                                         file_name=company_df['기업명'][i],
                                         dataframe=tmp_df)




if __name__ =="__main__":
    crawlingData = CrawlingData()