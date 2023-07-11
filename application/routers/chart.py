import pandas as pd
import matplotlib.pyplot as plt
from fastapi import APIRouter
import main,logger
from fastapi import FastAPI,Query,Path,Body,Header,Cookie,Response,Form,File,UploadFile
from fastapi.responses import FileResponse
import tempfile
import os
from datetime import datetime
import datetime
from matplotlib.dates import DateFormatter
from matplotlib.dates import date2num,datestr2num

chart = APIRouter()
mylog = logger.log("Chart Function Logs")



@chart.post("/plot")
async def plot(
    date :str ="yyyymmdd",
    file: UploadFile = File(description="A file read as UploadFile")
):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
        
    mylog.info("----------------plot function-------------")
    mylog.debug(f"input = {file} date  = {date}")
    
    #sheets = pd.ExcelFile(tmp_path)
    #for sheet in sheets:
    mylog.debug("read data")
    data = pd.read_excel(tmp_path)
    mylog.debug("read data")
    
    #data = pd.read_excel(tmp_path,sheet_name = page)
    
    # 繪製折線圖
    
    '''
    x = data.iloc[:,0]
    hour = x.apply(lambda t: t.hour)
    minute = x.apply(lambda t: t.minute)
    second = x.apply(lambda t: t.second)
    '''
    
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(figsize=(12, 8))             #設定輸出圖片的大小
    cols = data.shape[1]                    #獲取column的數量 若shape ==0，就是獲取row的數量
    col_names = data.columns.tolist()       #將column的名稱放進list並儲存在col_names
    mylog.debug("figure size  = (12,8)")
    mylog.debug("get column size and column name")
    
    
    
    x = data.iloc[:,0]
    x_len = len(x)
    
    start = 1
    end = 0
    
    for current in range(1,x_len):
        if x[current] < x[current-1] or current == x_len-1:
            start = end + 1
            end = current-1
            mylog.debug(f"Split data region start ={start} end = {end}\n")
            subx = x[start:end]
            x_str = subx.apply(lambda t: t.strftime("%H:%M:%S"))   #將datetime轉換為字串格式
            x_values = datestr2num(x_str)           # 將字串格式資料轉換為數值型別
            
            for i,col_name in zip(range(1,cols),col_names):
                y = data.iloc[start:end,i]
                plt.subplot(4,3,i)
                plt.plot(x_values, y)
                plt.xlabel('Time')
                plt.xticks(fontsize=8)
                plt.ylabel('Value')
                plt.title(f"{col_name}")
                mylog.debug(f"plot {col_name}")
                plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%H:%M:%S'))
            
            current = os.getcwd()
            folder = os.path.join(current,"log","usage")
            if not os.path.exists(folder):
                os.makedirs(folder)
            files = os.listdir(folder)
            if files:
                existcount = sum(1 for f in files if f.startswith("usage_"+date+"_"))
                #maxnum = max([int(f.split('.')[0]) for f in files])  #獲取檔案裏面數字最大的
                next = existcount + 1
            else : 
                next = 1 
                
            plt.suptitle(f"usage_{date}_{next}")
            plt.tight_layout()
            # 繪製折線圖
            # 將圖片儲存到本地
                
            image_name = f"usage_{date}_{next}.png"
            image_path = os.path.join(folder,image_name)
            plt.savefig(image_path)
            mylog.debug(f"output dir ={folder}")
            mylog.debug(f"save image ={image_name}")
           
            plt.clf()
            date_convert = datetime.datetime.strptime(date,"%Y%m%d").date()
            date_convert = date_convert +datetime.timedelta(days = 1)
            date = date_convert.strftime("%Y%m%d")
            mylog.debug(f"date update to {date}")
    
    
    # 將圖片作為響應返回到網頁上
    return FileResponse(image_path, media_type="image/png")
    
