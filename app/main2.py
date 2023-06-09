from typing import Optional
from typing import List,Union,Any
from fastapi import FastAPI,Query,Path,Body,Header,Cookie,Response,Form,File,UploadFile
from enum import Enum
from typing import Dict
from pydantic import BaseModel,Field,EmailStr
import json
from fastapi.responses import JSONResponse
import numpy as np


app =  FastAPI()
app1 = FastAPI()
app2 = FastAPI()
app3 = FastAPI()
app4 = FastAPI()


#進入網頁第一個程式

@app.get("/")
def hello():
    return "Hello! This is my fastapi!"

# 指定 api 路徑 @app.函數(路徑)
#可以藉由設置初值為None讓變數成為可選參數


@app.get("/users/{user_id}") 
def read_user(user_id: int, q: Optional[str] = None):
    return {"user_id": user_id, "q": q}


#Diction的應用
#這邊雖然前面key的值是int 但輸入的時候前後還是要有 "" 

@app.put("/Dict")
def Dictionary(Type:Dict[int,int]): 
    return {str(Type[11])+" "+str(Type[40813])}


#這邊使用put的原因為：get函數不能使用request body進行傳輸，正常來說普通的List函數是用request body進行傳遞的

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
def ENUM(hey:Model,de:Model):
    if hey is Model.alexnet:
        return {"A_Model ": hey ,"de_Model":de}
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
#class宣告時也要使用 class 名稱(BaseModel)才能用post、put...使用class

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
        return {"生活費 = " + str(item.price) + " 小於2000 -> 生活拮据",item_dict}
    if (item.price>20000):
        return {"生活費 = " + str(item.price) +  " 大於20000 -> 生活富足",item_dict}
    else:
        return {"生活費 = " + str(item.price),item_dict}
        return item_dict
        '''      

    if item.tax:
        if(item.price<2000) :
            return ["生活費 = " + str(item.price) + " 小於2000 -> 生活拮据",my_json]
        if (item.price>20000):
            return {"生活費 = " + str(item.price) +  " 大於20000 -> 生活富足",my_json}
        else:
            return {"生活費 = " + str(item.price),my_json}
        
    else:
        if(item.price<2000) :
            return ["生活費 = " + str(item.price) + " 小於2000 -> 生活拮据"]
        if (item.price>20000):
            return {"生活費 = " + str(item.price) +  " 大於20000 -> 生活富足"}
        else:
            return {"生活費 = " + str(item.price)}
            '''

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
    

#利用Query設定參數限制
#如果是int 有 gt(>),ge(>=),lt(<).le(<=) ，字串則可以使用min_length以及max_length
#alias 是可以更改頁面上左側變數顯示的名字，而description則是更改在input的格子上面的description

@app.get("/limit_the_length")
async def limit_length(input:str=Query(default=None,min_length=3,max_length=8,alias="My input string",description="Hi")):
    result = "input = "+input
    return result

@app.get("/limit_the_length_test")
async def limit_length(input:str=None):
    input += "4564"
    result = "input = "+input
    return result


#Path使用於此參數有出現在路徑上，若沒有->報錯 Unprocessable Entity
#路徑參數不能給別名，會找不到value
#路徑參數給default值是沒有用的
#Path函數也可以增加限制  gt(>),ge(>=),lt(<).le(<=) ，字串則可以使用min_length以及max_length
#不使用Query的原因是：對於路徑參數是無法使用Query的

@app.get("/path/{item_id}")
async def read_items(
    item_id: int = Path(title="The ID =",alias="item_id",description="this is id",le=100),
    q: Union[str, None] = Query(default=None, alias="item-query")
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

#若不想要使用Query，設定沒有默認值的q，可以在最前面加上一個*
#原本沒有default的變數是無法放在有default後面的，藉由加上一個*就可以了


'''

@app.get("/items/{item_id}")
async def read_items( *,item_id: int = Path(defalut = 156,title="The ID of the item to get"), q: str ):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results



@app.put("/mixture")
async def Mixture(*,num:int,name:str,item:Item):
    return {"ID Number":num,"name":name,"Item ":item}
'''



#Body函數，使得某參數也可以進入request Body，但不得用於路徑參數
#也就是說：原本會以上方格子形式輸入的參數，可以從下面Request Body的格子輸入
#如果原本就是一個class 使用body的函數，且embed = false ，request body裡面不會有變數名稱
#但若此時將embed = True 會有變數名稱的顯示

@app.put("/body")
async def update_item(item_id: int =Body(embed=True), item: Item = Body(embed=True)):
    results = {"item_id": item_id, "item": item}
    return results


#Field函數，也是查詢函數的一種，可以用於之前宣告過的class，讓class裡面的參數也有被限制，example的過程
#Query可以用在函數裡面，但是Field不能用在def那一行
#但title，description好像就沒有看到

class Item3(BaseModel):
    name: str
    description: Union[str, None] = Field(
        default=None, title="The description of the item", max_length=300,example = "1323"
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: Union[float, None] = None


@app.put("/items3/{item_id}")
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
@app.put("/multiple_structure")
def Structure(school:School =None):
    for item in school.classroom:
        if item.grade == 4:
            result = item
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

@app.put("/extra_example")
def example(people:Example):
    return people


@app.put("/extra_example2")
def example(people:Example = Body(
    example={
        "name":"Elsa",
        "telephone":"20569708**",
        "sex":"female"
    }
)):
    return people


'''
@app.get("/get_cookie/")
def read_cookie_info():
    content = {"message": "add cookie"}
    response = JSONResponse(content=content)
    response.set_cookie(key="session_info", value="xsxaxsafafa=fasfa=faafakfaslkfla;afsasfafafssda")
    return response


@app.get("/get_cookie/")
def read_cookie_info(response: Response):
    response.set_cookie(key="session_info", value="xsxaxsafafa=fasfa=faafakfaslkfla;afsasfafafssda")
    return {"message": "add cookie"}

@app.get("/cookie/")
async def read_items(ads_id: Union[str, None] = Cookie(default=None)):
    return {"ads_id": ads_id}
'''

#Header的使用，跟Query一樣可以逐項增加函數
#有不同的函數，像是轉換下畫線，但不確定用在哪裡

@app.get("/Header/")
async def read_items(x_token: Union[List[str], None] = Header(default=None,convert_underscores=True)):
    return {"X-Token values": x_token}

##Response Model = ...
#會將輸出限制在模型的定義內，輸出內容會是response model 的形式，若有修改，內容也會跟著改
#總而言之，就是會過濾掉不屬於response model 裡面定義過的參數的地方

###response_model可以利用Union，使得輸出可以有不同種類型
##for example    response_model = [Union UserINDB , Userout]
##但要注意的是，類型變數較多(較詳細)的類型要放在前面。

@app.post("/C_item/", response_model=Item)
async def create_item(item: Item) -> Any:
    return {"name":"Leooooooo" , "HELO":"ME"}


@app.get("/R_item/", response_model=List[Item])
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

@app.post("/user/",response_model=User_out)
async def create_user(user: User_in) -> User_in:
    return user
'''
@app.post("/user/",response_model=User_out,response_model_exclude_unset=True)
async def create_user(user: User_in) -> User_in:
    return user
'''

#response_model_exclude_unset = True :如果沒有設置的話，就不會return，但如果是一開始就有設置初值的話，還是return
#response_model_exclude_default = True : 如果是default值->就不會return
#response_model_exclude_None = True : 如果是 None ->不會return

##下面這行例子就是可以exclude超過一個項目
## response_model_exclude={"name","email"}  等同於 response_model_exclude = ["name","email"]
## 因為 list 會自動轉換成 set


#舉例來說，若是沒有設置full_name ，即使在class 裡面有fullname也不會顯示出來
#這邊這個例子對於 default 好像沒有用，因為中間有經過一個轉換，且中間有必須填入的函數




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

@app.post("/secret/"''',response_model = User_out''')
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

##response status code ，但不知道為何，輸入值還是會return 只是status code是 404 not found

@app.get("/test_status",status_code=404)
async def status(item:int):
    return item


##如何導入表單
#Content Type 不一樣(編碼 )
@app.post("/login")
async def login(username : str = Form() , password : str = Form()):
    return {"username":username}



#如何上傳文件，下列是兩種可以上傳文件的方法
#file會作為表單數據上傳


#此方法會將檔案已bytes的形式讀取、接收
#會把所有內容放在內存，適合小型文件
@app.post("/files/")
async def create_file(file: bytes = File()):
    return {"file_size": len(file)}

#uploadfile比起file的優勢
#當儲存在內存空間(ROM，cache)的文件超出上限的時候，會將檔案放在硬碟裡面
#因此更適合處理圖片、影片、二進制文件，也不會佔用所有內存空間
#file like接口?可以open read write

#這邊read 要用await是因為我們在def的時候是使用async
#若不是async 可以直接用file.read()
#若是要使用readline 就用file.file.readline()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    # inp = await file.read()
    input = file.file.readline()
    return {"filename": file.filename,"input":input}


#方法可以混用，目前還沒研究為甚麼要這樣，但可以加上description
@app.post("/uploadfile2/")
async def create_upload_file(
    file: UploadFile = File(description="A file read as UploadFile"),
):
    return {"filename": file.filename}


@app.post("/mul_files/")
async def create_files(files: list[bytes] = File()):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/mul_uploadfiles/")
async def create_upload_files(files: list[UploadFile]):
    return {"filenames": [file.filename for file in files]}



    

