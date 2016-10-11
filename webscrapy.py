#!/usr/bin/env python
# -*- coding: utf_8 -*-

import codecs
import sys
import unicodedata
import urllib2 as request
import time
from bs4 import BeautifulSoup
import mecab

sys.stdout = codecs.getwriter("utf-8")(sys.stdout)


# Main
def main():
    # URLの雛形
    url = "http://wiimk2.net/wiiu/title.php?title={number}"

    replace_dict = {
        # 漢字の表記ゆれ

    }

    # title={number}を500までループ
    for number in xrange(500):
        res = request.urlopen(url.format(number=number+1))  # URLオープン
        soup = BeautifulSoup(res.read())  # 読み込み

        title = soup.find('div', {'class': 'review'}).find('h2').string  # ゲームタイトルの取得
        reviews = soup.find('div', {'class': 'user_review_comments'}).findAll('p')  # レビュー文の取得

        # スクレイピングしたレビュー処理
        for review in reviews:
            text = review.text  # text形式(unicode)に変換
            # normResult = normalizeText(text) #不要な空白・改行等の処理

            # 形態素解析処理
            wakati_text = mecab.extract_key_word(title, text)
            # wordCount.fileOutput(strWakati)

            # リストの内容を標準出力
            for w in wakati_text:
                print w,  # mecab.multiple_replace(w, replace_dict),
            print ''

            time.sleep(2.0)  # 念のために2秒間のdelay


# 不要な空白を取り除き空行以外を返す
def non_empty_lines(text):
    for line in text.splitlines():
        line = u' '.join(line.split())
        if line:
            yield line


# 不要な空白・改行を取り除く
def normalize_text(text):
    text = unicodedata.normalize('NFKC', text)
    return u'\n'.join(non_empty_lines(text))


if __name__ == '__main__':
    main()
