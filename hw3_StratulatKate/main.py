from mypage import createHtml
from crawler import crawsite
from mystem import *
import os

def main():
    address = "http://gazeta-rvs.ru/news/best"
    numOfTags = 100
    for page in crawsite(address, numOfTags):
        createHtml(page, "./RVS")

    for dir1 in os.listdir("./RVS/plain"):
        for dir2 in os.listdir("./RVS/plain/%s" % dir1):
            for filename in os.listdir("./RVS/plain/%s/%s" % (dir1, dir2)):
                getMystemTxt("%s/%s" % (dir1, dir2), filename)

if __name__ == "__main__":
    main()
