from urllib.request import urlopen
from bs4 import BeautifulSoup
import socket

class Stock():
    Ticker=''
    Price=''
    Change=''
    Previous_Close = ''
    Open = ''
    Bid = ''
    Ask = ''
    Day_Range = ''
    Fifty_Two_Week_Range = ''
    Volume = ''
    Avg_Volume = ''
    Market_Cap = ''
    Beta = ''
    PE_Ratio = ''
    EPS = ''
    Dividend = ''
    Y_Target = ''
    def __init__(self,ticker):
        check=self.getS(ticker)
        
        while check==False:
            print("Loop due to socket timeout")
            check=self.getS(ticker)
    def dump(self):
        for Key in self.json_stock:
            print(self.json_stock[Key])
        
    def getS(self,ticker):
        self.json_stock = {}
        self.Ticker=ticker.replace('\n','')
        quote_page = 'https://finance.yahoo.com/quote/'+self.Ticker
        
        try:
            page = urlopen(quote_page,timeout = 5)
        except socket.timeout:
            print("socket timeout catch")
            return False
        
        soup = BeautifulSoup(page, 'html.parser')
        priceSoup = soup.find("div",{"id":"quote-header-info"})
        self.Price = priceSoup.find("span",{"data-reactid":"14"}).get_text() 
        self.Change = priceSoup.find("span",{"data-reactid":"16"}).get_text()
        table = soup.find_all('table')
        cells1 = table[0].find_all('td')
        dcount = 0
        for i in range(0, len(cells1)):
            shold = cells1[i]
            if dcount == 1:
                self.json_stock['Previous_Close'] = shold.get_text()
            elif dcount == 3:
                self.json_stock['Open'] = shold.get_text()
            elif dcount == 5:
                self.json_stock['Bid'] = shold.get_text()
            elif dcount == 7:
                self.json_stock['Ask'] = shold.get_text()
            elif dcount == 9:
                self.json_stock['DayRange'] = shold.get_text()
            elif dcount == 11:
                self.json_stock['Fifty_Two_Week_Range'] = shold.get_text()
            elif dcount == 13:
                self.json_stock['Volume'] = shold.get_text()
            elif dcount == 15:
                self.json_stock['Avg_Volume'] = shold.get_text()
            dcount+=1

        cells2 = table[1].find_all('td')
        for i in range(0, len(cells2)):
            shold = cells2[i]
            if dcount == 17:
                self.json_stock['Market_Cap'] = shold.get_text()
            elif dcount == 19:
                self.json_stock['Beta'] = shold.get_text()
            elif dcount == 21:
                self.json_stock['PE_Ratio'] = shold.get_text()
            elif dcount == 23:
                self.json_stock['EPS'] = shold.get_text()
            elif dcount == 27:
                self.json_stock['Dividend'] = shold.get_text()
            elif dcount == 31:
                self.json_stock['Y_Target'] = shold.get_text()
            dcount+=1

        return True

    def get_json(self):
        return self.json_stock

def main():
    s = Stock("FB")
    print(s.get_json())
if __name__ == '__main__':
    main()
