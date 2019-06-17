import urllib
from flask import Flask
from flask import request, render_template, url_for, redirect
from main import process
import re
from pymorphy2 import MorphAnalyzer
from gensim.models import word2vec
import gensim
import os
import random

def loadModel():
    global model
    f = 'ruscorpora_mystem_cbow_300_2_2015.bin.gz'
    if not os.path.isfile(f):
        urllib.request.urlretrieve("http://rusvectores.org/static/models/rusvectores2/%s"%f, f)
    model = gensim.models.KeyedVectors.load_word2vec_format(f, binary=True)

def loadTxt():
    global fText
    with open('vs.txt', 'r', encoding='utf-8') as f:
        fText = f.readlines()

def getStrings():
    global fText
    res = []
    l = len(fText)
    for i in range(10):
        r = (random.randint(0, (l//5)))*5
        res.append(fText[r:r+5])
    return res

app = Flask(__name__)
pm2 = MorphAnalyzer()
loadModel()
loadTxt()
started = False

@app.route('/')
def start():
    global isTrue, result, qNum, questionList, started, fText
    started = True
    questionList = getStrings()
    qNum = 0
    isTrue = "no"
    result = 0
    return render_template("start.html")

@app.route('/end')
def end():
    global result
    res = result
    return render_template("end.html", res = res)

@app.route('/questions')
def questions():
    global m, pm2, model, qNum, questionList, isTrue, result, started
    if not started:
        return redirect(url_for('start'))
    if request.args:
        if request.args['otvet'] == isTrue:
            result += 1
    if qNum < 10:
        qNum += 1
    else:
        return redirect(url_for('end'))
    p = random.randint(0,1)
    res = process(''.join(questionList[qNum-1]), model, pm2)
    if p == 0:
        isTrue = "no"
    else:
        res = ''.join(questionList[qNum-1])
        isTrue = "yes"
    temp = res.strip().split('\n')
    for i in range(len(temp)-2):
        temp[i] = temp[i][0].upper() + temp[i][1:]
    res = '<br>'.join(temp)
    return render_template("questions.html", res=res, qNum=qNum)

if __name__ == '__main__':
    import os
    app.debug = True
    #port = int(os.environ.get("PORT", 5000))
    #app.run(host='0.0.0.0', port=port)
    app.run()
