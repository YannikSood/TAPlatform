from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import praw
from textblob import TextBlob
from praw.models import MoreComments
import datetime
import sys
class comment_write2():

    def __init__(self,sub,yesterday): 
        r = praw.Reddit(client_id='rox3ZpzG7EVrbA', \
                     client_secret='VW_ZCXp3zqnMQzd6i5FpyStr_-M', \
                     user_agent='wsb')
        subreddit = r.subreddit(sub)
        i=0
        self.dayssince = 7
        if yesterday:
            to = datetime.datetime.today()
            self.dayssince = 1
            writefile = "old/C_"+str(to.month)+"_"+str(to.day)+"_"+str(to.year)+".txt"
        else:
            writefile = "com.txt"
        

        f = open(writefile,"w+")
        for submission in subreddit.new(limit=1000):
            curtime = datetime.datetime.now()
            if self.get_date(submission) + datetime.timedelta(days = self.dayssince) <= curtime:
                break
            title = str(submission.author) + ": " + str(submission.title)
            title = title.replace("\n","")
            i+=1
            if i%50 == 0:
                print("~",end = "",flush = True)
            f.write(title+"\n")
            for top_level_comment in submission.comments:
                if isinstance(top_level_comment, MoreComments):
                    continue
                title = "   "+str(top_level_comment.author) + ": " + str(top_level_comment.body)
                title = title.replace("\n","")
                f.write(title+"\n")
        f.close()   
        print("\n")
    def get_date(self,submission):
	    time = submission.created
	    return datetime.datetime.fromtimestamp(time)
class comment_write():

    def __init__(self,sub): 
        r = praw.Reddit(client_id='rox3ZpzG7EVrbA', \
                     client_secret='VW_ZCXp3zqnMQzd6i5FpyStr_-M', \
                     user_agent='wsb')
        subreddit = r.subreddit(sub)
        i=0
        f = open("com.txt","w+")
        for submission in subreddit.new(limit=1000):
            title = submission.title
            if "Daily Discussion Thread" in str(title) or "What Are Your Moves Tomorrow" in str(title):
                for top_level_comment in submission.comments:
                    if isinstance(top_level_comment, MoreComments):
                        continue
                    title = top_level_comment.body
                    title = title.replace("\n","")
                    f.write(title+"\n")
            title = title.replace("\n","")
            f.write(title+"\n")
        f.close()      

def main():
    comment_write('wallstreetbets')

if __name__ == "__main__":
    main()
    
