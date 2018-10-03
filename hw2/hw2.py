import json
import urllib.request
import sys
import re

class GitUser(): #класс для хранения информации пользователя
	def getFollowers(self): #получаем количество подписчиков пользователя
		url = 'https://api.github.com/users/%s/followers' % self.name
		response = urllib.request.urlopen(url)
		text = response.read().decode('utf-8')
		data = json.loads(text)
		return len(data)
		
	def getLangs(self): #получаем используемые пользователем языки
		userLang = []
		url = 'https://api.github.com/users/%s/repos' % self.name
		response = urllib.request.urlopen(url)
		text = response.read().decode('utf-8')
		data = json.loads(text)
		self.numOfReps = len(data)
		for i in data:
			lang = str(i["language"])
			if lang != "None":
				if lang not in userLang:
					userLang.append(lang)
		return userLang
	
	def __init__(self, username): #инициализаия класса
		self.name = username #имя пользователя
		self.numOfFollowers = self.getFollowers() #количество подписчиков пользователя
		self.numOfReps = 0 #количество репозиториев пользователя
		self.langsUsed = self.getLangs() #список используемых языков
		
def getData(user): #получаем данные профиля выбранного пользователя
	url = 'https://api.github.com/users/%s/repos' % user
	response = urllib.request.urlopen(url)
	text = response.read().decode('utf-8')
	data = json.loads(text)
	return data

def readFile(f): #читаем из файла список анализируемых пользователей
    rfile = open(f, 'r', encoding='utf-8')
    txt = rfile.read()
    rfile.close()
    return txt

def getUserInfo(data, user): #получаем список проектов, их описание и статистику по используемым языкам выбранного пользователя
  userLang = []
  repLang = {}
  for i in data:
	  name = str(i["name"])
	  desc = str(i["description"])
	  lang = str(i["language"])
	  print("%s: %s\n-----" % (name, desc))
	  if lang != "None":
		  if lang not in userLang:
			  userLang.append(lang)
		  repLang[name] = lang;
  print("Пользователь %s использует языки: %s." % (user, ', '.join(userLang)))
  for l in userLang:
	  listOfRep = []
	  for i, j in repLang.items():
		  if j == l:
			  listOfRep.append(i)
	  print("Язык %s используется в репозиториях: %s." % (l, ', '.join(listOfRep)))

def getMaxReps(gitUsers, userNames): #выясняем, у кого из пользователей списка больше репозиториев
  maxReps = 0
  maxName =""
  for i in range(len(gitUsers)):
	  if gitUsers[i].numOfReps > maxReps:
		  maxReps = gitUsers[i].numOfReps
		  maxName = userNames[i]
  print("Из пользователей %s больше всего репозиториев у %s." % (', '.join(userNames), maxName))

def getMaxFollowers(gitUsers, userNames): #выясняем, у кого из пользователей списка больше подписчиков
  maxFollowers = 0
  maxName = ""
  for i in range(len(gitUsers)):
	  if gitUsers[i].numOfFollowers > maxFollowers:
		  maxFollowers = gitUsers[i].numOfFollowers
		  maxName = userNames[i]		
  print("Больше всего подписчиков у %s: %d человек." % (maxName, maxFollowers))

def getPopularLang(gitUsers): #выясняем самый используемый язык среди пользователей списка
  langList = []
  langDict = {}
  popLangName = ""
  popLangNum = 0
  for i in range(len(gitUsers)):
	  for j in gitUsers[i].langsUsed:
		  if j not in langList:
			  langList.append(j)
			  langDict[j] = 0
		  else:
			  langDict[j] += 1
  for i, j in langDict.items():
	  if j > popLangNum:
		  popLangNum = j
		  popLangName = i
  print("Самый популярный язык средии пользователей: %s." % popLangName)

def main(): #основная функция
  gitUsers = [] #список объектов, хранящих данные пользователей из списка
  userNames = [] #список пользователей из файла
  user = "" #выбранный для анализа пользователь

  txt = readFile("1/1.txt") #открываем файл с именами пользователей
  userNames = re.findall(r"\S.*", txt) #получаем список пользователей
  print("Список пользователей: %s" % ', '.join(userNames))

  while True: #цикл по выбору пользователя для анализа
    user = input("Введите имя пользователя из списка или 0 для выхода >>")
    user = user.strip()
    if user != "0":
      if (user in userNames):
        try:
          data = getData(user)
        except Exception:
          print ("Ошибка соединения. Попробуйте ещё раз!")
          continue
        else:
          print("\nВы выбрали пользователя %s.\n" % user)
          print("Вот список его репозиториев:\n-----")
          break
      else:
        print("Неверный ввод. Попробуйте ещё раз!")
    else:
      sys.exit()

  getUserInfo(data, user) #получаем список проектов, их описание и статистику по используемым языкам выбранного пользователя

  print("-----\nПодождите, идёт сбор статистики...\n-----")
  # формируем список объектов с данными пользователей из списка
  for i in range(len(userNames)):
	  gitUsers.append(GitUser(userNames[i]))

  getMaxReps(gitUsers, userNames) #выясняем, у кого из пользователей списка больше репозиториев
  getMaxFollowers(gitUsers, userNames) #выясняем, у кого из пользователей списка больше подписчиков
  getPopularLang(gitUsers) #выясняем самый используемый язык среди пользователей списка

if __name__ == "__main__":
  main()
