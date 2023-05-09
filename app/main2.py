from fastapi import FastAPI,Query
from typing import List,Union

app = FastAPI()

@app.get("/")
def root():
    return "Hello World!"


#查詢函數
@app.get("/list")
async def L(q:list = Query(default = None,
                           alias= "Queue is me",
                           description= "This is a Queue")):
    queue_item = {"q":q}
    return queue_item

