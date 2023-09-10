from fastapi import APIRouter
import requests as req
import os
import sys
import yt_dlp as youtube_dl
import pandas as pd
import time
from configs import *
yt = APIRouter()

#123
#獲取各個影片資料的函數
def get_video_info(ok):
    print(f"check the correct url = {ok}")
    video_info = {}
    try:
        with youtube_dl.YoutubeDL() as ydl:
            info = ydl.extract_info(ok, download=False)
            video_info['ID'] = info.get('id')
            video_info['標題'] = info.get('title')
            video_info['影片縮圖'] = info.get('thumbnail')
            video_info['上傳者'] = info.get('uploader')
            video_info['上傳者網址'] = info.get('uploader_url')
            video_info['影片長度(秒)'] = info.get('duration')
            video_info['觀看次數'] = info.get('view_count',0)
            video_info['留言數'] = info.get('comment_count',0) 
            if video_info['留言數'] is None:
                video_info['留言數'] = 0
            video_info['喜歡數'] = info.get('like_count',0)
            video_info['描述'] = info.get('description')
            video_info['標籤'] = info.get('tags')
            video_info['網頁網址'] = info.get('webpage_url')
            video_info['上傳日期'] = info.get('upload_date')
            video_info['留言數:觀看數(%)'] = video_info['留言數'] / video_info['觀看次數'] *100
            video_info['喜歡數:觀看數(%)'] = video_info['喜歡數'] / video_info['觀看次數'] *100
            
            
    except youtube_dl.utils.DownloadError as e:
        print("取得影片資訊時出現錯誤：", e)
    return(video_info)


@yt.post("/youtube/get_video")
async def Get_Hot_Video():
    if not os.path.exists(DATA_PATH):
        os.mkdir(DATA_PATH)
        
    if not os.path.exists(VIDEO_LIST_PATH):
        os.mkdir(VIDEO_LIST_PATH)

    #google API key
    key="AIzaSyAszU0t5_IygOjinPadilL3a5EAZNbWIlA"
    #最多100筆
    maxResults=100

    #要從google api裡面獲取哪些資料
    params={
        "part":"snippet,contentDetails,statistics",
        "chart":"mostPopular",
        "regionCode":"TW",
        "key":key,
        "maxResults":maxResults
    }
    #API url
    url="https://youtube.googleapis.com/youtube/v3/videos"

    #用get函數獲取資料，並將response轉換為json
    response=req.get(url, params=params)
    r = response.json()

    #提取出裡面Items的id，等等會用於access每個影片
    video_id = []
    for res in r['items']:
        video_id.append(res['id'])

    count = len(video_id)
    data =[]

    #access每個影片，並獲取此影片的各種資料，並將這些資料以一個dict list儲存返回
    for i in range(count):
        next_to_be_get = video_id[i]
        herf = f"https://www.youtube.com/watch?v={next_to_be_get}"
        data.append(get_video_info(herf))

    #將此dict list轉換為dataframe，輸出成excel檔
    df = pd.DataFrame(data)
    df['留言率排名'] = df['留言數:觀看數(%)'].rank(ascending=False)
    df['喜歡率排名'] = df['喜歡數:觀看數(%)'].rank(ascending=False)

    now = time.strftime("%Y-%m-%d")
    save_path = os.path.join(VIDEO_LIST_PATH,f"{now}_videolist.xlsx")
    df.to_excel(save_path,index=True)

    return save_path


    