from fastapi import APIRouter,Depends
from fastapi.responses import HTMLResponse

items = APIRouter()
from . import user

#每個函數的路徑不能為空

@items.get("/name")
async def get_info(phone_number:str ,name:str):
    return {"Username":name,"telephone":phone_number}

@items.get("/items/Your_name")
async def Name(name:str):
    return {"Hello " + name + ", Myname is Leo","Nice to meet you..."}

#可以利用引用其他文件，使用函數跟authorize的功能


#這邊使用response_class = HTMLResponse只是因為希望可以正確應用到換行符號
@items.get("/secert",response_class=HTMLResponse)
async def Secret(User:user.User = Depends(user.get_current_user)):
    output = "Hello " + User.username + ", Myname is Leo.\n"+"Nice to meet you.\n"+"My faviorate dessert is chocolate brownie!\n"+"Don't tell anyone!!!!!!\n"
    return output
        

'''-----------------------2023/05/30 version-----------------------'''




