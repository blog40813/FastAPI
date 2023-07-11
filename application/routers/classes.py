from fastapi import APIRouter,Depends
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional,List

classes = APIRouter()
#from application import main,logger
import main,logger
from . import user
import json


mylog = logger.log("Class Function Logs")
t = "\""

debug_msg:str



class Item(BaseModel):
    name:str = "Leo"
    descri:Optional[str] = None
    price :float = 30000
    tax:int=0
    
    def __str__(self) -> str:
        return f"Item:{self.name}, description : {self.descri}, price : {self.price}, tax : {self.tax}"

class test(BaseModel):
    subject:str
    score:float
    
    def __str__(self) -> str:
        return f"Subject : {self.subject}  Score : {self.score}"


test2:test ={"science",55}



#兩個藉由API創建 Class item 的應用
##注意這邊有問題的是，dict類型不能放在一個list裡面進行輸出
@classes.post("/Create_Item")
async def Create(item:Item):
    
    mylog.info("----------/Create_Item--------")
    mylog.debug("input :"+ str(item))
    
    item_dict = item.dict()
    if item.tax:
        money = item.price*0.9
        mylog.debug("money(tax) :" + item.price + "*0.9  = " + money)
        item_dict.update({"money":money})
        #my_json = tuple(item_dict)
        
    if(item.price<2000) :
        
        mylog.debug("output = 生活費 = " + str(item.price) + " 小於2000 -> 生活拮据 "+str(item_dict)+ "\n")
        return {"生活費 = " + str(item.price) + " 小於2000 -> 生活拮据 "+str(item_dict)}
    
    if (item.price>20000):
        
        mylog.debug("output = 生活費 = " + str(item.price) + " 大於20000 -> 生活富足 "+str(item_dict)+ "\n")
        return {"生活費 = " + str(item.price) +  " 大於20000 -> 生活富足 "+str(item_dict)}
    
    else:
        
        mylog.debug("output = 生活費 = " + str(item.price)+" " +str(item_dict)+ "\n")
        return {"生活費 = " + str(item.price)+" "+str(item_dict)}



@classes.post("/Midterm")  
async def Midterm(record:test ):
    mylog.info("----------/Midterm--------")
    mylog.debug("input :"+ str(record))
    
    if (record.score >= 60) :
        
        mylog.debug(f"output = 及格了，分數是 : {record.score}\n")
        return {"及格了，分數是 " :  record.score}
    else:
        mylog.debug(f"output = Fail，分數是 : {record.score}\n")
        return {"Fail，分數是 " : record.score}
    
    
    
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
@classes.put("/multiple_structure")
def Structure(school:School =None):
    mylog.info("----------------multiple_struct function-------------")
    mylog.debug("input = "+str(school))
    
    for item in school.classroom:
        if item.grade == 4:
            result = item
    
    mylog.debug("output = "+str(result)+"\n")
    return result


##修改schema的方法 1.使用class config 2.利用Body = example = {....} 3. 直接設定初值
##下面提供了幾種可以修改schema裡面內容的code

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

@classes.put("/extra_example")
def example(people:Example):
    mylog.info("----------------extra_example function-------------")
    mylog.debug("input = "+str(people))
    mylog.debug("output = "+str(people)+"\n")
    return people

