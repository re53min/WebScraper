#!/usr/bin/env python
# -*- coding: utf_8 -*-

import codecs
import MeCab
import re
import sys
from collections import Counter

__author__ = 'b1012059'

sys.stdout = codecs.getwriter("utf-8")(sys.stdout)


# 分かち書き処理
def wakati(text):
    # MeCabの設定
    tagger = MeCab.Tagger('-Owakati')
    encoded_text = text.encode('utf-8', 'ignore')
    result = tagger.parse(encoded_text).decode('utf-8')

    return result


# textを形態素解析して名詞・形容詞をリストに返す
def extract_key_word(sake_name, sake_text):
    keywords = []
    replace_text = sake_text.replace(u'。', u'\n')
    # MeCabの設定
    tagger = MeCab.Tagger('-Ochasen')
    encode_text = replace_text.encode('utf-8', 'replace')
    node = tagger.parseToNode(encode_text)

    # 名詞と形容詞抽出
    while node:
        pos = node.feature.split(",")[0]
        if pos == '名詞':
            keywords.append(sake_name)
            keywords.append(node.surface.decode('utf-8', 'replace'))
        elif pos == '形容詞':
            keywords.append(sake_name)
            keywords.append(node.feature.split(",")[6].decode('utf-8', 'replace'))
        node = node.next

    return keywords


# 辞書を使って文字列を置換
def multiple_replace(text, adict):
    """ 一度に複数のパターンを置換する関数
    - text中からディクショナリのキーに合致する文字列を探し、対応の値で置換して返す
    - キーでは、正規表現を置換前文字列とできる
    """

    rx = re.compile('|'.join(adict))

    def dedictkey(text):
        """ マッチした文字列の元であるkeyを返す
        """
        for key in adict.keys():
            if re.search(key, text):
                return key

    def one_xlat(match):
        return adict[dedictkey(match.group(0))]

    return rx.sub(one_xlat, text)


if __name__ == "__main__":
    # keywords = extractKeyWord(u"薫酒 華やかな香りと爽やかな味わいのタイプ 吟醸、大吟醸が代表的。生酒、本醸造酒にも該当するものがある。 色調は淡く、果実や花のような上立ち香が高く、軽快で爽やかな味を有する。 香気成分を多く含み、熟成成分やアミノ酸は少ない。薫酒 華やかで透明感のある果実や花の香りが高く、爽やかさを感じさせる香草や柑橘類の香りも高い。反面、樹木やスパイスを思わせる香り、原料由来の穀物のフレーバーや、熟成香は極めて微量である。 薫酒 甘さととろみは中程度で、爽快な味わいをもたらす酸とのバランスがとれている。一方、苦味や旨味が少なく、明るく爽やかな味わいとなっている。口の中で華やかな香りは高いが、後の余韻は短い。"
    #                          u"爽酒 清楚な香りと軽快な味わいのタイプ 生酒が代表的。本醸造酒、純米酒にも該当するものがある。 色調は淡く、上立ち香は抑えられているが、新鮮で軽快な含み香と、なめらかでみずみずしい味を有する。 香気成分は中程度であるが、リンゴ酸などの有機酸を多く含み、アミノ酸、熟成成分は微少である。爽酒 全体が穏やかで控えめで、わずかな果実香と新鮮な爽やかさを感じさせる。反面、山菜などの苦味を思わせる香り、ふくよかさを感じさせる香りは少ない。 爽酒 清涼感をもった味わいで、軽くさらっとしている。ほのかな甘味と、フレッシュ感のある酸味、心地良い苦味が微量にあって、お酒の爽やかさをさらに引き立てる。穀類を思わせる味わいや熟成感はほとんどみることができない。 "
    #                          u"醇酒 ふくよかな香りとコクのある味わいのタイプ 純米酒が代表的。本醸造酒にも該当するものがある。色調はやや濃く、落ち着いた香りと、 やや重厚なほど良い苦味と旨味を有する。乳酸等の有機酸を多く含み、熟成成分のやや高いものがある。醇酒 フルーツや花、ハーブを思わせる香りは非常に少なく、樹木や石の香りがあり、ふくよかさを感じさせるまろやかで複雑な旨味を感じさせる香りが強く、濃厚で柔和な香りの特性を示している。 醇酒 甘味、酸味は、心地良い苦味とふくらみのある旨味と共に調和し、とろりとして充実したふくよかな味わいとなっている。味わいの残存時間が長く、力強さが感じられる。"
    #                          u"熟酒 扱いで 練れた香りと芳醇な味わいのタイプ 古酒が代表的。一部純米酒にも該当するものがある。色調は濃く、ナッツ類のような香気をもち、重厚でほどよい苦味と後味の良さを有する。熟成成分、有機酸、アミノ酸を多く含む。 熟酒 力強く複雑で個性的な香りを持つ。干した果物や干し草の香り、スパイスや樹木、香木を思わせる香りが非常に豊かである。また、きのこ類やナッツの香りが濃厚に熟した旨味を力強く暗示させる。 熟酒 甘味はとろりとしていて、よく練れた酸味が加わりバランスをとっている。強いスパイスや香ばしい味わいが、熟した複雑な旨味と共に口中に存在感を表す。重厚な後味と長い余韻がある。 "
    #                          u"薫酒 フルーティーフレーバーが海外でも大人気  果実や花の様な華やかな香りが高く、軽快で爽やかな味わいが特徴です。甘い風味を感じさせるものから辛口のものまで、様々なタイプが存在します。薫酒 清涼感のある香味が特徴的で、冷やすことによって爽快さが映えます。しかしあまり冷やしすぎると持ち味である華やかな香りが感じにくくなったり、酸味や苦味などの刺激要素が突出したりする場合があるのでよく注意して下さい。 香りが控えめで旨味成分が割としっかりしたタイプなら、ぬる燗も可能です。"
    #                          u"爽酒 淡麗辛口テイストで誰にでも好かれる万能選手 香りは全体的に控えめであるが、新鮮で清涼感のある含み香を持ち、なめらかでみずみずしい味わいが特徴です。爽酒 爽快な酒質と爽涼な飲み口、フレッシュな味わいが特徴的なこのタイプはしっかりと冷やす事で特性が活きます。また、味わいの成分中に刺激的な要素が少ないため、冷やしすぎてもこれらの要素が突出することがありません。"
    #                          u"醇酒 まさに原点。伝統的かつ王道をいく日本酒 原料の米そのものを想わせるようなふくよかな香りと、充実した旨味を感じさせるコクのある味わいが特徴です。醇酒 飲用温度帯が最も広く、品温の違いによってさまざまな変化を見せるタイプです。コクと旨味成分をしっかり持っているので、この要素を活かす事がポイント。旨味のふくらみが映えるやや高めの温度設定が好ましいです。"
    #                          u"熟酒 黄金色に輝く日本酒。本当の酒通が認める貴重品 ドライフルーツやスパイスなどの複雑性のある練れた熟成香を持ち、とろりとした甘味や深い酸味、ボリューム感のある旨味が合わさった力強い味わいが特徴です。熟酒 軽快なものから重厚なものまで様々であり、温度設定はそれぞれ異なりますが、重厚な旨味成分を持つものほど高めの温度設定と考えればよいでしょう。また、 大きく嗜好が分かれる傾向が見られるので、温度設定は好まれる方には高め、そうでない方はやや低めとし、強い香りと旨味を抑えるとより飲みやすくなりま す。但し、燗にする場合、温度が高すぎるとバランスが崩れる場合があるので、少し低めを心がけて下さい。")

    text = u"フルーティさが強いとそれが口に残ることも多いですが、獺祭は後味すっきり。フルーティでまろやかだ"

    adict = {
        u'(フルーティ|まろやか|コク)': u'甘い',
    }

    keywords = extract_key_word(u'獺祭', text)
    result = []
    for w in keywords:
        print w,
        result.append(multiple_replace(w, adict))
    print ''

    for w in result:
        print w,
    print ''

    # --------------出現回数--------------
    f = codecs.open('count.txt', 'w', "utf-8")
    counter = Counter(keywords)
    for word, cnt in counter.most_common():
        listData = [word, unicode(cnt)]
        # print word, cnt
        f.write(" ".join(listData) + "\r\n")

    f.close()
