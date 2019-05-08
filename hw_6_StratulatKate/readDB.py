import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime

def avglen():
  x = []
  y = []
  conn = sqlite3.connect('mydb.db')
  c = conn.cursor()
  c.execute("SELECT postid, ROUND(AVG(comlen)) avl FROM comments GROUP BY postid ORDER BY avl ASC")
  l = c.fetchall()
  c.execute("SELECT postid, postlen FROM posts")
  for i in c.fetchall():
    for j in l:
      if i[0] == j[0]:
        y.append(i[1])
        x.append(j[1])
  conn.commit()
  conn.close()
  plt.scatter(x, y)
  plt.title("Зависимость средней длины комментариев от длины поста")
  plt.xlabel("Средняя длина комментариев")
  plt.ylabel("Средняя длина поста")
  plt.show()

def namelen():
  x = []
  y = []
  conn = sqlite3.connect('mydb.db')
  c = conn.cursor()
  c.execute("SELECT name, ROUND(AVG(comlen)) as len FROM comments GROUP BY name ORDER BY len DESC LIMIT 10")
  for i in c.fetchall():
    x.append(i[0])
    y.append(i[1])
  conn.commit()
  conn.close()
  plt.bar(x, y, color='y')
  plt.title("Зависимость средней длины комментариев от имени комментатора")
  plt.xlabel("Имя комментатора")
  plt.ylabel("Средняя длина комментариев")
  plt.show()

def timelen():
  x = []
  y = []
  conn = sqlite3.connect('mydb.db')
  c = conn.cursor()
  c.execute("SELECT time, ROUND(AVG(comlen)) as len FROM comments GROUP BY time ORDER BY time ASC")
  for i in c.fetchall():
    x.append(i[0])
    y.append(i[1])
  conn.commit()
  conn.close()
  plt.bar(x, y, color='g')
  plt.title("Зависимость средней длины комментариев от времени суток")
  plt.xlabel("Время суток(часы)")
  plt.ylabel("Средняя длина комментариев")
  plt.show()

def posthourlen():
  x = []
  y = []
  conn = sqlite3.connect('mydb.db')
  c = conn.cursor()
  c.execute("SELECT time, postlen FROM posts")
  for i in c.fetchall():
    x.append(datetime.fromtimestamp(int(i[0])).hour)
    y.append(i[1])
  conn.commit()
  conn.close()
  plt.bar(x, y, color='r')
  plt.title("Зависимость длины постов от времени суток")
  plt.xlabel("Время суток(часы)")
  plt.ylabel("Длина постов")
  plt.show()

def postmonthlen():
  x = []
  y = []
  conn = sqlite3.connect('mydb.db')
  c = conn.cursor()
  c.execute("SELECT time, postlen FROM posts")
  for i in c.fetchall():
    x.append(datetime.fromtimestamp(int(i[0])).day)
    y.append(i[1])
  conn.commit()
  conn.close()
  plt.bar(x, y, color='b')
  plt.title("Зависимость длины постов от дня месяца")
  plt.xlabel("День Месяца")
  plt.ylabel("Длина постов")
  plt.show()
