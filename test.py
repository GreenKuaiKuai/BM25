import json
from udicOpenData.dictionary import *
from udicOpenData.stopwords import *


allDocumentLength = 352342;	# 全部歌詞的平均長度
n = ['j','mg','n','ng','nr','nrfg','nrt','ns','nt','nz','s','tg'] ## 設定名詞flag


## 載入反向索引表
print('load json')
with open("/home/gigi/BM25/inverted_index.json", 'r') as f:
    inverted_index = json.load(f)

## 載入歌詞長度表
with open("/home/gigi/BM25/song_length.json", 'r') as f:
    song_length = json.load(f)
print('done')


def getSongs(keyword):
	# 用關鍵字取得包含這個詞的歌單(反向索引)
	return inverted_index[keyword]

def getTermFrequency(keyword, document):
	# 用關鍵字跟歌名去查這個詞在這首歌出現幾次
	return inverted_index[keyword][document]

def getDocumentLength(document):
	# 用歌名找這首歌的長度
	return song_length[document]

def getQuery(query):
    ## 對query做斷詞，回傳keyword list
    tokens = list(rmsw(query, flag=True))
    keyword_list = []
    
    for num in range(len(tokens)):
        if (tokens[num][1] in n and len(tokens[num][0]) > 1): ## 是名詞且大於一個字
            keyword_list.append(tokens[num][0])
    
    return keyword_list




