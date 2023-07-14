from fastapi import APIRouter,FastAPI,Path

handlefile = APIRouter()
from fastapi.responses import HTMLResponse,JSONResponse,FileResponse
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


mylog = logger.log("File Function Logs")


#方法可以混用，目前還沒研究為甚麼要這樣，但可以加上description
@handlefile.get("/GetFile/{filename}")
async def GetFile(filename:str = Path(description= "Complete_Filename (abc.txt)")):
    filepath = os.path.join(os.getcwd(),"data",f"{filename}")
    return FileResponse(filepath,filename=filename)

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
    
    
    folder = os.path.join(os.getcwd(),"data","txt")
    os.makedirs(folder, exist_ok=True)
    
    file_list = []
    
    for file in files:
        file_path = os.path.join(folder, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_list.append(file.filename)
    
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

    folder = os.path.join(os.getcwd(),"data","csv_xlsx")
    
    if not os.path.exists(folder):
        os.mkdir(folder)
    
    path = os.path.join(folder,file.filename)
    
    data_txtDF.to_csv(f"{path}.csv",index= False)
    data_txtDF.to_excel(f"{path}.xlsx",index= False)
    path += ".xlsx"
    return {"file":path}


@handlefile.post("/txt_to_csv_all/")
async def to_csv():
    txt_dir = os.path.join(os.getcwd(),"data","txt")
    finished = os.path.join(txt_dir,"finished")
    
    if not os.path.exists(txt_dir):
        os.mkdir(txt_dir)
    if not os.path.exists(finished):
        os.mkdir(finished)
    
            
    data_list = os.listdir(txt_dir)
    
    deal = 0
    deal_list =[]

    for f in data_list:
        if not f=="finished":
            deal = 1
            deal_list.append(f)
            read_path = os.path.join(txt_dir,f)
            with open(read_path, "r", encoding="utf-8") as file:
                lines = file.readlines()

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
            
            #data_txtDF[column_names[0]] = data_txtDF[column_names[0]].dt.time
            #data_txtDF[column_names[0]] = datetime.strftime(data_txtDF[column_names[0]],format="%H:%M:%S")
            #data_txtDF[column_names[0]] = data_txtDF[column_names[0]].astype(str)
            #data_txtDF[2:] = data_txtDF[2:].astype(float)
            
            folder = os.path.join(os.getcwd(),"data","csv_xlsx")
            
            if not os.path.exists(folder):
                os.mkdir(folder)
            
            path = os.path.join(folder,f)
            
            data_txtDF.to_csv(f"{path}.csv",index= False)
            data_txtDF.to_excel(f"{path}.xlsx",index= False)
            path += ".xlsx"
            file.close()
        
    
            src_path = os.path.join(txt_dir,f)
            des_path = os.path.join(finished,f)
            shutil.move(src_path,des_path)
            
    if deal: 
        return {"Transfer file":deal_list}
    else:
        return "No data exist"

