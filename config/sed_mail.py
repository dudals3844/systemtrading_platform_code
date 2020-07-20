import smtplib
class Gmail():
    def __init__(self):
        self.fromaddress = 'dudals3844@gmail.com'
        self.toaddress = 'dudals3844@gmail.com'

        self.id = 'dudals3844'
        self.password = ''

        self.server = smtplib.SMTP('smtp.gmail.com:587')
        self.server.starttls()
        self.server.login(self.id, self.password)

    def send_mail(self,msg):
        msg = msg.encode('utf8')
        self.server.sendmail(self.fromaddress, self.toaddress, msg)



