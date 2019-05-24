import smtplib 
from email.mime.text import MIMEText

class MailServer:
    def __init__(self):
        self.s = smtplib.SMTP('smtp.gmail.com', 587)
        self.s.starttls()


    def sendmessage(self, message_text, sub):
        msg = MIMEText(message_text)
        # Authentication 
        msg['Subject'] = sub
        self.s.login("boldpredictionscmu@gmail.com", "boldmld1") #POC only, else store this password in an encrypted format 
        # sending the mail 
        self.s.sendmail("boldpredictionscmu@gmail.com", ["vishwass@andrew.cmu.edu","vishwassin@gmail.com","liz2@andrew.cmu.edu","weiweihu@andrew.cmu.edu","atumu@andrew.cmu.edu"], msg.as_string())
        #POC only, read these values from a config file

        # terminating the session 
        self.s.quit()