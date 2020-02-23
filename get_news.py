import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from collections import Counter
import datetime
from datetime import date,timedelta
import MeCab
from collections import defaultdict



class News():
    def __init__(self):
        self.collected_news={}
        self.title_list=defaultdict(dict)

    def get_words(self):
        #現在時刻を取得、日本時刻に合わせる
        now_time=datetime.datetime.now(tz=datetime.timezone.utc)+timedelta(hours=9)
        stopwords=["さん"]
        news_count=6
        news=[]

        #日付ごとにニュースを取得し、newsにappend
        for i in range(news_count):
            date=now_time+timedelta(days=-1*(i+1))
            today="{:04}{:02}{:02}".format(date.year,date.month,date.day)

            #todayがcollected_newsにない場合は取得。
            if today not in self.collected_news:
                title_list=[]
                link_list=[]
                for page in range(1,50):
                    url="https://news.yahoo.co.jp/topics/top-picks?date={}&page={}".format(today,page)
                    r=requests.get(url)
                    soup=BeautifulSoup(r.text)
                    title_list_page=[s.get_text() for s in soup.find_all("div",class_="newsFeed_item_title")]
                    link_list_page=[s.get("href") for s in soup.find_all("a",class_="newsFeed_item_link")]
                    if len(title_list_page)==0:
                        break
                    else:
                        title_list+=title_list_page
                        link_list+=link_list_page


                mecab=MeCab.Tagger()
                vocab=[]
                for title,link in zip(title_list,link_list):
                    tokens=mecab.parse(title).split()
                    get_vocab=[tokens[i] for i in range(0,len(tokens)-1,2) if tokens[i+1].split(",")[0]=="名詞"]
                    vocab+=get_vocab
                    for word in get_vocab:
                        if word not in self.title_list:
                            self.title_list[word]=defaultdict(list)
                        #if today not in self.title_list[word]:
                        #    self.title_list[word][today]=[{"title":title,"link":link}]
                        #else:
                        self.title_list[word][today].append({"title":title,"link":link})

                ranked_vocab= \
                    [k for k,v in sorted(Counter(vocab).items(),key=lambda x:-x[1]) \
                    if len(k)>=2 and k not in stopwords][0:10]
                self.collected_news[today]=ranked_vocab
            news.append((today,self.collected_news[today]))

        news=self.reshape_news(news)
        return news

    def get_news(self,word):
        #news_list=sorted(self.title_list[word].items(),key=lambda x: -int(x[0]))

        #日付ごとにtitle_list
        #title_list=[{title,list}]

        return \
            [{"date":self.string2date(date),"title_list":title_list} for date,title_list in self.title_list[word].items()]

    def reshape_news(self,news):
        word_size=len(news[0][1])
        news_count=len(news)
        date=[self.string2date(d[0]) for d in news]
        words=[[news[j][1][i] for j in range(news_count)] for i in range(word_size)]
        news={"date":date,"words":words}
        return news

    def string2date(self,string):
        return "{}年{}月{}日".format(string[0:4],string[4:6],string[6:8])
