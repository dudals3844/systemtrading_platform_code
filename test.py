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
import sys
from PyQt5.QtWidgets import *

data = [[1,2,3],
        [4,5,6]]

df = pd.read_csv('C:/Users/PC/PycharmProjects/systemtrading_platform/db/mystock/보유종목.csv')

app = QApplication(sys.argv)
label = QLabel(str(df))
label.show()

app.exec_()