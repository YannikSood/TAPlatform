from wsb2 import comment_write
from wsb2 import comment_write2
from Stock import Stock
from textblob import TextBlob
from urllib.request import urlopen
from bs4 import BeautifulSoup
import socket
import sys
import datetime
MENTION_LIMIT= 10
from mail_me import send_mail
class wsb():
    def __init__(self,ticker,prin, c,txtfile): 
        self.ticker = ticker 
        self.sensum = 0.0
        self.bbsentsum = 0.0
        self.sentcount = 0
        self.bull = 0
        self.bear = 0
        self.prin = prin
        self.avg_sent = 0.0
        self.holder = ''
        i=0
        com = open(txtfile,"r")
        for line in com:
            title = line
            if ticker in str(title):
                floc = str(title).find(self.ticker) #location of tickerr
                if floc != -1:
                    if floc == 0:  # if first element
                        if prin:
                            print(title)
                        self.sent(title)
                    elif not str(title)[floc-1].isalpha(): #if is not preceded by letter to prevent HAT from finding T
                        if prin:
                            print(title)
                        self.sent(title)
        com.close()
        # avg calculations
        self.avg_sent = 0.0
        self.bb_avg_sent = 0.0
        self.g_score = 0.0
        self.rec = 0
        if self.sentcount != 0:
            self.avg_sent = self.sensum/self.sentcount
            self.bb_avg_sent = self.bbsentsum/self.sentcount
            try:
                self.g_score = float(self.bull)/float(self.bear)
                if self.g_score >= 2.0:
                    self.rec = 1
                elif self.g_score <= 0.5:
                    self.rec = -1
                self.g_score = str(self.g_score)[:5]
            except:
                self.g_score = float(self.bull)
                pass
        if c and self.sentcount >= MENTION_LIMIT:
            self.result()
    
    #find sentiment
    def sent(self, post): 
        a = TextBlob(str(post))
        senthold = a.sentiment.polarity
        '''
            bbsent idea is that a poor sentiment about a put is a positive change 
            a positive sentiment about a put is also a positive 
                -i.e. RIP my dumb bad puts 
                gives negative sentiment but indicates percent gain
        '''
        bbsent = senthold
        if " call" in post or " bull" in post:
            self.bull+=1
        if " put" in post or " bear" in post:
            bbsent = bbsent*-1
            self.bear+=1 
        
        self.bbsentsum+=bbsent
        self.sensum+=senthold
        self.sentcount+=1

    def result(self):
        print("\n" + self.ticker)
        print("sentiment: " + str(self.avg_sent)[0:6])
        print("bull bear sentiment: " + str(self.bb_avg_sent)[0:6])
        print("mentions: " + str(self.sentcount))
        print("bull: "+str(self.bull))
        print("bear: "+str(self.bear))
        print("G-Score: "+str(self.g_score))
        self.holder = self.ticker +"\n"
        self.holder+="sentiment: " + str(self.avg_sent)[0:6] +"\n"
        self.holder+="bull bear sentiment: " + str(self.bb_avg_sent)[0:6] +"\n"
        self.holder+="mentions: " + str(self.sentcount) +"\n"
        self.holder+="bull: "+str(self.bull) + "\n"
        self.holder+="bear: "+str(self.bear) + "\n"
        self.holder+="G-Score: "+str(self.g_score)+"\n"
        if self.rec == 1:
            self.holder+="G-Rec: UP\n"
        elif self.rec == -1:
            self.holder+="G-Rec: DOWN\n"
        else:
            self.holder+="G-Rec: N\n"
def all(p,c,com_count,h,d,txtfile,readFile):
    email_mess = ""
    f = open(readFile, "r")
    #f = open("After.txt", "r")
    #f = open("Before.txt", "r")
    ticker = ""
    sentt = 0.0
    sentc = 0
    bull = 0
    bear = 0
    bb = 0.0
    wsb_obj = ''
    g_score = 0.0
    match = 0.0
    matchcount = 0.0
    for line in f:
        if line[0:-1] == "A" or line[0:-1] == "IV":
            line = "!@^^^%&$(#*)@(@(((!^#&$*JHDHYHUhugiIUGI"
        wsb_obj = wsb(line[0:-1] + " ",p,c,txtfile)
        if len(wsb_obj.holder) > 20:
            email_mess = email_mess + "\n"+wsb_obj.holder
        if d and wsb_obj.sentcount>10:
            s = Stock(line[0:-1])
            print(s.Price + " " + s.Change)
            matchcount += 1.0
            if "-" in s.Change and "-" in str(wsb_obj.bb_avg_sent):
                print("Match")
                match+=1.0
            elif not "-" in str(wsb_obj.bb_avg_sent) and "+" in s.Change:
                print("Match")
                match+=1.0
            else:
                print("No Match")

        if float(wsb_obj.avg_sent)*h > float(sentt)*h and int(wsb_obj.sentcount) >= int(com_count):
            sentt = wsb_obj.avg_sent
            bb = wsb_obj.bb_avg_sent
            ticker = wsb_obj.ticker
            sentc = wsb_obj.sentcount
            bull = wsb_obj.bull
            bear = wsb_obj.bear
            g_score = wsb_obj.g_score

    
    print("\n")
    if h == 1.0:    
        print("Most Loved: " + ticker)
    else:
        print("Most Hated: " + ticker)
    print("sentiment: " + str(sentt)[0:6])
    print("bull bear sentiment: " + str(bb)[0:6])
    print("mentions: " + str(sentc))
    print("bull: "+str(bull))
    print("bear: "+str(bear))
    print("G-Score: "+str(g_score))
    if matchcount>0:
        print("Match percentage: "+ str(match/matchcount))
    f.close()
    return email_mess

def earnings():
    quote_page = 'https://www.nasdaq.com/earnings/earnings-calendar.aspx' #?date=2019-May-09
    to = datetime.datetime.today()
    to = to + datetime.timedelta(days = 1)
    month = ['nill','January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'September', 'October', 'November', 'December']
    tomorowpage = quote_page+"?date="+ str(to.year)+"-"+str(month[to.month])+"-"+str(to.day).zfill(2)
    try:
            page = urlopen(quote_page,timeout = 5)
            page2 = urlopen(tomorowpage,timeout = 5)
    except socket.timeout:
            print("socket timeout catch")
            return False
    BAWrite("After.txt",page)
    BAWrite("Before.txt",page2)
    

def BAWrite(location, page):
    soup = BeautifulSoup(page, 'html.parser')
    table = soup.find_all("tr")
    strsearch = "Pre"
    if "After" in location:
        strsearch = "After Hours"
    i = 1
    f2 = open(location,"w+")
    while i < len(table):
        data = table[i].find_all("a")
        if len(data)<2:
            break
        if strsearch in str(data[0]):
            hold = data[1].get_text()
            tick = hold[hold.find("(")+1:hold.find(")")]
            if "The" in tick:
                hold = hold[hold.find(")")+1:]
                tick = hold[hold.find("(")+1:hold.find(")")]
            f2.write(tick+"\n")    

        i+=1
    f2.close()
    
def main():
    p = False
    a = False
    c = False
    d = False
    h = 1.0
    txtfile = "com.txt"
    com_count = 0
    for i in range(1,len(sys.argv)):
        if ".txt" in sys.argv[i]:
            txtfile = "old/"+str(sys.argv[i])
    for i in range(1,len(sys.argv)):
        if "e" in sys.argv[i]:
            mail_obj = send_mail()
            earnings()
            try:
                com_count = sys.argv[i+1]
            except:
                pass
            a = True
            if "all" in sys.argv[i]:
                messholder = ""
                af_holder = ""
                bef_holder = ""
                afterheader = "Stocks to Watch for with earnings after hours:"
                af_holder += all(c,True,com_count,h,d,txtfile,"After.txt")
                #af_holder += all(c,True,com_count,h,d,txtfile,"After.txt")
                beforeheader = "\nStocks to Watch for with earnings before hours:"
                bef_holder += all(c,True,com_count,h,d,txtfile,"Before.txt")
                
                if len(af_holder) > 10:
                    messholder+=afterheader
                    messholder+=af_holder
                    mail_obj.append_msg(messholder)
                    af_placer = af_holder.replace("\n\n","\n~\n")[1:]
                    af_placer+="~\n"
                    f = open("yest.txt","a")
                    f.write(af_placer)
                    f.close()
            #        mail_obj.send()
                if len(bef_holder) > 10:
                    messholder = ""
                    messholder+=beforeheader
                    messholder+=bef_holder
                    mail_obj.append_msg(messholder)
                    bef_placer = bef_holder.replace("\n\n","\n~\n")[1:]
                    bef_placer+="~\n"
                    f = open("yest.txt","a")
                    f.write(bef_placer)
                    f.close()
                if len(bef_holder) > 10 or len(af_holder) > 10:
                    mail_obj.send()
            elif "a" in sys.argv[i]:
                all(c,True,com_count,h,d,txtfile,"After.txt")
            elif "b" in sys.argv[i]:
                all(c,True,com_count,h,d,txtfile,"Before.txt")
            else:
                all(c,True,com_count,h,d,txtfile,"sap.txt")
            return
        if "h" in sys.argv[i]:
            print("\n\t-u Update comments (takes around a min)\n\t\t-u2 Update version 2 looks at all comments\n\t\t-y puts it in a current dater")
            print("\t-c Includes WSB commnets")
            print("\t-p prints the mentions and sentiment (only for -a)")
            print("\t-a searches all WSB stocks to find the most loved follow with number of set min threshhold i.e. -a 9")
            print("\t-l changes most loved to most hates")
            print("\t-e places the companies reporting before and after hours in the before and after txt files\n\t\t-a or -b before or after hours earnigns report")
            print("\t-d prints the daily change price")
            print("\t.txt file reads from the txt files in the old/ written by the -y tag\n")
            return
        if "u" in sys.argv[i]:
            y = False
            if "y" in sys.argv[i]:
                y = True
            if "2" in sys.argv[i]:
                print("Updating v2   biiiiiiig data  this gonna take a while")
                try:
                    sub = sys.argv[i+1]
                except:
                    sub = 'wallstreetbets'
                    comment_write2(sub,y)
            else:
                print("Updating")
                try:
                    sub = sys.argv[i+1]
                except:
                    sub = 'wallstreetbets'
                comment_write(sub)
        if "c" in sys.argv[i]:
            c = True
        if "p" in sys.argv[i]:
            p = True
        if "l" in sys.argv[i]:
            h = -1.0
        if "d" in sys.argv[i]:
            d = True
        if "a" in sys.argv[i]:
            try:
                com_count = sys.argv[i+1]
            except:
                pass
            a = True
            all(c,p,com_count,h,d,txtfile,"sap.txt")
        

        
    w = ''
    if not a:
        inp = input("Ticker: ")
        w = wsb(inp + " ",c,True,txtfile)
        if d:
            s = Stock(inp)
            print(s.Price + " " + s.Change)
    if "-x" in sys.argv[i]:
        l_store = w.holder.split("\n")
        l_store = l_store[1:-3]
        to_load = ""
        for i in range(len(l_store)):
            to_load +=l_store[i]+"\n"
        
        f = open("TEST.txt","w")
        f.write(to_load)
        f.close()



if __name__ == "__main__":
    main()
    
