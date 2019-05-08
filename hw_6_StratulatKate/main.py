#acea1f9facea1f9facb576882dacb09ee6aaceaacea1f9ff42654477d8dbf19374cb73a

import urllib.request
import json
import re
from datetime import datetime
import sqlite3
import os
from readDB import*

#создаем таблицу в базе данных
def createTable():
  conn = sqlite3.connect('mydb.db')
  c = conn.cursor()
  c.execute("CREATE TABLE IF NOT EXISTS posts(postid text, text text, time int, postlen int)")
  conn.commit()
  c.execute("CREATE TABLE IF NOT EXISTS comments(postid text, comid text, text text, owner text, name text, time int, comlen int)")
  conn.commit()
  conn.close()

#добавляем строку с результатом
def insertInPosts(postid, text, time):
  conn = sqlite3.connect('mydb.db')
  c = conn.cursor()
  c.execute("INSERT INTO posts VALUES (?,?,?,?)", (postid, text, time, numOfWords(text)))
  conn.commit()
  conn.close()

#добавляем строку с результатом
def insertInComments(postid, comid, text, owner, name, time):
  conn = sqlite3.connect('mydb.db')
  c = conn.cursor()
  c.execute("INSERT INTO comments VALUES (?,?,?,?,?,?,?)", (postid, comid, text, owner, name, time, numOfWords(text)))
  conn.commit()
  conn.close()

def numOfWords(txt):
  return len(getWords(txt))

def getWords(txt):
  words = re.findall("\W*\w+", txt)
  return words

def removeStopWords(txt, sw):
  text = []
  for word in getWords(txt):
    if word.lower() not in sw:
      text.append(word.lower())
  return text
    
def sendRequest(req):
  response = urllib.request.urlopen(req)
  result = response.read().decode('utf-8')
  data = json.loads(result)
  return data

def txtToUTF(text):
  text = ''.join(char if ord(char) < 65536 else '' for char in text)
  return text

def writeToFile(path, name, txt):
  with open("%s/Post#%s.txt" % (path, name), 'a+', encoding='utf8') as f:
    f.write(txt + "\n")

def createFile(path, txt):
  if not os.path.exists("./%s" % path):
    os.makedirs("./%s" % path)
  with open("./%s/Post#%s.txt" % (path, txt), 'w+', encoding='utf8') as f:
    f.write("")

def readStopWords():
  l = []
  with open("stopwords.txt", 'r', encoding='utf8') as f:
    for line in f.readlines():
      l.append(line.strip())
  return l

def main():
  token = '8423c2448423c2448423c244d08441f2a1884238423c244dee1644d9e90529494134bf8'
  domain = 'tipkhimki'
  offset = [0, 100]
  numOfPosts = 51

  stopwords = readStopWords()

  #закомментировать эти две строки после первого запуска
  createTable()

  for off in offset:
    #получаем записи со стены сообщества
    req = urllib.request.Request('https://api.vk.com/method/wall.get?domain=%s&offset=%d&count=%d&v=5.92&access_token=%s'%(domain, off, numOfPosts, token))
    data = sendRequest(req)
    posts = data["response"]["items"]
    #владелец постов
    owner_id = posts[0]["owner_id"]
    #проход по каждому посту
    for post in posts:
      req = urllib.request.Request('https://api.vk.com/method/wall.getComments?owner_id=%d&post_id=%d&offset=%d&count=%d&v=5.92&access_token=%s'%(owner_id, post["id"], off, 101, token))
      data = sendRequest(req)
      comments = data["response"]["items"]
      if len(comments) == 0:
        continue
      text = txtToUTF(post["text"])   #получаем текст поста
      postTime = post["date"]
      postID = str(post["id"])
      insertInPosts(postID, text, postTime)
      createFile("plain", postID)
      writeToFile("plain", postID, text)
      writeToFile("plain", postID, "---------\n-----------")
      for comment in comments:
        try:
          text = txtToUTF(comment["text"])
        except:
          continue
        writeToFile("plain", postID, text)
        writeToFile("plain", postID, "---------")
        req = urllib.request.Request('https://api.vk.com/method/users.get?user_ids=%s&v=5.92&access_token=%s'%(comment["from_id"],token))
        data = sendRequest(req)
        try:
          name = data["response"][0]["first_name"]
          insertInComments(postID, comment["id"], text, comment["from_id"], name, datetime.fromtimestamp(comment["date"]).hour)
        except Exception:
          pass
      
  avglen()
  namelen()
  timelen()
  posthourlen()
  postmonthlen()    

if __name__ == '__main__':
    main()
