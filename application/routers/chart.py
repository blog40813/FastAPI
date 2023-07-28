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
from configs import *
from enum import Enum
import shutil

chart = APIRouter()
mylog = logger.log("Chart Function Logs")



@chart.get("/GetChart/{filename}")
async def GetFile(filename:str = Path(description= "Filename",example="filename.filetype_YYYYMMDD_number")):
    mylog.info("----------------GetChart function-------------")
    filepath = os.path.join(DATA_USAGE_PATH,f"{filename}.png")
    mylog.debug(f"Finding Chart {filename}")
    if os.path.exists(filepath):
        mylog.debug(f"Chart exist, return {filename}")
        return FileResponse(filepath,media_type="image/png")
    else:
        mylog.debug(f"{filename} does not exist")
        return f"{filename} does not exist"


@chart.post("/plot")
async def plot(
    date :str ="yyyymmdd",
    file: UploadFile = File(description="A file read as UploadFile")
):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
        
    mylog.info("----------------plot function-------------")
    mylog.debug(f"input = {file.filename} date  = {date}")
    

    if file.filename.endswith( ".csv"):
        # 處理 CSV 文件
        data = pd.read_csv(tmp_path)
    elif file.filename.endswith((".xls", ".xlsx")):
        # 處理 Excel 文件
        data = pd.read_excel(tmp_path)
    else:
        # Error
        return {"error": "Unsupported file format"}

    
    
    #sheets = pd.ExcelFile(tmp_path)
    #for sheet in sheets:
    #data = pd.read_excel(tmp_path)
    mylog.debug("read data")
    
    #data = pd.read_excel(tmp_path,sheet_name = page)
    
    # 繪製折線圖
    
    '''
    x = data.iloc[:,0]
    hour = x.apply(lambda t: t.hour)
    minute = x.apply(lambda t: t.minute)
    second = x.apply(lambda t: t.second)
    '''
    
    plt.rcParams['axes.unicode_minus'] = False #繪製圖表的時候希望負號不要變成破折號

    plt.figure(figsize=(12, 8))             #設定輸出圖片的大小
    cols = data.shape[1]                    #獲取column的數量 若shape ==0，就是獲取row的數量
    col_names = data.columns.tolist()       #將column的名稱放進list並儲存在col_names
    mylog.debug("figure size  = (12,8)")
    mylog.debug("get column size and column name")
    
    
    
    x = data.iloc[:,0] # data在前面有先利用pandas的功能讀取成 data frame ，這邊是取用 colume = 0 的資料，在這裡通常是時間資料(時：分：秒)
    x_len = len(x) #取得資料總共有幾筆
    
    start = 1
    end = 0

   
    for current in range(1,x_len):
        if x[current] < x[current-1] or current == x_len-1:   #切分出每一天的資料 也就是當現在時間小於剛剛的時間代表跨天 並記錄這天資料的start跟end準備繪圖
            start = end + 1
            end = current-1
            mylog.debug(f"Split data region start ={start} end = {end}")
            mylog.debug("--------------------------------------------")
            subx = x[start:end]
            check =0
            
            for item in subx:                           #確認這個時間資料是字串還是datetime型別，如果是datetime會轉換成字串以利使用
                if isinstance(item,str):
                    check = 1
                    
            if check==0:
                x_str = subx.apply(lambda t: t.strftime("%H:%M:%S"))   #將datetime轉換為字串格式 
            else:
                x_str = subx
            

            x_values = datestr2num(x_str)# 將字串格式資料轉換為數值型別，讓等等繪圖的時候可以正確使用時間資料
            
            for i,col_name in zip(range(1,cols),col_names[1:]):  #針對每一個column繪圖，其實也可以使用 col_names[i]來取用標題內容，這邊是針對zip做練習
                y = data.iloc[start:end,i]
                plt.subplot(4,3,i)    #因為資料最多不會超過12筆，所以這邊直接以12當標準，不過也可以使用 (cols-1)/3 , 3,i讓每一行都有三筆資料 自動分割
                plt.plot(x_values, y)  #這邊是先plot再設定折線圖的title x/y axis等等
                plt.xlabel('Time')
                plt.xticks(fontsize=8)
                plt.ylabel('Value')
                plt.title(f"{col_name}")
                mylog.debug(f"plot {col_name}")
                plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%H:%M:%S'))  #讓X軸的時間數值表示方式是時 分 秒
            
            
            '''
            if not os.path.exists(DATA_USAGE_PATH):
                os.makedirs(DATA_USAGE_PATH)
            files = os.listdir(DATA_USAGE_PATH)
            '''
            store_path = os.path.join(DATA_USAGE_PATH,file.filename.split('.')[0])  #儲存檔案(設定儲存目標資料夾)
            if not os.path.exists(store_path):
                os.makedirs(store_path)
                
            files = os.listdir(store_path)  #獲取資料夾裡面擁有的檔案
                
            if files:
                existcount = sum(1 for f in files if f.startswith(f"{file.filename}_"+date+"_")) #如果發現相同檔案相同日子已經有檔案，那就編號+1
                
                #maxnum = max([int(f.split('.')[0]) for f in files])  #獲取檔案裏面數字最大的
                next = existcount + 1
            else : 
                next = 1 
                
            plt.suptitle(f"{file.filename}_{date}_{next}")
            plt.tight_layout()
            # 設定整張圖片的標題，以及tight layout 是讓每一個圖片有合理的間距跟布置，使得不會疊圖

            # 將圖片儲存到資料夾裡面
            image_name = f"{file.filename}_{date}_{next}.png"
            image_path = os.path.join(store_path,image_name)
            plt.savefig(image_path)
            mylog.debug(f"output dir ={store_path}")
            mylog.debug(f"save image ={image_name}")
           
            #儲存完圖片之後要將內容全部清空
            #更新日期，先將date(str)轉換成datetime並加上一天，再將此日期轉換回str資料以利使用
            plt.clf()
            date_convert = datetime.datetime.strptime(date,"%Y%m%d").date()
            date_convert = date_convert +datetime.timedelta(days = 1)
            date = date_convert.strftime("%Y%m%d")
            mylog.debug(f"date update to {date}")
    
    
    # 將圖片作為響應返回到網頁上
    return FileResponse(image_path, media_type="image/png")

@chart.post("/plot2")
async def plot(
    file: UploadFile = File(description="A file read as UploadFile")
):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
    
    mylog.info("----------------plot function-------------")
    mylog.debug(f"input = {file.filename}")

    if file.filename.endswith( ".csv"):
        # 處理 CSV 文件
        data = pd.read_csv(tmp_path)
        file_type = 0
    elif file.filename.endswith((".xls", ".xlsx")):
        # 處理 Excel 文件
        data = pd.read_excel(tmp_path)
        file_type = 1
    else:
        file_type = 2
        return {"error": "Unsupported file format"}

    #sheets = pd.ExcelFile(tmp_path)
    #for sheet in sheets:
    #data = pd.read_excel(tmp_path)
    mylog.debug("read data")
    
    #data = pd.read_excel(tmp_path,sheet_name = page)
    
    # 繪製折線圖
    
    '''
    x = data.iloc[:,0]
    hour = x.apply(lambda t: t.hour)
    minute = x.apply(lambda t: t.minute)
    second = x.apply(lambda t: t.second)
    '''
    
    plt.rcParams['axes.unicode_minus'] = False  #繪製圖表的時候希望負號不要變成破折號
    plt.figure(figsize=(12, 8))             #設定輸出圖片的大小
    cols = data.shape[1]                    #獲取column的數量 若shape ==0，就是獲取row的數量
    col_names = data.columns.tolist()       #將column的名稱放進list並儲存在col_names
    mylog.debug("figure size  = (12,8)")
    mylog.debug("get column size and column name")
    
    if file_type == 0:
        date =col_names[-1].replace('-','')
    elif file_type == 1:
        date = datetime.datetime.strftime(col_names[-1],"%Y%m%d")

    x = data.iloc[:,0]   # data在前面有先利用pandas的功能讀取成 data frame ，這邊是取用 colume = 0 的資料，在這裡通常是時間資料(時：分：秒)
    x_len = len(x) #取得資料總共有幾筆
    
    start = 1
    end = 0
    
    for current in range(1,x_len):
        if x[current] < x[current-1] or current == x_len-1: #切分出每一天的資料 也就是當現在時間小於剛剛的時間代表跨天 並記錄這天資料的start跟end準備繪圖
            start = end + 1
            end = current-1
            mylog.debug(f"Split data region start ={start} end = {end}")
            mylog.debug("--------------------------------------------")
            subx = x[start:end]
            check =0
            
            for item in subx: #確認這個時間資料是字串還是datetime型別，如果是datetime會轉換成字串以利使用
                if isinstance(item,str):
                    check = 1
                    
            if check==0:
                x_str = subx.apply(lambda t: t.strftime("%H:%M:%S"))   #將datetime轉換為字串格式 
            else:
                x_str = subx
                
            x_values = datestr2num(x_str)# 將字串格式資料轉換為數值型別
            
            for i,col_name in zip(range(1,cols),col_names[1:]): #針對每一個column繪圖，其實也可以使用 col_names[i]來取用標題內容，這邊是針對zip做練習
                y = data.iloc[start:end,i]
                if y is not None:
                    plt.subplot(4,3,i) #因為資料最多不會超過12筆，所以這邊直接以12當標準，不過也可以使用 (cols-1)/3 , 3,i讓每一行都有三筆資料 自動分割
                    plt.plot(x_values, y) #這邊是先plot再設定折線圖的title x/y axis等等
                    plt.xlabel('Time')
                    plt.xticks(fontsize=8)
                    plt.ylabel('Value')
                    plt.title(f"{col_name}")
                    mylog.debug(f"plot {col_name}")
                    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%H:%M:%S'))  #讓X軸的時間數值表示方式是時 分 秒
            '''
            if not os.path.exists(DATA_USAGE_PATH):
                os.makedirs(DATA_USAGE_PATH)
            files = os.listdir(DATA_USAGE_PATH)
            '''
            store_path = os.path.join(DATA_USAGE_PATH,file.filename.split('.')[0]) #儲存檔案(設定儲存目標資料夾)
            if not os.path.exists(store_path):
                os.makedirs(store_path)
            
            files = os.listdir(store_path) #獲取資料夾裡面擁有的檔案
                
                
            if files:
                existcount = sum(1 for f in files if f.startswith(f"{file.filename}_"+date+"_")) #如果發現相同檔案相同日子已經有檔案，那就編號+1
                #maxnum = max([int(f.split('.')[0]) for f in files])  #獲取檔案裏面數字最大的
                next = existcount + 1
            else : 
                next = 1 
                
            plt.suptitle(f"{file.filename}_{date}_{next}")
            plt.tight_layout()
            # 設定整張圖片的標題，以及tight layout 是讓每一個圖片有合理的間距跟布置，使得不會疊圖

            # 將圖片儲存到資料夾裡面
            
             #儲存完圖片之後要將內容全部清空
            #更新日期，先將date(str)轉換成datetime並加上一天，再將此日期轉換回str資料以利使用
                
            image_name = f"{file.filename}_{date}_{next}.png"
            image_path = os.path.join(store_path,image_name)
            plt.savefig(image_path)
            mylog.debug(f"output dir ={store_path}")
            mylog.debug(f"save image ={image_name}")
           
            plt.clf()
            date_convert = datetime.datetime.strptime(date,"%Y%m%d").date()
            date_convert = date_convert +datetime.timedelta(days = 1)
            date = date_convert.strftime("%Y%m%d")
            mylog.debug(f"date update to {date}")
    
    
    # 將圖片作為響應返回到網頁上
    return FileResponse(image_path, media_type="image/png")




class Model(str,Enum):  
    csv = "csv"
    excel = "excel"
    all = "all"




@chart.post("/plot_all")
async def plot(input : Model):
    if not os.path.exists(DATA_USAGE_PATH):
        os.makedirs(DATA_USAGE_PATH)
    if not os.path.exists(DATA_CSV_FINISH_PATH):
        os.makedirs(DATA_CSV_FINISH_PATH)
    if not os.path.exists(DATA_CSV_PATH):
        os.makedirs(DATA_CSV_PATH)
    
    data_list = os.listdir(DATA_CSV_PATH)
    deal = 0
    deal_list =[]
    
    for f in data_list:
        readpath =os.path.join(DATA_CSV_PATH,f)
        if (input is Model.csv or input is Model.all):
            if f.endswith( ".csv"):
                # 處理 CSV 文件
                data = pd.read_csv(readpath)
                deal = 1
                file_type = 0
            else:
                deal = 0
        elif (input is Model.excel or input is Model.all):
            if f.endswith((".xls", ".xlsx")):
                # 處理 Excel 文件
                data = pd.read_excel(readpath)
                deal = 1
                file_type = 1
            else:
                deal = 0
        else:
            
            return {"error": "Unsupported file format"}
        
        #sheets = pd.ExcelFile(tmp_path)
        #for sheet in sheets:
        #data = pd.read_excel(tmp_path)
        mylog.debug("read data")
        
        #data = pd.read_excel(tmp_path,sheet_name = page)
        
        # 繪製折線圖
        
        '''
        x = data.iloc[:,0]
        hour = x.apply(lambda t: t.hour)
        minute = x.apply(lambda t: t.minute)
        second = x.apply(lambda t: t.second)
        '''
        if deal:
            deal_list.append(f)
            
            plt.rcParams['axes.unicode_minus'] = False
            
            plt.figure(figsize=(12, 8))             #設定輸出圖片的大小
            cols = data.shape[1]                    #獲取column的數量 若shape ==0，就是獲取row的數量
            col_names = data.columns.tolist()       #將column的名稱放進list並儲存在col_names
            mylog.debug("figure size  = (12,8)")
            mylog.debug("get column size and column name")
            
            
            if file_type == 0:
                date =col_names[-1].replace('-','')
            elif file_type == 1:
                date = datetime.datetime.strftime(col_names[-1],"%Y%m%d")
            
            
            x = data.iloc[:,0]
            x_len = len(x)
            
            start = 0
            end = -1
            
            for current in range(0,x_len):
                if not current==0 and  x[current] < x[current-1] or current == x_len-1:
                    start = end + 1
                    end = current-1
                    mylog.debug(f"Split data region start ={start} end = {end+2}")
                    mylog.debug("--------------------------------------------")
                    subx = x[start:end]
                    check =0
                    for item in subx:
                        if isinstance(item,str):
                            check = 1
                            
                    if check==0:
                        x_str = subx.apply(lambda t: t.strftime("%H:%M:%S"))   #將datetime轉換為字串格式 
                    else:
                        x_str = subx
                        
                    x_values = datestr2num(x_str)# 將字串格式資料轉換為數值型別
                    
                    for i,col_name in zip(range(1,cols),col_names[1:]):
                        y = data.iloc[start:end,i]
                        plt.subplot(4,3,i)
                        plt.plot(x_values, y)
                        plt.xlabel('Time')
                        plt.xticks(fontsize=8)
                        plt.ylabel('Value')
                        plt.title(f"{col_name}")
                        mylog.debug(f"plot {col_name}")
                        plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%H:%M:%S'))
                    
                    
                    '''
                    if not os.path.exists(DATA_USAGE_PATH):
                        os.makedirs(DATA_USAGE_PATH)
                    files = os.listdir(DATA_USAGE_PATH)
                    '''
                    store_path = os.path.join(DATA_USAGE_PATH,f.split('.')[0])
                    if not os.path.exists(store_path):
                        os.makedirs(store_path)
                    files = os.listdir(store_path)
                    
                    
                    if files:
                        existcount = sum(1 for file in files if file.startswith(f"{f}_"+date+"_"))
                        
                        #maxnum = max([int(f.split('.')[0]) for f in files])  #獲取檔案裏面數字最大的
                        next = existcount + 1
                    else : 
                        next = 1 
                        
                    plt.suptitle(f"{f}_{date}_{next}")
                    plt.tight_layout()
                    # 繪製折線圖
                    # 將圖片儲存到本地
                        
                    image_name = f"{f}_{date}_{next}.png"
                    image_path = os.path.join(store_path,image_name)
                    plt.savefig(image_path)
                    mylog.debug(f"output dir ={store_path}")
                    mylog.debug(f"save image ={image_name}")
                
                    plt.clf()
                    date_convert = datetime.datetime.strptime(date,"%Y%m%d").date()
                    date_convert = date_convert +datetime.timedelta(days = 1)
                    date = date_convert.strftime("%Y%m%d")
                    mylog.debug(f"date update to {date}")
                    
            
        
            src_path = os.path.join(DATA_CSV_PATH,f)
            des_path = os.path.join(DATA_CSV_FINISH_PATH,f) 
            shutil.move(src_path,des_path)

        
                    
                    
        
    
    # 將圖片作為響應返回到網頁上
    return deal_list





