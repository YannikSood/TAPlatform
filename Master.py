import os
import subprocess
import sys
import datetime
import smtplib
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
class run():
    def __init__(self,selections,email):
        subprocess.check_output("python3 ML3.0.py s "+selections, shell=True)
        subprocess.check_output("python3 Load_create.py "+ selections, shell=True)
        result = subprocess.check_output("python3 ML3.0.py l", shell=True)
        print(str(result)[2:8])
        self.result = str(result)[2:8]
               
        self.server = smtplib.SMTP(host='smtp.gmail.com',port=587)
        self.server.ehlo()
        self.server.starttls()
        self.server.login("Stoneg.Stocks", "VTduq4et!")
        self.message = 'Based on your selected preference the all mighty and wise ML algorithm has predicted spy to change by '+ self.result+" tomorrow"
        me = "Stoneg.Stocks@gmail.com"
        you = email
    
        to = datetime.datetime.now()
        msg = MIMEMultipart()
        msg["To"] = you
        msg["From"] = me
        msg["Subject"] = "Subject: ML Guess " + str(to.month)+"/"+ str(to.day)+"/"+str(to.year)
        
        msgText = MIMEText('%s' % (self.message), 'html')  
        msg.attach(msgText)   # Added, and edited the previous line

            
        self.server.sendmail(me, you, msg.as_string())
        

if __name__ == "__main__":
    run(sys.argv[1],sys.argv[2])
