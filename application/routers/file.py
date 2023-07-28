from fastapi import APIRouter,FastAPI,Path

handlefile = APIRouter()
from fastapi.responses import HTMLResponse,JSONResponse,FileResponse,StreamingResponse
from fastapi.staticfiles import StaticFiles
import sys

import main,logger
import tempfile
from typing import Optional
from typing import List,Union,Any
from fastapi import FastAPI,Query,Path,Body,Header,Cookie,Response,Form,File,UploadFile

from enum import Enum
from typing import Dict
from pydantic import BaseModel,Field,EmailStr
import json
import numpy as np
import pandas as pd
import os
import shutil
from datetime import datetime
from configs import *


mylog = logger.log("File Function Logs")

@handlefile.get("/GetFile/{filename}")
async def GetFile(filename:str = Path(description= "Complete_Filename (abc.txt)")):
    mylog.info("---------GetFile Function---------")
    mylog.debug(f"input = {filename}")
    
    if filename.endswith(".txt") or filename.endswith(".log"):
        filepath = os.path.join(DATA_TXT_PATH,f"{filename}")
        if not os.path.exists(filepath):
            filepath = os.path.join(DATA_TXT_FINISH_PATH,f"{filename}")
    
        if os.path.exists(filepath):
                mylog.debug(f"File Exist, file_path = {filepath}")
                return StreamingResponse(open(filepath, "rb"), media_type="application/octet-stream",headers={"Content-Disposition": f"attachment; filename={filename}"})  #讓.txt或.log回傳形式是檔案
        
    elif filename.endswith(".xlsx") or filename.endswith(".csv"):
        filepath = os.path.join(DATA_CSV_PATH,f"{filename}")
        if not os.path.exists(filepath):
            filepath = os.path.join(DATA_CSV_FINISH_PATH,f"{filename}")
            
    if os.path.exists(filepath):
        mylog.debug(f"File Exist, file_path = {filepath}")
        return FileResponse(filepath,filename=filename)
    else:
        return "File does not exist"


#-------------------------FastAPI練習---------------------------------#


@handlefile.post("/uploadfile2/",include_in_schema= False)
async def create_upload_file(
    file: UploadFile = File(description="A file read as UploadFile"),
):
    mylog.info("--------------uploadfile2 function-------------")
    mylog.debug("input = "+file.filename )
    mylog.debug("output = filename : "+file.filename+"\n" )
    return {"filename": file.filename}


@handlefile.post("/mul_files/",include_in_schema= False)
async def create_files(files: list[bytes] = File()):
    mylog.info("--------------mul_files function-------------")
    mylog.debug("output = ")
    for i in files:
        mylog.debug("filelen = "+(len(i)))
    mylog.debug("")
    return {"file_sizes": [len(file) for file in files]}

#-------------------------------------------------------------#




def convert(s):
    try:
        return float(s)
    except:
        return s


#為了將txt檔案上傳到server或是電腦裡面存放txt的資料夾
@handlefile.post("/Upload_txt")
async def Upload_txt(
    files: list[UploadFile] = File()
):
    mylog.info("--------------Upload_txt function-------------")
    
    os.makedirs(DATA_TXT_PATH, exist_ok=True) #exist_OK = True是如果發現資料夾存在，也不會引發error，會繼續執行
    
    file_list = []
    
    for file in files:
        file_path = os.path.join(DATA_TXT_PATH, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer) #將file.file是代表一個可以讀取的二進制，並將此資料寫進buffer裡
        file_list.append(file.filename)
        mylog.debug(f"File :{file.filename} Saved.")
    
    return {"file":file_list }


@handlefile.post("/usage_txt_to_csv/")
async def create_upload_file(
    file: UploadFile = File(description="A file read as UploadFile"),
):
   
    mylog.info("--------------txt_to_csv function-------------")
    mylog.debug("input = "+file.filename )
    
    content = await file.read()   #讀取檔案，但因為這邊是二進制，所以下面要使用utf-8的encoding將data讀進lines裡面
    lines = content.decode("utf-8").split("\n")

    data_txt = []
    
    device_start_index = lines[0].find('(')   #獲取設備名稱
    device_end_index = lines[0].find(')')
    device = lines[0][device_start_index+1:device_end_index].strip()
    
    data_date_index = lines[0].find("西元")  #獲取資料日期
    data_obj = lines[0][data_date_index+2:data_date_index+13]
    data_date = datetime.strptime(data_obj,"%Y年%m月%d日").date()

    print(data_date)
    
    column_names = lines[2].strip().split()  #獲取資料的column names
    column_names[0] = "time"
    
    column_names.append(device)
    column_names.append(data_date)   #將剛剛獲得的device跟日期放進column裡面

    
    for line in lines[3:-2]:     #處理資料 因為第一行是資訊，第二行空行，第三行colume name 所以資料從3開始
        if line:
            column = line.strip().split()
            
            time_str = column[0]        #第一列是時間，將str資料轉換成datetime形式，資料有 時分秒
            date = datetime.strptime(time_str,"%H時%M分%S秒").time()
            data_txt.append([date]+[convert(x) for x in column[1:]]+[None]*2) #將資料放進row裡面
            

    data_txtDF = pd.DataFrame(data_txt,columns= column_names)   #將資料轉換成dataframe形式

    
    if not os.path.exists(DATA_CSV_PATH):
        os.mkdir(DATA_CSV_PATH)
    
    if file.filename.endswith(".txt") or file.filename.endswith(".log") :
        store_name = device + "_" + file.filename.rsplit('.',1)[0] #只獲取檔名(不含附檔名)
        path = os.path.join(DATA_CSV_PATH,store_name)
    
    data_txtDF.to_csv(f"{path}.csv",index= False,encoding="utf-8") #將資料儲存為csv或xlsx
    data_txtDF.to_excel(f"{path}.xlsx",index= False)
    path += ".xlsx"
    return {"file":path}


@handlefile.post("/usage_txt_to_csv_all/")
async def to_csv():
    mylog.info("---------txt_to_csv_all Function---------")
    if not os.path.exists(DATA_TXT_PATH):
        os.mkdir(DATA_TXT_PATH)
    if not os.path.exists(DATA_TXT_FINISH_PATH):
        os.mkdir(DATA_TXT_FINISH_PATH)
    
            
    data_list = os.listdir(DATA_TXT_PATH)
    
    deal = 0
    deal_list =[]
    
    

    for f in data_list:
        if not f=="finished":
            deal = 1
            deal_list.append(f)
            read_path = os.path.join(DATA_TXT_PATH,f)
            with open(read_path, "r", encoding="utf-8") as file:
                lines = file.readlines()

            mylog.debug(f"Open file{f} and readlines ")
            mylog.debug("Dealing with data")
            
            
            device_start_index = lines[0].find('(')
            device_end_index = lines[0].find(')')
            device = lines[0][device_start_index+1:device_end_index].strip()
            
            data_date_index = lines[0].find("西元")
            data_obj = lines[0][data_date_index+2:data_date_index+13]
            data_date = datetime.strptime(data_obj,"%Y年%m月%d日").date()
            
            data_txt = []
            column_names = lines[2].strip().split()
            column_names[0] = "time"
            
            column_names.append(device)
            column_names.append(data_date)
        

            for line in lines[3:-2]:
                if line:
                    column = line.strip().split()
                    
                    time_str = column[0]
                    date = datetime.strptime(time_str,"%H時%M分%S秒").time()
                    data_txt.append([date]+[convert(x) for x in column[1:]]+[None]*2)
                    
                    #data_txt.append([convert(x) for x in column[:]])
                    
                    #date = pd.to_datetime(time_str, format="%H時%M分%S秒").time.strftime("%H:%M:%S")
                    #date = pd.to_datetime(time_str,format="%H時%M分%S秒")

            data_txtDF = pd.DataFrame(data_txt,columns= column_names)
            mylog.debug("Complete transfer data to DataFrame")
            #data_txtDF[column_names[0]] = data_txtDF[column_names[0]].dt.time
            #data_txtDF[column_names[0]] = datetime.strftime(data_txtDF[column_names[0]],format="%H:%M:%S")
            #data_txtDF[column_names[0]] = data_txtDF[column_names[0]].astype(str)
            #data_txtDF[2:] = data_txtDF[2:].astype(float)
            
            
            if not os.path.exists(DATA_CSV_PATH):
                os.mkdir(DATA_CSV_PATH)
            
            if f.endswith(".txt") or f.endswith(".log") :
                store_name = device + "_" + f.rsplit('.',1)[0]
                    
            path = os.path.join(DATA_CSV_PATH,store_name)
            
            mylog.debug(f"Saving {f}.csv file")
            data_txtDF.to_csv(f"{path}.csv",index= False)
            mylog.debug(f"Saving {f}.xlsx file")
            data_txtDF.to_excel(f"{path}.xlsx",index= False)
            mylog.debug("Finish saving files")
            file.close()
            
            src_path = os.path.join(DATA_TXT_PATH,f)
            des_path = os.path.join(DATA_TXT_FINISH_PATH,f) 
            
            shutil.move(src_path,des_path)
            mylog.debug(f"{f} moved to {des_path}")
            mylog.debug("-------------------------------")
            
    if deal:
        mylog.debug(f"Transfile :{deal_list}") 
        return {"Transfer file":deal_list}
    else:
        mylog.debug("No data exist")
        return "No data exist"

