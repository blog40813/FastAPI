from typing import Optional
from typing import List,Union,Any
from fastapi import FastAPI,Query,Path,Body,Header,HTTPException,Depends
from enum import Enum
from typing import Dict
from pydantic import BaseModel,Field,EmailStr
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
import json
from jose import JWTError, jwt
from passlib.context import CryptContext


app =  FastAPI()
app1 = FastAPI()
app2 = FastAPI()
app3 = FastAPI()
app4 = FastAPI()


#進入網頁第一個程式

@app.get("/")
async def root():
    return {"message": "Hello World!!!"}


# 指定 api 路徑 @app.函數(路徑)
#可以藉由Optional或是設置初值為None讓變數成為可選參數

@app.get("/users/{user_id}") 
def read_user(user_id: int, q: Optional[str] = None):
    return {"user_id": user_id, "q": q}

#Diction的應用
#這邊雖然前面key的值是int 但輸入的時候還是要有"

@app.put("/Dict")
def Dictionary(Type:Dict[int,int]):
    return {str(Type[11])+" "+str(Type[40813])}


#這邊使用put的原因為：get函數不能使用request body進行傳輸
@app.put("/L_Sum")
def List_Sum(L:List[int]=[1,2,3], sum:int=0):
    for item in L:
        sum += item
    result = "L_sum"+" = "+str(sum)
    return result

#解決方法，將List做為查詢函數傳遞
#L_Sum_Query?L=1&L=2&L=3&sum=1516利用網址進行取用
#有些type是沒辦法用Query的方法 用get進行取用ㄉ。 example:dict的型態，class的型態

@app.get("/L_Sum_Query")
def List_Sum(L:List[int]=Query(default=[1,2,3]), sum:int=0):
    for item in L:
        sum += item
    result = "L_sum"+" = "+str(sum)
    return result



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



#若是要使用先前建立過的class，要先from pydantic import BaseModel
#class宣告時也要使用 class 名稱(BaseModel)才能用post、put...建立class



class Item(BaseModel):
    name:str = "Leo"
    descri:Optional[str] = None
    price :float = 30000
    tax:int=0

class test(BaseModel):
    subject:str
    score:float


test2:test ={"science",55}


#兩個藉由API創建 Class item 的應用


##注意這邊有問題的是，dict類型不能放在一個list裡面進行輸出
@app.post("/Create_Item")
async def Create(item:Item):
    item_dict = item.dict()
    if item.tax:
        money = item.price*0.9
        item_dict.update({"money":money})
        #my_json = tuple(item_dict)
        
    if(item.price<2000) :
        return ["生活費 = " + str(item.price) + " 小於2000 -> 生活拮据",item_dict]
    if (item.price>20000):
        return {"生活費 = " + str(item.price) +  " 大於20000 -> 生活富足",item_dict}
    else:
        #return {"生活費 = " + str(item.price),item_dict}
        return item_dict


@app.post("/item_test/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


@app.post("/Midterm")
async def Midterm(record:test ):
    if (record.score >= 60) :
        return {"及格了，分數是 " :  record.score}
    else:
        return {"Fail，分數是 " : record.score}
    


#利用Query設定參數限制 ，查詢函數的限制，數字有四種可以用 gt(>),ge(>=),lt(<).le(<=) ，字串則可以使用min_length以及max_length
@app.get("/limit_the_length")
async def limit_length(input:str=Query(default=None,min_length=3,max_length=8,alias="My input string",description="Hi")):
    result = "input = "+input
    return result


#-----------------------------分界線(Boundary) Between app and app1----------------------------------#

@app1.get("/")
def root():
    return "Hello World!"


#使用Query,Path等函數，不是直接使用類別，因此不會有錯。
#Alias 更改的是左半部參數名稱，Description 是右半部的敘述
@app1.get("/list1")
async def L(q:list = Query(default = None,
                           alias= "Queue is me",
                           description= "This is a Queue")):
    for items in q:
        if(items =="Leo"):
            re_value = items
    return re_value


#Path使用於此參數有出現在路徑上，若沒有->報錯 Unprocessable Entity
#路徑參數不能給別名，會找不到value
#Path函數也可以增加限制  gt(>),ge(>=),lt(<).le(<=) ，字串則可以使用min_length以及max_length
#不使用Query的原因是：對於路徑參數是無法使用Query的

@app1.get("/items/{item_id}")
async def read_items(
    item_id: int = Path(title="The ID =",alias="item_id",description="this is id",le=500),
    q: Union[str, None] = Query(default=None, alias="item-query")
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results



#若不想要使用Query，設定沒有默認值的查詢函數q，可以在最前面加上一個*
#此函數跟上面那段一模一樣
'''
@app.get("/items/{item_id}")
async def read_items(*, item_id: int = Path(title="The ID of the item to get"), q: str):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
'''

#-----------------------------分界線(Boundary) Between app1 and app2----------------------------------#
@app2.get("/")
def root():
    return "This is root"



@app2.put("/mixture")
async def Mixture(*,num:int,name:str,item:Item):
    return {"ID Number":num,"name":name,"Item ":item}




#Body函數，使得某參數也可以進入request Body，但不得用於路徑參數
#也就是說：原本會以上方格子形式輸入的參數，可以從下面Request Body的格子輸入

@app2.put("/body")
async def update_item(item_id: int = Body(), item: Item = Body(embed=True)):
    results = {"item_id": item_id, "item": item}
    return results




#Field函數，是查詢函數，可以用於之前宣告過的class
class Item3(BaseModel):
    name: str
    description: Union[str, None] = Field(
        default=None, title="The description of the item", max_length=300,example = "1323"
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: Union[float, None] = None




@app2.put("/items3/{item_id}")
async def update_item(item_id: int, item3: Item3 = Body(embed=True)):
    results = {"item_id": item_id, "item": item3}
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
def example(people:Example = Body(
    example={
        "name":"Elsa",
        "telephone":"20569708**",
        "sex":"female"
    }
)):
    return people


#-----------------------------分界線(Boundary) Between app2 and app3----------------------------------#


from datetime import datetime,time,timedelta
from uuid import UUID

@app3.get("/")
def root():
    return "Hello!"

#Header 的使用
#下面這個例子也跟Query一樣可以逐步增加函數

@app3.get("/items/")
async def read_items(x_token: Union[List[str], None] = Header(default=None)):
    return {"X-Token values": x_token}



##Response Model = ...
#會將輸出限制在模型的定義內，輸出內容會是response model 的形式，若有修改，內容也會跟著改
#總而言之，就是會過濾掉不屬於response model 裡面定義過的參數的地方

@app3.post("/C_item/", response_model=Item)
async def create_item(item: Item) -> Any:
    return {"name":"Leooooooo" , "HELO":"ME"}


@app3.get("/R_item/", response_model=List[Item])
async def read_items() -> Any:
    return [
        {"name": "Portal Gun", "price": 42.0},
        {"name": "Plumbus", "price": 32.0},
    ]
    


##Extra Example
#在下面這個例子當中，User裡面能輸出的值並不包含password
class User_in(BaseModel):
    username:str 
    password:str
    email:EmailStr 
    full_name   :Union[str,None] = None
    
class User_out(BaseModel):
    username:str
    email:EmailStr 
    full_name : Union[str,None] = None



##若不使用response model 也可已將箭頭後面改成要限制的response model，但若兩個同時存在，則會使用response model

@app3.post("/user/",response_model=User_out)
async def create_user(user: User_in) -> User_in:
    return user

#response_model_exclude_unset = True :如果沒有設置的話，就不會return，但如果是一開始就有設置初值的話，還是return
#response_model_exclude_default = True : 如果是default值->就不會return
#response_model_exclude_None = True : 如果是 None ->不會return



#這邊這個例子對於 default 好像沒有用，因為中間有經過一個轉換，且中間有必須填入的函數
'''
@app3.post("/exclude_default",response_model=User_out,response_model_exclude_default=True)
async def exclude_default(user:User_in):
    return user

#因此這邊提供另一個
@app3.post("/exclude_default",response_model=User_in,response_model_exclude_defaults=True)
async def exclude_default(user:User_in):
    return user
'''



## response_model_exclude={"name","email"}  等同於 response_model_exclude = ["name","email"]
## 因為 list 會自動轉換成 set



##多層函數

class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: Union[str, None] = None
    #password :str


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


##**user_in.dict() = 解碼，會將這個dictionary的key作為變數名稱，value作為值，傳遞進物件裡面，若是另一個物件沒有key，則值不會被傳遞過去

def fake_save_user(user_in: User_in):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password = hashed_password)
    print("User saved! ..not really")
    return user_in_db

@app3.post("/secret/"''',response_model = User_out''')
async def create_secret_user(user_in: User_in):
    user_saved = fake_save_user(user_in)
    return user_saved




###可以利用UserBase的方式建立資料，這樣重複的資料就不用建立兩次，有點像inherient class，且執行結果會等同於上面這段code

'''
class UserBase(BaseModel):
    username:str
    email:EmailStr
    fullname:Union[str,None] = None
    
class UserIn(UserBase):
    password : str
    
class Userout(UserBase):
    pass
    
class UserINDB(UserBase):
    hashed_password:str

'''

###response_model可以利用Union，使得輸出可以有不同種類型
##for example    response_model = [Union UserINDB , Userout]
##但要注意的是，類型變數較多(較詳細)的類型要放在前面。
 
 
 
 
 ##response status code ，但不知道為何，輸入值還是會return 只是status code是 404 not found，然後測試發現從網址access的方法 只有get能用?，或是有其他方法
@app3.get("/test_status",status_code=404)
async def status(item:int):
    return item




#-----------------------------分界線(Boundary) Between app3 and app4----------------------------------#
from fastapi import Form,File,UploadFile

@app4.get("/")
def root():
    return "Hi,This is the root page!"


##如何導入表單



#如何上傳文件，下列是兩種可以上傳文件的方法
#file會作為表單數據上傳


#此方法會將檔案已bytes的形式讀取、接收
#會把所有內容放在內存，適合小型文件
@app4.post("/login")
async def login(username : str = Form() , password : str = Form()):
    return {"username":username}


@app4.post("/files/")
async def create_file(file: bytes = File()):
    return {"file_size": len(file)}

#uploadfile比起file的優勢
#當儲存在內存空間(ROM，cache)的文件超出上限的時候，會將檔案放在硬碟裡面
#因此更適合處理圖片、影片、二進制文件，也不會佔用所有內存空間
#file like接口?可以open read write

#這邊read 要用await是因為我們在def的時候是使用async
#若不是async 可以直接用file.read()
#若是要使用readline 就用file.file.readline()

@app4.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    # inp = await file.read()
    input = file.file.readline()
    return {"filename": file.filename,"input":input}


#方法可以混用，目前還沒研究為甚麼要這樣，但可以加上description
@app4.post("/uploadfile2/")
async def create_upload_file(
    file: UploadFile = File(description="A file read as UploadFile"),
):
    return {"filename": file.filename}


@app4.post("/mul_files/")
async def create_files(files: list[bytes] = File()):
    return {"file_sizes": [len(file) for file in files]}


@app4.post("/mul_uploadfiles/")
async def create_upload_files(files: list[UploadFile]):
    return {"filenames": [file.filename for file in files]}


'''2023/05/19--version'''



#HTTP exceptrion handling

chk_list = ["my","favorite","fruit","is","the","banana","and","the","apple","?"]

@app4.get("/exception")
async def Exception(check:int):
    if check > chk_list.count:
        raise HTTPException(status_code=404,detail="pool you!")
    return {"item = ":chk_list[check]}




####################################################################################
####################################################################################
####################################################################################



#密碼相關
#這邊這個oauth2使得後端或是API可以獨立於對用戶進行身分驗證的服務器，URL是相對路徑(接收URL作為參數)
oauth2_scheme1 = OAuth2PasswordBearer(tokenUrl="token1")
#以這個例子來說，要前端要取用password這個功能之前要先進行身分驗證，而這個驗證的路徑就會是上面的tokenUrl(相對路徑，並為Post請求，也就是會引用/token)
#而oauth2會接收一個str類型的token(身分驗證通過後會給的令牌)，方便下次帶這個token就可以通過身分驗證，其有一定的過期時間，過期後要重新驗證。

@app4.get("/password")
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
'''
async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
'''
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


@app4.post("/token1")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db1.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app4.get("/users/me1")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user   

####################################################################################
####################################################################################
####################################################################################

#利用openssl rand -hex 32 來生成我們的 secret key
#01db80dacb3ba76233a60cf626346f4921205a29f4f7a6bccd05826e3f6f440e
#Algorithm = 加密的算法
#最下面的是設置令牌過期的時間
SECRET_KEY = "01db80dacb3ba76233a60cf626346f4921205a29f4f7a6bccd05826e3f6f440e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

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

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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


@app4.post("/token", response_model=Token)
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


@app4.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app4.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]

'''2023/05/23--version (unfinished)'''


##可以使用額外數據類型

'''
@app3.put("/extra_data_type")
def Extra_Data_Type(
    item_id:UUID,
    start_datetime:datetime = None,
    end_datetime:datetime = None,
    repeat_at:time =None,
    process_after:timedelta =None
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return{
        "item_id":item_id,
        "start_datetime":start_datetime,
        "end_datetime":end_datetime,
        "repeat_at" : repeat_at,
        "process_afterr" :process_after,
        "start_process" : start_process,
        "duration" : duration
    }
    

'''
##Cookie使用
from fastapi import Cookie,Response
'''
@app3.get("/Cookie")
def Cookie_test(ads_id:str =Cookie(default = None)):
    return {"ads_id":ads_id}


@app3.post("/cookie-and-object/")
def create_cookie(response: Response):
    response.set_cookie(key="fakesession", value="fake-cookie-session-value")
    return {"message": "Come to the dark side, we have cookies"}
'''
'''
@app.get("/file/{filepath:path}")
def Get(filepath:str):
    return {"filepath":filepath}   
''' 