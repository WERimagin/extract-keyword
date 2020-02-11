import MeCab
import requests
from bs4 import BeautifulSoup
from collections import Counter
import nltk
from nltk.corpus import stopwords

def parse_vocab(urls):

    vocab=[]
    #nltk.download()
    stop_words = stopwords.words('english')
    for url in urls[0:5]:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")

        body=soup.body
        for script in body(["script", "style"]):
            script.decompose()
        body_text=body.get_text()
        body_split_text=[t.strip() for t in body_text.split("\n") if len(t.strip())>0]

        mecab = MeCab.Tagger("-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd")
        for t in body_split_text:
            tokens=mecab.parse(t).split()
            vocab+=[tokens[i] for i in range(0,len(tokens)-1,2) if tokens[i+1].split(",")[0]=="名詞"]

    #print(sorted(Counter(vocab).items(),key=lambda x:-x[1]))
    ranked_vocab=[(k,v) for k,v in sorted(Counter(vocab).items(),key=lambda x:-x[1]) if k.lower() not in stop_words][0:30]
    return ranked_vocab
