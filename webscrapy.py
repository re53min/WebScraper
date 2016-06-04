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
    replace_dict = {
        # 漢字の表記ゆれ
        u'(旨い|美味い|ウマい)': u'うまい',
        u'美味しい': u'おいしい',
        u'(万寿|万壽)': u'萬寿',
        u'端麗': u'淡麗',
        u'(cp|CP|Cp|cP)': u'コストパフォーマンス',
        u'百壽': u'百寿',
        u'千壽': u'千寿',
        u'(うま味|うまみ|旨み)': u'旨味',
        u'さわやか': u'爽やか',
        u'吟': u'純米吟醸',


        # 味わい表現
        u'(フルーティー|フルーティ|甘い|甘み|優しい|やさしい|柔らかい|甘口)': u'甘味',
        u'(酸っぱい|酸|辛い|辛口|ドライ|キレ|からい|きれ|)': u'酸味',
        u'(まろやか|コク|穏やか|後味|濃い|旨|深い|滑らか)': u'旨味',
        u'(苦い|苦味|雑|にがみ|えぐみ|邪魔|ひどい|くどい)': u'雑味',
    }

    # URLリストから1行ずつ読み、対象のwebページを取得し、任意のタグのテキストをスクレイピング
    for target_url in open('url.txt').readlines():
        target_url = target_url.split(",")
        sake_name = target_url[0].decode('utf-8')
        res = request.urlopen(target_url[1])  # URLオープン
        soup = BeautifulSoup(res.read())  # 読み込み

        # レビュー者を削除
        for tmp in soup.findAll("div", {"class": "voicemember"}):
            tmp.extract()
        html_div = soup.find('div', {'id': 'maincontent'})  # メインコンテンツの取得
        texts = html_div.findAll('dd')  # メインコンテンツ内のレビューのみをスクレイピング

        # text = text.find_next_siblings('dd')

        # スクレイピングしたレビュー処理
        for text in texts:
            text = text.text  # text形式(unicode)に変換
            # normResult = normalizeText(text) #不要な空白・改行等の処理
            # レビュー処理
            # strResult = wakatiText(text)
            # print sakeName
            # print text

            str_wakati = mecab.extract_key_word(sake_name, text)
            #wordCount.fileOutput(strWakati)

            # リストの内容を標準出力
            # result = []
            for w in str_wakati:
                # print w,
                # result.append(multiple_replace(w, adict)),
                print mecab.multiple_replace(w, replace_dict),
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
