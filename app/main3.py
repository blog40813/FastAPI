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


@app.get("/openapi.json")
def get_open_api_endpoint():
    return get_openapi(title="Your API Title", version="1.0.0", routes=app.routes)

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
app.mount("/sta", StaticFiles(directory="D:\exercise\sta"), name="sta")

@app.get("/")
async def root():
    return {"message": "Hello World!!!"}

# 指定 api 路徑 @app.函數(路徑)
#可以藉由Optional或是設置初值為None讓變數成為可選參數

@app.get("/users/{user_id}") 
def read_user(user_id: int, q: Optional[str] = None):
    return {"user_id": user_id, "q": q}
