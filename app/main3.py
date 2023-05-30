from typing import Optional
from typing import List,Union,Any
from fastapi import FastAPI,Query,Path,Body,Header,HTTPException,Depends,status
from enum import Enum
from typing import Dict
from pydantic import BaseModel,Field,EmailStr
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
import json
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.openapi.docs import get_swagger_ui_html,get_swagger_ui_oauth2_redirect_html
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse,HTMLResponse,JSONResponse
import json





app =  FastAPI()


##################################一進入頁面就需要輸入帳號密碼###############################


import secrets
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "user")
    correct_password = secrets.compare_digest(credentials.password, "password")
    if not (credentials.username and credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

app = FastAPI(docs_url=None, redoc_url=None, openapi_url = None)

from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
'''
@app.get("/docs", include_in_schema=False)
async def get_documentation(username: str = Depends(get_current_username)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")
'''

@app.get("/openapi.json", include_in_schema=False)
async def openapi(username: str = Depends(get_current_username)):
    return get_openapi(title = "FastAPI", version="0.1.0", routes=app.routes)

#include_in_schema是指要不要把此函數顯現在網頁上

#######################################################################################

"""2023/05/30 version"""

origins = [
    "http://140.96.83.18.tiangolo.com",
    "https://140.96.83.18.tiangolo.com",
    "http://140.96.83.18",
    "http://140.96.83.18:8000",
    "http://140.96.83.18:8000/docs",
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
    "http://172.20.149.54:56795"
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

'''
@app.get("/openapi.json")
def get_open_api_endpoint():
    return get_openapi(title="Your API Title", version="1.0.0", routes=app.routes)
'''


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>FastAPI Swagger UI</title>
        <link rel="stylesheet" type="text/css" href="/sta/swagger-ui.css">
        <script src="/sta/swagger-ui-bundle.js"></script>
        <script src="/sta/swagger-ui-standalone-preset.js"></script>
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script>
            const ui = SwaggerUIBundle({
                url: "/openapi.json",
                dom_id: "#swagger-ui",
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIStandalonePreset
                ],
                layout: "BaseLayout"
            })
        </script>
    </body>
    </html>
    """



# 将静态文件夹路径指向 Swagger UI 的文件夹路径
#put the needed file to sta (index.jsx/swagger-ui.css/swagger-ui-bundle.js/swagger-ui-standalone-preset.js)
app.mount("/sta", StaticFiles(directory="D:\exercise\sta"), name="sta")

@app.get("/")
async def root():
    return {"message": "Hello World!!!"}

# 指定 api 路徑 @app.函數(路徑)
#可以藉由Optional或是設置初值為None讓變數成為可選參數

@app.get("/users/{user_id}") 
def read_user(user_id: int, q: Optional[str] = None):
    return {"user_id": user_id, "q": q}


##2023/05/26 External visit for fastapi success 
#need to use ipconfig to know the open IP
#need to set port 8000 open (開啟防火牆設定新增)
#need to down load some file from swagger ui (zip)
#put the needed file to static (index.jsx/swagger-ui.css/swagger-ui-bundle.js/swagger-ui-standalone-preset.js)