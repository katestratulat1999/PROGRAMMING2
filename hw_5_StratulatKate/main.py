import sqlite3
from flask import Flask
from flask import url_for, render_template, request, redirect
import os
import pymorphy2

#формируем базу данных
def write2db():
    conn = sqlite3.connect('mysearch.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS students(name text, major text, year integer)")
    with open("%s/metadata.csv" % (name), 'a+') as f:
        f.write(meta)
    conn.commit()
    conn.close()

#создаем таблицу в базе данных
def createTable():
    conn = sqlite3.connect('mysearch.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS articles(url text, title text, text text)")
    conn.commit()
    conn.close()

#добавляем строку с результатом
def insertRow(url, title, txt):
    conn = sqlite3.connect('mysearch.db')
    c = conn.cursor()
    c.execute("INSERT INTO articles VALUES (?,?,?)", (url, title, txt))
    conn.commit()
    conn.close()

#считываем данные из корпуса
def readData():
    for dir in os.listdir("./data/plain"):
        for d in os.listdir("./data/plain/%s" % dir):
            for f in os.listdir("./data/plain/%s/%s" % (dir, d)):
                with open("./data/plain/%s/%s/%s" % (dir, d, f), 'r', encoding = "utf-8") as f:
                    txt = ""
                    url = ""
                    for line in f:
                        if line.startswith("@url"):
                            url = line.strip()[5:]
                        elif line.startswith("@ti"):
                            title = line.strip()[4:]
                        elif not line.strip().startswith("@"):
                            txt += line.strip() + " "
                    insertRow(url, title, txt)

#выделяем жирным найденное слово
def markResults(l, txt):
    resAll = []
    for res in l:
        res = list(res)
        i = res[2].find(" " + txt)
        start = 0
        if i < 0:
            i = 0
        if i > 20:
            start = i - 20
        if i > 0:
            print(i)
            res[2] = "..." + res[2][start:i] + "<b>" + res[2][i:i+len(txt)+1] + "</b>" + res[2][i+len(txt)+1:i+125] + "..."
        else:
            res[2] = "..." + res[2][:125] + "..."
        resAll.append(res)
    return resAll

#поиск слова в таблице
def searchInDB(txt):
    searchTxt = ["% " + txt + " %", "% " + txt + ".%", "%" + txt.capitalize() + " %", "%" + txt.capitalize() + ".%"]
    txt = txt.strip()
    resAll = []
    conn = sqlite3.connect('mysearch.db')
    c = conn.cursor()
    for var in searchTxt:
        l = c.execute('SELECT * FROM articles WHERE text LIKE (?)', (var,))
        res = markResults(l.fetchall(), txt)
        resAll += res
    conn.close()
    return resAll

#получаем различные формы слова
def getMorph(txt):
    global m
    a = set()
    for p in m.parse(txt):
        a.add(p.normal_form)
        for i in p.lexeme:
            a.add(i.word)
    return list(a)

#закомментировать эти две строки после первого запуска
#createTable()
#readData()

m = pymorphy2.MorphAnalyzer()
app = Flask(__name__)

@app.route('/')
@app.route('/search')
def search():
    urls = []
    checkList = []
    if request.args:
        txt = request.args['txt']
        if txt.strip() == '':
            urls = [['', '', '<h4><b>По Вашему запросу ничего не найдено!</b></h4>']]
            return render_template('search.html', urls=urls)
        for i in getMorph(txt):
            url = searchInDB(i)
            url1 = []
            # удаляем повторы
            for item in url:
                if item[1] in checkList:
                    pass
                else:
                    checkList.append(item[1])
                    url1.append(item)
            urls += url1
    if not urls:
        urls = [['', '', '<h4><b>По Вашему запросу ничего не найдено!</b></h4>']]
    return render_template('search.html', urls=urls)

if __name__ == '__main__':
    app.run(debug = True)
