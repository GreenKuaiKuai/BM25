import sys
import json
from udicOpenData.dictionary import *
from udicOpenData.stopwords import *


allDocumentLength = 355949;	# 全部歌詞的平均長度
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
	if keyword in inverted_index:
		return inverted_index[keyword]
	else:
		return []

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

# 計算BM25分數
def getBM25Value(keyword, document):
	k = 1		# 分數權重
	b = 0.5		# 文章長度考量權重
	tf = getTermFrequency(keyword, document)	# 關鍵字在這首歌出現幾次
	dl = getDocumentLength(document)			# 這首歌的歌詞長度
	adl = allDocumentLength						# 所有歌曲的歌詞平均長度

	score = (k + 1) * tf / (tf + k * (1.0 - b + b * dl / adl))
	return score

# 輸入使用者的關鍵字句，回傳關聯性排序歌單
def BM25Sort(searchQuery):
	searchQuery = getQuery(searchQuery)	# 關鍵字句斷詞
	songScore = dict()
	for keyword in searchQuery:
		songList = getSongs(keyword);	# 取得包含這個關鍵字的歌單
		for song in songList:				# 計算這個關鍵字在各首歌有幾分，累加結果
			if song in songScore:
				songScore[song] += getBM25Value(keyword, song)
			else:
				songScore[song] = getBM25Value(keyword, song)

	result = dict(sorted(songScore.items(), key=lambda x:x[1], reverse=True))		#分數由高至低排序

	return list(result.keys())


# ----------- 測試 ---------------
# 傳query到function
def run(query):
	result = BM25Sort(query)
	print("\n搜尋: {:20}\n前10名:".format(query))
	for i in range(len(result)):
		print("{:3} - {:10}".format(i+1, result[i]))			# 印出前10筆
	return result

# 用command line送關鍵字
def runCMD():
	if len(sys.argv) < 1:		# 沒有查詢關鍵字
		print("No Query\n")
		return
	else:
		query = " ".join(sys.argv[1:])
	run(query)

runCMD()