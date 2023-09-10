from fastapi import APIRouter,Depends
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional

items = APIRouter()
#from application import main,logger
import main,logger
from . import user
import json


#每個函數的路徑不能為空
mylog = logger.log("Item Function Logs")
t = "\""

debug_msg:str
#123
#我我

@items.get("/name")
async def get_info(phone_number:str ,name:str):
    
    mylog.info("----------name function--------")
    mylog.debug("input : phone_number = "+phone_number + " name = "+name)
    
    debug_msg = "output : \n" + json.dumps({"Username":name,"telephone":phone_number})+"\n"
    mylog.debug(debug_msg)
    
    return {"Username":name,"telephone":phone_number}



@items.get("/items/Your_name")
async def Name(name:str):
    mylog.info("----------/items/Your_name--------")
    mylog.debug("input :"+name)
    debug_msg = "output : \n" +"Hello " + name + ", Myname is Leo, Nice to meet you..." +"\n"
    mylog.debug(debug_msg)
    return {"Hello " + name + ", Myname is Leo","Nice to meet you..."}

#可以利用引用其他文件，使用函數跟authorize的功能




#這邊使用response_class = HTMLResponse只是因為希望可以正確應用到換行符號
@items.get("/secert",response_class=HTMLResponse)
async def Secret(User:user.User = Depends(user.get_current_active_user)):
    output = "Hello " + User.username + ", Myname is Leo.\n"+"Nice to meet you.\n"+"My faviorate dessert is chocolate brownie!\n"+"Don't tell anyone!!!!!!\n"
    
    mylog.info("----------secret--------")
    mylog.debug("input :"+User.username)
    debug_msg = "output : \n" + output+"\n"
    mylog.debug(debug_msg)
    
    return output
        

'''-----------------------2023/05/30 version-----------------------'''




