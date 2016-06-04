# coding: utf-8

import sys
import codecs
import csv
from collections import Counter

sys.stdout = codecs.getwriter("utf-8")(sys.stdout)

def fileInput(text):
    f = codecs.getreader('utf-8-sig')(open(text+'.txt','r'))
    keywords = []
    # 1行毎にファイル終端まで全て読む(改行文字も含まれる)
    lines = f.read()
    f.close()

    itemList = lines.split(" ")
    keywords.append([item for item in itemList]),

    return keywords

def fileOutput(fileName, keywords):
    f = codecs.getreader('utf-8-sig')(open(fileName + 'Count.txt', 'w',))
    #f = codecs.open(fileName + 'Count', 'w', "utf-8")

    for w in keywords:
        counter = Counter(w)

    for word, cnt in counter.most_common():
        listData = []
        listData.append(word)
        listData.append(unicode(cnt))
        #print word, cnt
        f.write(" ".join(listData)+"\r\n")

    f.close()

def csvOutput(keywords):
    f = codecs.getwriter('cp932')(open('data.csv', 'w')) #ファイルが無ければ作る、の'a'を指定します
    csvWriter = csv.writer(f, delimiter=',')
    for w in keywords:
        counter = Counter(w)

    for word, cnt in counter.most_common():
        listData = []
        sWord = word.encode('sjis')
        #print type(word)
        listData.append([sWord, cnt])

        csvWriter.writerow(listData)

    f.close()

if __name__ == '__main__':
    fileName = 'corpusB'
    fileOutput(fileName, fileInput(fileName))
