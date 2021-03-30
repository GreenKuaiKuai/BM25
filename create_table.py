import os
from os.path import join
from udicOpenData.dictionary import *
from udicOpenData.stopwords import *
import json

## 歌詞檔案路徑
lyricsPath = "/home/gigi/BM25/txt/"
## 設定名詞flag
n = ['j','mg','n','ng','nr','nrfg','nrt','ns','nt','nz','s','tg']
## 反向索引詞表 token:歌曲編號:出現次數
inverted_index = dict() 
## 歌曲編號表  index即是此歌曲編號
song_index = [] 
## 文章長度列表
song_length = []
## 全部文章長度
all_length = 0

## 讀每個歌詞檔
fileList = os.listdir(lyricsPath)
for lyricsFile in fileList:

    ## 儲存歌名
    song_index.append(lyricsFile[:-4])
    now_index = len(song_index) - 1
    length = 0

    print(lyricsFile[:-4]) #去掉副檔名

    ## 讀歌詞檔
    fullpath = join(lyricsPath, lyricsFile)
    with open(fullpath, 'r') as f:
        for line in f.readlines(): ## 每一行歌詞

            tokens = list(rmsw(line, flag=True)) # 斷詞
            length += len(tokens)

            for num in range(len(tokens)):
                if (tokens[num][1] in n and len(tokens[num][0]) > 1): ## 是名詞且大於一個字
                    token = tokens[num][0]
                    if token not in inverted_index:
                        inverted_index[token] = {now_index: 1}
                    else:
                        if now_index not in inverted_index[token]:
                            inverted_index[token][now_index] = 1
                        else:
                            inverted_index[token][now_index] += 1
    
    ## 儲存長度
    song_length.append(length)
    all_length += length

print("全部文章長度: "+ str(all_length) )
# print(song_index)
# print(song_length)

## 儲存反向索引表
with open('inverted_index.json', 'w') as outfile:  
    json.dump(inverted_index, outfile)

with open('song_index.json', 'w') as outfile:  
    json.dump(song_index, outfile)

with open('song_length.json', 'w') as outfile:  
    json.dump(song_length, outfile)