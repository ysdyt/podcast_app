import MeCab
import re
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud

mecab = MeCab.Tagger ('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')

#file = './text/google_speech_api/08_001_NiRed-false_lev-false_samp44k.txt'
file = './text/aws_transcribe/07_001_NiRed-false_lev-false_samp16k.txt'
word = []
all_word = []

with open(file, 'r', encoding='utf-8') as f:
    text = f.read()
    print("char_len:",len(text.replace('\n', '')))
    
    node = mecab.parseToNode(text.replace('\n', ''))
    target_part = ('名詞')
    while node:
        #print(node.feature.split(",")[0])
        all_word.append(node.surface) #全単語取得
        if node.feature.split(",")[0] in target_part:
            #print(node.surface)
            word.append(node.surface) #名詞のみ取得
        node = node.next

print("重複有りの全単語数:",len(all_word))        
print("重複有りの名詞単語数:",len(word))

print(len(set(all_word)))
all_word_freq_dict = Counter(all_word)
#print(all_word_freq_dict)
print("重複なしの全単語数:", len(all_word_freq_dict))

print(word)
print(len(set(word)))
word_freq_dict = Counter(word)
print("重複なしの名詞単語数:", len(word_freq_dict))
