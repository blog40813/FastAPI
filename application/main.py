from fastapi import FastAPI,Query,Path,Body,Header,HTTPException,Depends,status,responses
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import datetime
from datetime import timedelta,datetime
#from fastapi.openapi.docs import get_swagger_ui_html
#from fastapi.openapi.utils import get_openapi

from routers.user import user
from routers.init_web import web
from routers.item import items
from routers.classes import classes
from routers.file import handlefile
from routers.function import funct
from routers.chart import chart
import logger
import os

#把items下寫的功能都import進來，可以執行
#但路徑不能為空123

import sys
pwd = os.path.dirname(os.getcwd())
sys.path.append(pwd)


#在下面的code裡面，tags就是大標題，所有從這邊include進來的函數最上面會有大標作區段
app = FastAPI()

sta_path = os.path.join(pwd,"sta")
#目前設置http credential的方法只看到可以使用在有app裡面

mylog = logger.log("Main Function")

'''-------------------------------------------'''
##123
##456 
import secrets
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

ACCESS_TOKEN_EXPIRE_MINUTES = 30

##進入網頁之前需要驗證的code
async def get_current_username(*,credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "user")
    correct_password = secrets.compare_digest(credentials.password, "password")

    if not (credentials.username and credentials.password):
        mylog.debug("Incorrect email or password")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
        
    mylog.info("------------get_current_username function-----------")
    mylog.debug("input username:"+credentials.username)
    mylog.debug("input password:"+credentials.password)
    mylog.debug("output(credential.username):"+credentials.username+"\n")
    
    return credentials.username
    
app = FastAPI(docs_url=None, redoc_url=None, openapi_url = None)
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

@app.get("/openapi.json", include_in_schema=False)
async def openapi(username: str = Depends(get_current_username)):
    
    mylog.info("------------Open Web-----------\n")
    
    return get_openapi(title = "FastAPI", version="0.1.0", routes=app.routes)
#include_in_schema是指要不要把此函數顯現在網頁上

'''-------------------------------------------'''
'''
@app.middleware("http")
async def authorize_request(request, call_next):
    if request.url.path == "/":
        # 如果請求的是登錄路由，直接繼續處理
        return await call_next(request)

    credentials = security.__call__(request)
    if not credentials:
        # 如果無法驗證憑據，返回未授權的錯誤
        raise HTTPException(status_code=401, detail="Unauthorized")

    if not get_current_username(credentials = credentials):
        # 如果驗證使用者失敗，返回未授權的錯誤
        raise HTTPException(status_code=401, detail="Unauthorized")

    # 檢查授權時間限制
    current_time = datetime.now()
    #expiration_time = datetime(2023, 6, 1, 0, 0, 0)  # 假設授權有效期至 2023 年 6 月 1 日
    expiration_time = datetime.now() + timedelta(seconds=30)
    if current_time > expiration_time:
        # 如果授權已過期，返回未授權的錯誤
        raise HTTPException(status_code=401, detail="Authorization expired")

    # 授權通過，繼續處理請求
    response = await call_next(request)
    return response
'''

@app.get("/do",tags=["Main"])
async def root():
    
    mylog.info("--------------do function-----------")
    mylog.debug("output = Hello, Welcome to my FastAPI\n")
    return "Hello, Welcome to my FastAPI"

app.include_router(items,tags=["Items"])
app.include_router(web,tags=["Web"])
app.include_router(user,tags=["User"])
app.include_router(classes,tags=["Class"])
app.include_router(funct,tags=["Function"])
app.include_router(handlefile,tags=["Files"])
app.include_router(chart,tags=["Chart"])



# 将静态文件夹路径指向 Swagger UI 的文件夹路径
#put the needed file to sta (index.jsx/swagger-ui.css/swagger-ui-bundle.js/swagger-ui-standalone-preset.js)
app.mount("/sta", StaticFiles(directory="./../sta"), name="sta")


"---------------------------2023/05/30 version import function from other .py file ------------------------------"