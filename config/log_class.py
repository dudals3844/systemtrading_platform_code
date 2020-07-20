import logging.config
from datetime import datetime

class Logging():
    def __init__(self, configPath ='config/logging.conf', logPath ='log'):
        self.configPath = configPath
        self.logPath = logPath

        logging.config.fileConfig(self.configPath)
        self.logger = logging.getLogger('Kiwoom')
        self.kiwoomLog()

    def kiwoomLog(self):
        fh = logging.FileHandler(self.logPath + '/{:%Y-%m-%d}.log'.format(datetime.now()), encoding='utf-8')
        formatter = logging.Formatter('[%(asctime)s] I %(filename)s | %(name)s-%(funcName)s-%(lineno)04d I %(levelname)-8s > %(message)s')

        fh.setFormatter(formatter)
        self.logger.addHandler(fh)