# ВИСЕЛИЦА
import os
import re
import random

# функция считывает файл
def readFile(f):
    rfile = open(f, 'r', encoding='utf-8')
    txt = rfile.read()
    rfile.close()
    return txt

# функция просит ввести букву, меняет _ на угаданную, в противном случае - уменьшает кол-во попыток на 1
def guessWord():
    global numOfTries, temp, numOfMisses, win
    letter = input("Введите букву: >> ")
    if letter not in letters:
        if letter in word:
            print("Угадал!")
            for i in range(numOfLetters):
                if word[i] == letter and temp[i] == "_":
                    temp = temp[:i] + letter + temp[i+1:]
            print(temp)
            if "_" not in temp:
                win = True
                return
        else:
            print("Неверная буква!")
            for i in range(numOfMisses):
                print(hangMan[i])
            numOfMisses += 1
    else:
        print("Буква уже была!")
        for i in range(numOfMisses):
            print(hangMan[i])
        numOfMisses += 1
    letters.append(letter)
    numOfTries -= 1
    if (numOfTries > 4):
        print("Осталось " + str(numOfTries) + " попыток.")
    elif (numOfTries > 1):
        print("Осталось " + str(numOfTries) + " попытки.")
    elif (numOfTries == 1):
        print("Осталась 1 попытка.")

# детали человечка
letters = []
temp = ""
numOfTries = 10
numOfMisses = 0
hangMan = ["-----","|   |","|   O","|   |","|   \\\\","|   |","|   |","|  / \\","|","|"]
win = False

# выбор темы
subjects = ("Домашние животные", "Виды спорта", "Блюда итальянской кухни")
sub = input(
    "Выберите тему (введите соответствующую теме цифру):\n1 - Домашние животные,\n2 - Виды спорта,\n3 - Блюда итальянской кухни\n>>")
while (int(sub) < 1 or int(sub) > 3):
    sub = input("Неверный ввод. Повторите выбор: >> ")
print("Вы выбрали тему: " + subjects[int(sub)-1] + ".")

# эта функция рандомно выбирает слово из списка
txt = readFile("1/" + subjects[int(sub)-1] +".txt")
result = re.findall(r"\w*\n", txt)
word = result[random.randint(0, 9)].strip()

numOfLetters = len(word)
print("У вас есть " + str(numOfTries) + " попыток, чтобы угадать слово из " + str(numOfLetters) + " букв.")
print("_" * numOfLetters)

temp = "_" * numOfLetters

while True:
    guessWord()
    if win:
        print("Ты выиграл!")
        break
    if numOfTries == 0:
        print("Ты проиграл!")
        break
