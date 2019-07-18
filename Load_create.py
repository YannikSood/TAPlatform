import datetime
import wsb3
import sys
import Stock
class load():
    def __init__(self,selections):
        hold = Stock.Stock("SPY").get_json()

        now = datetime.datetime.now()
        wsbfile = "old/C_"+str(now.month)+"_"+str(now.day)+"_"+str(now.year)+".txt"
        wsb3obj = wsb3.wsb('',False,False,wsbfile)
        HT = {  "S":str(wsb3obj.avg_sent)[0:6],
                "A":str(wsb3obj.bb_avg_sent)[0:6],
                "M":str(wsb3obj.sentcount),
                "B":str(wsb3obj.bull),
                "E":str(wsb3obj.bear),
                "G":str(wsb3obj.g_score),
                "V":str(hold["Volume"]).replace(",","")
        }
        f = open("TEST.txt", "w")
        for char in selections:
            f.write(HT[char]+"\n")
        f.close()

if __name__ == "__main__":
    selections = sys.argv[1]
    load(selections)
