from typing import Optional
from typing import List,Union
from fastapi import FastAPI,Query,Path,Body
from enum import Enum
from typing import Dict
from pydantic import BaseModel,Field


app =  FastAPI()
app1 = FastAPI()
app2 = FastAPI()
app3 = FastAPI()

class Item(BaseModel):
    name:str = "Leo"
    descri:Optional[str] = None
    price :float =30000
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
    
#利用Query設定參數限制
@app.get("/limit the length")
async def limit_length(input:str=Query(default=None,min_length=3,max_length=8)):
    result = "input = "+input
    return result

#-----------------------------分界線(Boundary) Between app and app1----------------------------------#

@app1.get("/")
def root():
    return "Hello World!"


#查詢函數,可以逐步增加項數
@app1.get("/list")
async def L(q:list = Query(default = None,
                           alias= "Queue is me",
                           description= "This is a Queue")):
    queue_item = {"q":q}
    return queue_item


#可以逐步增加項的list ，並做運算，這邊即使有Body還是可以使用get，因為使用Query,Path等函數，不是直接使用類別，因此不會有錯。
@app1.get("/list1")
async def L(q:list = Query(default = None,
                           alias= "Queue is me",
                           description= "This is a Queue")):
    for items in q:
        if(items =="Leo"):
            re_value = items
    return re_value


#普通的List 好像無法直接用get函數，因此這邊使用put
@app1.put("/list2")
async def L2(q:List[int]=[]):
    return {"q ":q}

#Path使用於此參數有出現在路徑上，若沒有->報錯 Unprocessable Entity
@app1.get("/items/{item_id}")
async def read_items(
    item_id: int = Path(title="The ID of the item to get"),
    q: Union[str, None] = Query(default=None, alias="item-query")
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

#若不想要使用Query，設定沒有默認值的q，可以在最前面加上一個*
#此函數跟上面那段一模一樣
'''
@app.get("/items/{item_id}")
async def read_items(*, item_id: int = Path(title="The ID of the item to get"), q: str):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
'''

#查詢函數的限制，數字有四種可以用 gt(>),ge(>=),lt(<).le(<=) ，字串則可以使用min_length以及max_length

@app1.get("/int_limit")
async def Limit(
    *,num:int = Query(gt = 0,le=50000),name:str
):
    result = {"Money":str(num)}
    if(name) :result.update({"名字":name})
    return result
    
#-----------------------------分界線(Boundary) Between app1 and app2----------------------------------#
@app2.get("/")
def root():
    return "This is root"

@app2.put("/mixture")
async def Mixture(*,num:int,name:str,item:Item):
    return {"ID Number":num,"name":name,"Item ":item}

#Body函數，使得某參數也可以進入request Body，但不得用於路徑參數

@app2.put("/body")
async def update_item(item_id: int = Body(), item: Item = Body(embed=True)):
    results = {"item_id": item_id, "item": item}
    return results

#Fidle函數，是查詢函數，可以用於之前宣告過的class
class Item3(BaseModel):
    name: str
    description: Union[str, None] = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: Union[float, None] = None


@app2.put("/items3/{item_id}")
async def update_item(item_id: int, item: Item = Body(embed=True)):
    results = {"item_id": item_id, "item": item}
    return results



### Multiple structure 
class Student(BaseModel):
    name:str = "Leo" 
    id:int = 13

class Classroom(BaseModel):
    grade:int = 4
    room:int = 8
    student:List[Student]
    
class School(BaseModel):
    region:str ="Taoyuan"
    classroom:List[Classroom]
    

##可以建立multiple structure
@app2.put("/multiple_structure")
def Structure(school:School =None):
    for item in school.classroom:
        if item.grade == 4:
            result = item
    return result

##修改schema的方法 1.使用class config 2.利用Body = example = {....} 3. 直接設定初值
class Example(BaseModel):
    name:str
    telephone:str
    sex:str
    
    class Config:
        schema_extra = {
            "example":{
                "name":"Leo",
                "telephone":"09569708**",
                "sex":"male"
            }
        }

@app2.put("/extra_example")
def example(people:Example):
    return people


@app2.put("/extra_example2")
def example(people:Example =Body(
    example={
        "name":"Elsa",
        "telephone":"09209708**",
        "sex":"female"
    }
)):
    return people


#-----------------------------分界線(Boundary) Between app2 and app3----------------------------------#

  
'''
@app.get("/file/{filepath:path}")
def Get(filepath:str):
    return {"filepath":filepath}   
''' 