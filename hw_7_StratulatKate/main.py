from flask import Flask
from flask import request, render_template
from gr import mainFunc
import re

app = Flask(__name__)

@app.after_request
def add_header(response):
    response.cache_control.max_age = 0
    return response

@app.route('/')
def index():
    if request.args:
        res = re.findall("[а-яёА-яЁ]+", request.args['word'].strip())
        if res:
            try:
                txt = mainFunc(res)
                return render_template("index.html", title = "Ваш запрос: " +\
                                       request.args['word'].strip(), txt = txt, im = '<img src="/static/figure.png" alt="наш граф">')
            except Exception:
                return render_template("index.html", title = "Ваш запрос: " +\
                                       request.args['word'].strip(), txt = "К сожалению, не удалось построить граф.<br>Попробуйте другое сочетание.", im = '')
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=False)
    
