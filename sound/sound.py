import playsound
from multiprocessing import Process

class Sound():
    def readBeforeJangStart(self):
        playsound.playsound("beforejangstart.mp3", True)

    def playBeforeJangStart(self):
        Process(target=self.readBeforeJangStart()).start()


    def readCancleMedoOrder(self):
        playsound.playsound("canclemedoorder.mp3", True)

    def playCancleMedoOrder(self):
        Process(target=self.readCancleMedoOrder()).start()

    def readCancleMesuOrder(self):
        playsound.playsound("canclemesuorder.mp3", True)

    def playCancleMesuOrder(self):
        Process(target=self.readCancleMesuOrder()).start()

    def readCaution(self):
        playsound.playsound("caution.mp3", True)

    def playCaution(self):
        Process(target=self.readCaution()).start()

    def readChagualMedoOrder(self):
        playsound.playsound("chegualmedoorder.mp3", True)

    def playChagualMedoOrder(self):
        Process(target=self.readChagualMedoOrder()).start()

    def readChagualMesuOrder(self):
        playsound.playsound("chegualmesuorder.mp3", True)

    def playChagualMesuOrder(self):
        Process(target=self.readChagualMesuOrder()).start()




if __name__ == "__main__":
    sound = Sound()
    # sound.playBeforeJangStart()
    # sound.playCancleMedoOrder()
    # sound.playCancleMesuOrder()
    # sound.readCaution()
    sound.readChagualMedoOrder()

    sound.playChagualMesuOrder()