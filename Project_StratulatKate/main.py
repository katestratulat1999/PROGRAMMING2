from pymorphy2 import MorphAnalyzer
import gensim
import re
import os
from gensim.models import word2vec

def changeText(txt):
    ft = ''
    for a in txt.split('\n'):
        ft += chText(a) + '\n'
    return ft

def chText(txt):
    global pos
    finalTxt = ''
    ana = re.findall('\w+', txt)
    for word in ana:
        if True:
            f = pm2.parse(word)[0]
            if True:
                w = findSin(word, f.normal_form, pos[f.tag.POS])
                if w != '':
                    finalTxt += w + ' '
                else:
                    finalTxt += word + ' '
            else:
                finalTxt += word + ' '
        else:
            finalTxt += word + ' '
    return finalTxt

def findSin(word, lex, tag):
    props = saveProps(word, lex)
    sins = getSins(lex + "_" + tag)
    res = applyProps(sins, props)
    if res:
        return res
    else:
        return word

def saveProps(word, lex):
    global pm2
    word = word.replace('ё', 'е')
    w = pm2.parse(word)[0]
    return w.tag

def applyProps(sins, props):
    global pm2
    for sin in sins:
        word = sin[0].split('_')[0]
        p = pm2.parse(word)[0]
        try:
            if p.tag.gender == props.gender:
                res = p.inflect(fixTags(props))
                return res.word 
        except Exception:
            continue  
    return ''

def getSins(word):
    res = searchInModel(word)
    return res

def searchInModel(word):
    global model
    neib = []
    if word in model:
        for i in model.most_similar(positive=[word], topn=10):
            if i[1] >= 0.5:
                neib.append(i)
    else:
        pass
    return neib

def fixTags(tags):
    tags = str(tags)
    tags = re.sub(',[AGQSPMa-z-]+? ', ',', tags)
    tags = tags.replace("impf,", "")
    tags = re.sub('([A-Z]) (plur|femn|masc|neut|inan)', '\\1,\\2', tags)
    tags = tags.replace("Impe neut", "")
    tags = tags.split(',')
    cleanTags = []
    for t in tags:
        if t:
            if ' ' in t:
                t = t.split(' ')[1]
            cleanTags.append(t)
    return frozenset(cleanTags)

def process(txt, mod, mypy):
    global pm2, pos, model
    model = mod
    pm2 = mypy
    pos = {'NOUN':'S','ADJF':'A','ADJS':'A','COMP':'ADV','VERB':'V',\
           'INFN':'V','PRTF':'V','PRTS':'V','GRND':'V','NUMR':'NUM',\
           'ADVB':'ADV','NPRO':'SPRO','PRED':'ADVPRO','PREP':'PR',\
           'CONJ':'CONJ','PRCL':'PART','INTJ':'INTJ'}
    finalTxt = changeText(txt)
    return finalTxt

