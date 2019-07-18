from flask import Flask
from flask import request
import Stock
app = Flask(__name__)
import Master
import os

@app.route("/")
def homepage():
    f = open("home.html","r")
    lines = f.read()
    return lines


@app.route('/stock/<ticker>')
def index(ticker):
    return Stock.Stock(str(ticker)).get_json()

@app.route('/learn/')
def learn():
    email = request.args.get("email")

    options = ["S","A","M","B","E","G","V"]
    prefstr = ""

    
    for choice in options:
        if request.args.get(choice) != None:
            prefstr += choice
    print(email)     
    if len(prefstr) == 0 or email == "":
        f = open("home.html","r")
        lines = f.read()
        lines += "Error no prefences or email entered"
        return lines
    os.system("python3 Master.py "+str(prefstr)+" "+str(email)+ "&")
    
    f = open("log.txt","a+")
    f.write(str(email)+": "+str(prefstr)+"\n")
    f.close()

    return "Request Submitted"
if __name__=="__main__":
    app.run(host="0.0.0.0",port = 80)
