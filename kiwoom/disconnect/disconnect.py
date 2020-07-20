from PyQt5.QAxContainer import *

class Disconnect(QAxWidget):
    # 스크린 번호 끊기
    def disconnectScreen(self, sScrNo=None):
        self.dynamicCall("DisconnectRealData(QString)", sScrNo)

    # 실시간 데이터 끊기
    def disconnectRealData(self, sScrNo=None, code=None):
        # sScrNo는 스크린 번호
        self.dynamicCall("SetRealRemove(QString,QString)", sScrNo, code)