from typing import Optional
from typing import List
from fastapi import FastAPI,Query
from enum import Enum
from typing import Dict
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name:str
    descri:Optional[str] = None
    price :float
    tax:int=0
    

#若是要使用先前建立過的class，要先from pydantic import BaseModel
#class宣告時也要使用 class 名稱(BaseModel)才能用post、put...建立class
class test(BaseModel):
    subject:str
    score:float
    

test2:test ={"science",55}
    
#進入網頁第一個程式
@app.get("/")
async def root():
    return {"message": "Hello World!!!"}


# 指定 api 路徑 @app.函數(路徑)
#可以藉由Optional或是設置初值為None讓變數成為可選參數

@app.get("/users/{user_id}") 
def read_user(user_id: int, q: Optional[str] = None):
    return {"user_id": user_id, "q": q}

#-------------------------------------------------------#

#這邊使用put的原因為：get函數不能擁有程式主體
@app.put("/L_Sum")
def List_Sum(L:List[int]=[], sum:int=0):
    for item in L:
        sum += item
    result = "L_sum"+" = "+str(sum)
    return result

#Diction的應用

@app.put("/Dict")
def Dictionary(Type:Dict[int,int]):
    return {str(Type[11])+" "+str(Type[40813])}

#Enum的應用

class Model(str,Enum):
    alexnet = "alexnet"
    CN = "CNN"
    RNN = "RNN"

@app.get("/ENUM")
def ENUM(hey:Model):
    if hey is Model.alexnet:
        return {"A_Model ": hey}
    if hey is Model.CN:
        return {"C_Model ": hey}
    if hey is Model.RNN:
        return {"R_Model ": hey}
    
#可以藉由API的函數來取用已經宣告過的變數
    
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

#兩個藉由API創建class的應用

@app.post("/Create Item")
async def Create(item:Item):
    if item.tax:
        item_dict = item.dict()
        money = item.price*0.9
        item_dict.update({"money":money})
    if(item.price<2000) :
        return ["生活費 = " + str(item.price) + " 小於2000 -> 生活拮据",item_dict]
    if (item.price>20000):
        return {"生活費 = " + str(item.price) +  " 大於20000 -> 生活富足",item_dict}
    else:
        return {"生活費 = " + str(item.price),item_dict}

@app.post("/Midterm")
async def Midterm(record:test):
    if (record.score >= 60) :
        return {"及格了，分數是 " :  record.score}
    else:
        return {"Fail，分數是 " : record.score}
'''
@app.get("/file/{filepath:path}")
def Get(filepath:str):
    return {"filepath":filepath}   
''' 