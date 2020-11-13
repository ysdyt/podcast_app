import MeCab
import re
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pickle
import sys
import os

args = sys.argv
file_name = args[1]
file_b_name = os.path.splitext(args[1])[0]

with open('./transcribed_file/{}'.format(file_name), 'rb') as f:
    transcribed_result = pickle.load(f)

# mecab
mecab = MeCab.Tagger ('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
node = mecab.parseToNode(transcribed_result['results']['transcripts'][0]['transcript'].replace(' ', ''))
target_part = ('名詞')
word = []

while node:
    if node.feature.split(",")[0] in target_part:
        word.append(node.surface)
    node = node.next

word_freq_dict = Counter(word)
stop_words = ['音', '化', '井上', 'お願い', 'こと', '今日', 'それ', 'ところ', 'みたい', '話','的','人','何','自分','方','感じ','みんな','私','僕','今','時',
              '中','後','気','番','誰','風','結局', '技術','確か','そうそう','前','白金','鉱業','工業','最近','他','一番','好き','名前','データ','データサイエンティスト',
              '会社','分析','会','回','人たち','ブレインパッド','毎回','逆','内容','俺','じゃなくて','住所','人','一','あなた','データサイエンス', '一緒', '吉田', '十',
              '二','ソレ', '我々', '二つ', '今回', '上', '普通', '訳', 'たくさん', 'めちゃくちゃ', 'そうだ', '全部', '五', '八','百','側','一つ','さっき', '年',
              'うんそう','三', '目', '一', '四', '五','六','七','八','九','彼','コミュニティ','係','それぞれ','皆さん','お客さん','か月','非常','城中','上中','白銀',
              'お客様','千','大変','昔','データー','お話し','ないじゃないですか','系','キャレット', '個', '部分','形','問題','僕ら','当時','質問','一個','有村', '最適', '先生']
min_cnt = 2 #考慮する最低出現回数 default=2

word_freq_dict_without_sw = {}
for k,v in word_freq_dict.items():
    #print(k)
    if k not in stop_words and v > min_cnt: # stop wordの除外, 最低出現数の制限
        if not re.search(r'^[あ-ん]{1,2}$', k): # ひらがな1~2文字の単語も除外
            #print(k,v)
            word_freq_dict_without_sw[k] = v

wordcloud = WordCloud(
    background_color="white",
    max_words = 500,
    max_font_size=140,
    random_state=2019,
    width=900,
    height=500,
    font_path="~/Library/Fonts/RictyDiminished-Bold.ttf",
    stopwords=set(stop_words),
    )
wordcloud.generate_from_frequencies(word_freq_dict_without_sw)
#plt.imshow(wordcloud)

new_dir_path = './wordcloud_figs'
os.makedirs(new_dir_path, exist_ok=True)
output_path = "./wordcloud_figs/{}.png".format(file_b_name)
wordcloud.to_file(output_path)
print('Completed to make the wordcloud image: {}'.format(output_path))
