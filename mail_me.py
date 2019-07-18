import smtplib
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
class send_mail():
    def __init__(self):
        self.server = smtplib.SMTP(host='smtp.gmail.com',port=587)
        self.server.ehlo()
        self.server.starttls()
	####
        self.server.login("email", "passowrd")
        ###
	self.message = ''
    def append_msg(self, msg):
        self.message = self.message + "\n" + msg
    def send(self):
        to = datetime.datetime.today()
        disclaimer = '''All recomendations are wild guesses based upon possibly poor and untested market data.\nFollow any of these tips a your own risk
        \n\n
        Guess tally:
        Right 9, Wrong 1, No Change 3\n
        The Guess tally is recorded data based on the price change at open the day after a recommendation.\nRight means the stock moved in guessed direction        more than +/-1%.  \nNo change means the price moved between -1% and 1%.  \nWrong means the stock moved opposite the guess greater than +/-1%.'''
        me = "Stoneg.Stocks@gmail.com"
        you = "stoneg@vt.edu"
        attachment = 'Logo.gif'

        msg = MIMEMultipart()
        msg["To"] = you
        msg["From"] = me
        msg["Subject"] = "Subject: Daily Stocks " + str(to.month)+"/"+ str(to.day)+"/"+str(to.year)
        self.message = self.message.replace("\n","<br>\n")
        
        msgText = MIMEText('<b></b><br>%s<br><img src="cid:%s"><br>%s<br>' % (self.message, attachment,disclaimer), 'html')  
        msg.attach(msgText)   # Added, and edited the previous line

        fp = open(attachment, 'rb')                                                    
        img = MIMEImage(fp.read())
        fp.close()
        img.add_header('Content-ID', '<{}>'.format(attachment))
        msg.attach(img)
        f = open("mailers.txt","r")
        #f = open("testmail.txt","r")
        try:
            for line in f:
                self.server.sendmail(me, line, msg.as_string())
        except:
            pass
