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


#方法可以混用，目前還沒研究為甚麼要這樣，但可以加上description
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

@handlefile.post("/uploadfile2/")
async def create_upload_file(
    file: UploadFile = File(description="A file read as UploadFile"),
):
    mylog.info("--------------uploadfile2 function-------------")
    mylog.debug("input = "+file.filename )
    mylog.debug("output = filename : "+file.filename+"\n" )
    return {"filename": file.filename}


@handlefile.post("/mul_files/")
async def create_files(files: list[bytes] = File()):
    mylog.info("--------------mul_files function-------------")
    mylog.debug("output = ")
    for i in files:
        mylog.debug("filelen = "+(len(i)))
    mylog.debug("")
    return {"file_sizes": [len(file) for file in files]}

def convert(s):
    try:
        return float(s)
    except:
        return s

@handlefile.post("/Upload_txt")
async def Upload_txt(
    files: list[UploadFile] = File()
):
    mylog.info("--------------Upload_txt function-------------")
    
    os.makedirs(DATA_TXT_PATH, exist_ok=True)
    
    file_list = []
    
    for file in files:
        file_path = os.path.join(DATA_TXT_PATH, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_list.append(file.filename)
        mylog.debug(f"File :{file.filename} Saved.")
    
    return {"file":file_list }


@handlefile.post("/txt_to_csv/")
async def create_upload_file(
    file: UploadFile = File(description="A file read as UploadFile"),
):
   
    mylog.info("--------------txt_to_csv function-------------")
    mylog.debug("input = "+file.filename )
    
    content = await file.read()
    lines = content.decode("utf-8").split("\n")

    data_txt = []
    column_names = lines[2].strip().split()
    column_names[0] = "time"
    
    for line in lines[3:-2]:
        if line:
            column = line.strip().split()
            
            time_str = column[0]
            date = datetime.strptime(time_str,"%H時%M分%S秒").time()
            data_txt.append([date]+[convert(x) for x in column[1:]])
            

    data_txtDF = pd.DataFrame(data_txt,columns= column_names)

    
    if not os.path.exists(DATA_CSV_PATH):
        os.mkdir(DATA_CSV_PATH)
    
    path = os.path.join(DATA_CSV_PATH,file.filename)
    
    data_txtDF.to_csv(f"{path}.csv",index= False)
    data_txtDF.to_excel(f"{path}.xlsx",index= False)
    path += ".xlsx"
    return {"file":path}


@handlefile.post("/txt_to_csv_all/")
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
            
            data_txt = []
            column_names = lines[2].strip().split()
            column_names[0] = "time"
            
            for line in lines[3:-2]:
                if line:
                    column = line.strip().split()
                    
                    time_str = column[0]
                    date = datetime.strptime(time_str,"%H時%M分%S秒").time()
                    data_txt.append([date]+[convert(x) for x in column[1:]])
                    
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
            
            path = os.path.join(DATA_CSV_PATH,f)
            
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

