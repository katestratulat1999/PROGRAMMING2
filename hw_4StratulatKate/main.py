from flask import Flask
from flask import url_for, render_template, request, redirect
import os.path
import json
import pygal

#создаём CSV с заголовками
def createCSV():
    if not os.path.exists("table.csv"):
        with open("table.csv", "w", encoding = 'utf-8') as f:
            header = "%s\t%s\t%s\t%s\t%s\t%s\n"%(
                    'name','age','education','hometown','sex','choise')
            f.write(header)

#записываем данные в CSV
def write2CSV(name, age, edu, hometown, sex, choise):
    with open("table.csv", "a+", encoding = 'utf-8') as f:
        field = "%s\t%s\t%s\t%s\t%s\t%s\n"%(
                name, age, edu, hometown, sex, choise)
        f.write(field)

#конвертируем CSV в список
def csv2list():
    with open("table.csv", "r", encoding = "utf-8") as f:
        data = []
        headers = f.readline().strip().split('\t')
        for line in f:
            l = line.strip().split('\t')
            d = {}
            for i in range(len(headers)):
                d[headers[i]] = l[i]
            data.append(d)
    return data


#конвертируем CSV в JSON
def csv2json():
    s = csv2list()
    return json.dumps(s)

#собираем данные из результатов опроса
def getStats(col, stats):
    items = set()
    res = {}
    for row in stats:
        items.add(row[col])
    for item in items:
        choise = [0, 0]
        for row in stats:
            if row[col] == item:
                if row['choise'] == 'пЕрчит':
                    choise[0] += 1
                else:
                    choise[1] += 1
        res[item] = choise
    return res

#выводим статистику в графиках
def drawStats(col, stats):
    title = {'sex':'Пол', 'education':'Образование', 'age':'Возраст', 'hometown':'Родной город'}
    res = getStats(col, stats)
    chart = pygal.HorizontalBar(y_label_rotation=-25)
    chart.title = 'Выборка результатов опроса по категории: ' + title[col]
    chart.x_labels = 'перчИт', 'пЕрчит'
    for key, value in res.items():
        chart.add(key, value)
    chart.render_to_file('./static/%s.svg'%col)

#запускаем сервер
app = Flask(__name__)
createCSV()

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/stats')
def stats():
    if os.path.exists("table.csv"):
        urls = {
            'поиск по результатам': url_for('search'),
            'сохранить результаты опросов': url_for('jsonpage'),
            'пройти опрос': url_for('form')}
        stats = csv2list()
        drawStats('sex', stats)
        drawStats('hometown', stats)
        drawStats('education', stats)
        drawStats('age', stats)
        return render_template('stats.html', urls=urls)
    else:
        return render_template('error.html')

@app.route('/search')
def search():
    urls = {
            'страница статистики': url_for('stats'),
            'сохранить результаты опросов': url_for('jsonpage'),
            'пройти опрос': url_for('form')}
    if request.args:
        urls = {
            'назад к поиску': url_for('search'),
            'страница статистики': url_for('stats'),
            'сохранить результаты опросов': url_for('jsonpage'),
            'пройти опрос': url_for('form')}
        hometown = request.args['hometown'].capitalize()
        sex = request.args['sex']
        rev = csv2list()
        s = "<thead><tr><th>%s</th><th>%s</th><th>%s</th><th>%s</th><th>%s</th><th>%s</th></tr></thead><tbody>"%(
                'Имя','Возраст','Образование','Родной город','Пол','Выбор')
        for item in rev:
            if item['hometown'] == hometown:
                if item['sex'] == sex:
                    s += '<tr>'
                    for key, value in item.items():
                        s = s + '<td>' + value + '</td>'
                    s += '</tr></tbody>'
        return render_template('results.html', table=s, urls=urls)
    rev = csv2list()
    towns = set()
    for item in rev:
        towns.add(item['hometown'])
    return render_template('search.html', urls=urls, towns=towns)

@app.route('/jsonpage')
def jsonpage():
    urls = {
            'страница статистики': url_for('stats'),
            'поиск по результатам': url_for('search'),
            'пройти опрос': url_for('form')}
    with open("data.json", "w") as f:
        f.write(csv2json())
        path = os.getcwd() + "data.json"
    return render_template('jsonpage.html', path=path, urls=urls)

@app.route('/thanks')
def thanks():
    urls = {
            'страница статистики': url_for('stats'),
            'поиск по результатам': url_for('search'),
            'сохранить результаты опросов': url_for('jsonpage'),
            'пройти опрос': url_for('form')}
    if request.args:
        name = request.args['name'].capitalize()
        age = request.args['age']
        edu = request.args['edu'].lower()
        hometown = request.args['hometown'].capitalize()
        sex = request.args['sex']
        choise = request.args['choise']
        write2CSV(name,age,edu,hometown,sex,choise)
        return render_template('thanks.html', name=name, urls=urls)
    return 0

if __name__ == '__main__':
    app.run(debug = True)
