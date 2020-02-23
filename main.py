# server.py
from flask import Flask,render_template, request
from parse_vocab import parse_vocab
from get_urls import get_urls
from get_news import News

app = Flask(__name__)
news=News()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/parse_url/index.html')
def parse_url():
    return render_template("parse_url/index.html")

@app.route('/parse_url/input_text.html', methods=['POST']) #Methodを明示する必要あり
def input_text():
    if request.method == 'POST':
        url = request.form['name']
        link_url=get_urls(url,size=1)
        if len(link_url)==0:
            return render_template("parse_url/index.html")
        vocab=parse_vocab(link_url)
    return render_template('parse_url/input_text.html', vocab=vocab)

@app.route('/parse_url/input_domain.html', methods=['POST']) #Methodを明示する必要あり
def input_domain():
    if request.method == 'POST':
        url = request.form['name']
        link_url=get_urls(url,size=5)
        if len(link_url)==0:
            return render_template("parse_url/index.html")
        vocab=parse_vocab(link_url)
    return render_template('parse_url/input_domain.html', vocab=vocab)

@app.route('/news/index.html')
def news_index():
    global news
    news_data=news.get_words()
    return render_template('news/index.html', news_data=news_data)

#単語ごとに返す
@app.route('/news/<name>')
def news_name(name=None):
    news_list=news.get_news(name)
    return render_template('news/news_list.html', news_list=news_list)

app.debug = True
result = app.run(host='0.0.0.0', port=80)
