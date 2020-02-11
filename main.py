# server.py
from flask import Flask,render_template, request
from parse_vocab import parse_vocab
from get_urls import get_urls

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/input_text', methods=['POST']) #Methodを明示する必要あり
def input_text():
    if request.method == 'POST':
        url = request.form['name']
        vocab=parse_vocab([url])
    return render_template('input_text.html', vocab=vocab)

@app.route('/input_domain', methods=['POST']) #Methodを明示する必要あり
def input_domain():
    if request.method == 'POST':
        url = request.form['name']
        link_url=get_urls(url)
        vocab=parse_vocab(link_url)
    return render_template('input_domain.html', vocab=vocab)

app.debug = True
app.run(host='0.0.0.0', port=80)
