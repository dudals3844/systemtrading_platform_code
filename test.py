import pandas as pd
import matplotlib.pyplot as plt
from threading import Thread
import threading
import time
import sqlite3
from bs4 import BeautifulSoup as bs
import requests
import re
from selenium import webdriver
import pyglet
from multiprocessing import Process, Queue
import _thread
import winsound
import playsound
import concurrent.futures
import asyncio
# class TMP:
#     def __int__(self):
#         self.tmp_str = 'hello'
#
#     def println(self):
#         print(self.tmp_str)
#
#
#
# #
# tmp = Thread(target=println, args=('hello',))
# # threading.Timer(1, println('hello',)).start()
# # threading.Timer(3, println('hello', )).start()
# tmp.start()
# tmp.join()
# print(2)
#
# if __name__ == '__main__':
#     def playSound():
#         playsound.playsound('sound/beforejangstart.mp3', True)
#
#     def playOtherSound():
#         playsound.playsound('sound/mesuorder.mp3', True)
#
#
#
#     t = Process(target=playSound())
#     t.start()
#     t2 = Process(target=playOtherSound())
#     time.sleep(2)
#     t2.start()
tmpList = [1,2,3,4]
tmpList2 = [5,6,7,8]
df = pd.DataFrame()

df['a'] = tmpList
df['a'] = tmpList2
df['b'] = tmpList
print(df)
for i in range(len(df['a'])):
    print(df['a'].iloc[i])



