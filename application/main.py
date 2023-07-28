from fastapi import FastAPI,Query,Path,Body,Header,HTTPException,Depends,status,responses
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import datetime
from datetime import timedelta,datetime

from routers.user import user
from routers.init_web import web
from routers.item import items
from routers.classes import classes
from routers.file import handlefile
from routers.function import funct
from routers.chart import chart
import logger
import os
from configs import *


import sys
sys.path.append(CURRENT_PATH)


#在下面的code裡面，tags就是大標題，所有從這邊include進來的函數最上面會有大標作區段
app = FastAPI()



mylog = logger.log("Main Function")

'''-------------------------------------------'''

import secrets
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

ACCESS_TOKEN_EXPIRE_MINUTES = 30


    
app = FastAPI(docs_url=None, redoc_url=None, openapi_url = None)
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi


'''
為了取得API的OpenAPI規範(Json格式)，使得Swagger UI 可以使用他來取得API相關資訊(get_openapi function)

'''
@app.get("/openapi.json", include_in_schema=False)
async def openapi():
    
    mylog.info("------------Open Web-----------\n")
    
    return get_openapi(title = "FastAPI", version="0.1.0", routes=app.routes)
#include_in_schema是指要不要把此函數顯現在網頁上



##進入網頁之前需要驗證的code

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


"將所有router include進app 使得router裡面的所有function可以使用 tag是到時候會顯現在Swagger UI上面的大標題"

app.include_router(items,tags=["Items"])
app.include_router(web,tags=["Web"])
app.include_router(user,tags=["User"])
app.include_router(classes,tags=["Class"])
app.include_router(funct,tags=["Function"])
app.include_router(handlefile,tags=["Files"])
app.include_router(chart,tags=["Chart"])



# 將靜態文件資料夾路徑指向Swagger UI的靜態文件資料夾
#put the needed file to sta (index.jsx/swagger-ui.css/swagger-ui-bundle.js/swagger-ui-standalone-preset.js)

'''
目的是讓FastAPI連接Swagger UI 的靜態文件 讓Swagger UI 可以正確顯示 API 文件
index.jsx ： Swagger UI的入口文件 用於呈現API文件的HTML結構 載入所需的CSS和JavaScripts文件
swagger-ui.css ： Swagger UI 的樣式表文件 美化、排版API文件內容 主要負責視覺體驗的部分
swagger-ui-bundle.js ： Swagger UI 的 JavaScript 包 包含所有Swagger UI 的核心功能跟模組 負責API規範的解析、渲染、互動功能
swagger-ui-standalone-preset.js ：
Swagger UI 的另一個 JavaScript 包 用於設定和配置Swagger UI 的選項及外觀 有許多自定義的選項 可以讓使用者根據需要調整Swagger UI的行為跟外觀

當我們綁定了靜態文件之後 進入網站時SwaggerUI會載入並渲染 嘗試向/openapi.json發出請求API規範
所以前面才要先定義一個/openapi.json的路徑(函數)
'''
app.mount("/sta", StaticFiles(directory="./../sta"), name="sta")


"---------------------------2023/05/30 version import function from other .py file ------------------------------"