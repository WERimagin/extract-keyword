import MeCab
import requests
from bs4 import BeautifulSoup
from collections import Counter

def parse_vocab(urls):

    vocab=[]
    stop_words = \
    ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
    for url in urls[0:5]:
        r = requests.get(url)
        r.encoding=r.apparent_encoding
        soup = BeautifulSoup(r.text, "html.parser")

        body=soup.body
        for script in body(["script", "style"]):
            script.decompose()
        body_text=body.get_text()
        body_split_text=[t.strip() for t in body_text.split("\n") if len(t.strip())>0]

        #エラーが出たため放置
        #mecab = MeCab.Tagger("-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd")
        mecab=MeCab.Tagger()
        for t in body_split_text:
            tokens=mecab.parse(t).split()
            vocab+=[tokens[i] for i in range(0,len(tokens)-1,2) if tokens[i+1].split(",")[0]=="名詞"]

    #print(sorted(Counter(vocab).items(),key=lambda x:-x[1]))
    ranked_vocab=[(k,v) for k,v in sorted(Counter(vocab).items(),key=lambda x:-x[1]) if k.lower() not in stop_words][0:30]
    return ranked_vocab
