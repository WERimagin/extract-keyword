import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from collections import Counter
import datetime
from datetime import date,timedelta
import MeCab

class News():
    def __init__(self):
        self.collected_news={}
    def get_news(self):

        #現在時刻を取得、日本時刻に合わせる
        now_time=datetime.datetime.now(tz=datetime.timezone.utc)+timedelta(hours=9)
        stopwords=["さん"]
        news_count=6
        news=[]

        for i in range(news_count):
            date=now_time+timedelta(days=-1*(i+1))
            today="{:04}{:02}{:02}".format(date.year,date.month,date.day)

            #todayがcollected_newsにない場合は取得。
            if today not in self.collected_news:
                title_list=[]
                for page in range(1,50):
                    url="https://news.yahoo.co.jp/topics/top-picks?date={}&page={}".format(today,page)
                    r=requests.get(url)
                    soup=BeautifulSoup(r.text)
                    title_list_page=[s.get_text() for s in soup.find_all("div",class_="newsFeed_item_title")]
                    if len(title_list_page)==0:
                        break
                    else:
                        title_list+=title_list_page


                mecab=MeCab.Tagger()
                vocab=[]
                for t in title_list:
                    tokens=mecab.parse(t).split()
                    vocab+=[tokens[i] for i in range(0,len(tokens)-1,2) if tokens[i+1].split(",")[0]=="名詞"]

                ranked_vocab= \
                    [(k,v) for k,v in sorted(Counter(vocab).items(),key=lambda x:-x[1]) \
                    if len(k)>=2 and k not in stopwords][0:10]
                self.collected_news[today]=ranked_vocab
            news.append((today,self.collected_news[today]))
        return news
