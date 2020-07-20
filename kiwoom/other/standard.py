class Standard():
    def standardCode(self, code):
        code = "{0:0>6}".format(code)  # 오류안나게 종목코드 6자리 맞춰줌
        return code