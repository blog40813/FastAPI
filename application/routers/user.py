from fastapi import APIRouter,Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from typing import Union
from pydantic import BaseModel
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import Union
from fastapi import FastAPI
from datetime import datetime, timedelta
import json

user = APIRouter()

#import sys
#sys.path.append("D:\Fastapi\exercise\\application")

import logger
mylog = logger.log("User Function")
#密碼相關
#這邊這個oauth2使得後端或是API可以獨立於對用戶進行身分驗證的服務器，URL是相對路徑(接收URL作為參數)
t = "\""

'''


oauth2_scheme1 = OAuth2PasswordBearer(tokenUrl="token1")
#以這個例子來說，要前端要取用password這個功能之前要先進行身分驗證，而這個驗證的路徑就會是上面的tokenUrl(相對路徑，並為Post請求，也就是會引用/token)
#而oauth2會接收一個str類型的token(身分驗證通過後會給的令牌)，方便下次帶這個token就可以通過身分驗證，其有一定的過期時間，過期後要重新驗證。

ACCESS_TOKEN_EXPIRE_MINUTES = 30

@user.get("/password")
async def read_items(token: str = Depends(oauth2_scheme1)):
    return {"token1": token}

#獲取當前用戶

class User(BaseModel):
    username:str
    email:Union[str,None] = None
    full_name :Union[str,None] = None
    disabled :Union[bool,None] = None

def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )


#DATA BASE FOR USER
fake_users_db1 = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
    "Leo": {
        "username": "Leo",
        "full_name": "Fat Xiang",
        "email": "Leo@example.com",
        "hashed_password": "fakehashed40813",
        "disabled": False,
    },
}

def fake_hash_password(password: str):
    return "fakehashed" + password


class UserInDB(User):
    hashed_password: str
    
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    
#原始代碼沒有辦法產生Inactive user的訊息，因為在fake_decoder_token中，disable = None

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_user(token: str = Depends(oauth2_scheme1)):
    user_dict = fake_users_db1[token]
    user = UserInDB(**user_dict)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user





@user.post("/token1",include_in_schema=False)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db1.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@user.get("/users/me1")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user   


'''

'''-----------------------2023/05/30 version-----------------------'''






SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



@user.get("/password")
async def read_items(token: str = Depends(oauth2_scheme)):
    
    mylog.info("---------password function--------------")
    mylog.debug("input : " + token)
    debug_msg = "output: "+ json.dumps({"token1": token})
    mylog.debug(debug_msg+"\n")
    
    return {"token1": token}



def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@user.post("/token", response_model=Token ,include_in_schema=False)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}



@user.get("/users/me1")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    
    debug_msg = json.dumps(current_user.dict())+"\n"
    mylog.info("----------------users/me1 function -------------")
    mylog.debug("output:\n"+debug_msg)
    return current_user   
