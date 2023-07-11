from fastapi import APIRouter,FastAPI,Path

funct = APIRouter()
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

mylog = logger.log("Funct Function Logs")

class Item(BaseModel):
    name:str = "Leo"
    descri:Optional[str] = None
    price :float = 30000
    tax:int=0


@funct.get("/L_Sum_Query")
def List_Sum(L:List[int]=Query(default=[1,2,3]), sum:int=0):
    mylog.info("--------------L_Sum_Query Function----------")
    string="sum = " + str(sum)+" "
    for item in L:
        sum += item
        string =string + str(item) + " "
    mylog.debug("input = "+string)
    result = "L_sum"+" = "+str(sum)
    mylog.debug("output = "+result+"\n")
    return result


class Model(str,Enum):  
    alexnet = "alexnet"
    CN = "CNN"
    RNN = "RNN"

@funct.get("/ENUM")
def ENUM(hey:Model,de:Model):
    mylog.info("--------------ENUM Function----------")
    if hey is Model.alexnet:
        mylog.debug("output = A_Model :" + hey + " , de_Model :"+de+"\n")
        return {"A_Model ": hey ,"de_Model":de}
    if hey is Model.CN:
        mylog.debug("output = C_Model :" + hey + "\n")
        return {"C_Model ": hey}
    if hey is Model.RNN:
        mylog.debug("output = R_Model :" + hey + "\n")
        return {"R_Model ": hey}
    
    
#利用Query設定參數限制
#如果是int 有 gt(>),ge(>=),lt(<).le(<=) ，字串則可以使用min_length以及max_length
#alias 是可以更改頁面上左側變數顯示的名字，而description則是更改在input的格子上面的description

@funct.get("/limit_the_length")
async def limit_length(input:str=Query(default=None,min_length=3,max_length=8,alias="My input string",description="length must be 3~8")):
    mylog.info("--------------limit_the_length Function----------")
    result = "input = "+input
    mylog.debug(result)
    mylog.debug("output = "+result+"\n")
    return result


#Body函數，使得某參數也可以進入request Body，但不得用於路徑參數
#也就是說：原本會以上方格子形式輸入的參數，可以從下面Request Body的格子輸入
#如果原本就是一個class 使用body的函數，且embed = false ，request body裡面不會有變數名稱
#但若此時將embed = True 會有變數名稱的顯示

@funct.put("/body")
async def update_item(item_id: int =Body(embed=True), item: Item = Body(embed=True)):
    results = {"item_id": item_id, "item": item}
    mylog.info("--------------body Function----------")
    mylog.debug("input = "+str(results))
    mylog.debug("output = "+str(results)+"\n")
    return results
