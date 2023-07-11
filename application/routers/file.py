from fastapi import APIRouter,FastAPI,Path

handlefile = APIRouter()
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.staticfiles import StaticFiles
import sys

import main,logger

from typing import Optional
from typing import List,Union,Any
from fastapi import FastAPI,Query,Path,Body,Header,Cookie,Response,Form,File,UploadFile
from enum import Enum
from typing import Dict
from pydantic import BaseModel,Field,EmailStr
import json
import numpy as np

mylog = logger.log("File Function Logs")


#方法可以混用，目前還沒研究為甚麼要這樣，但可以加上description
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
