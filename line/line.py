import requests
import threading
# 라인 메신저에 메시지 보내기
class Line():
    def __init__(self):
        pass

    def Messaging(self, message):
        try:

            TARGET_URL = 'https://notify-api.line.me/api/notify'
            TOKEN = 'HVX82OYkOm1ijw3Yex3HXrcupo2nr3N7iwLygWZu4Mv'

            response = requests.post(
                TARGET_URL,
                headers={
                    'Authorization': 'Bearer ' + TOKEN
                },
                data={
                    'message': message
                }
            )

        except Exception as ex:
            print(ex)


    def sendMessage(self, message):
        th = threading.Thread(target=self.Messaging, args=(message,))
        th.start()


