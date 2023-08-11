from prefect import flow,get_run_logger
from request import Post_request
import logger
from configs import *
# 禁用不安全請求警告


url1 = 'https://140.96.111.164:5998/setJsonProfile_Async'

input1 = {
  "after_col_value": "4,4,4,2,4,2,3,3",
  "csv_name": "newprofile",
  "dataitem": "id",
  "datatype": "string,string,string,string,string,string,string,string",
  "gen_qi_settingvalue": "4,4*千,3",
  "isNull": "N,Y,Y,N,N,Y,N,N",
  "minKvalue": "3",
  "pro_col_cht": "id,age,workclass,fnlwgt,education,education_num,marital_status,occupation",
  "qi_col": "fnlwgt-1,education_num-2",
  "tablekeycol": "id,marital_status,occupation"
}

url2 = 'https://140.96.111.164:5998/MacHash_Async'

input2 = {
  "columns_mac": "123",
  "hashTableName": "adult_id",
  "hashkey": "BASRsdfs456465",
  "pname": "DeId_adult_machash_test",
  "prodesc": "describe: DeId-project with hash on adult dataset.",
  "projName": "DeId_adult_machash_test",
  "sep": "^|"
}

url3 = 'https://140.96.111.164:5998/getReport_Sync'

input3 = {
  "projName": "2QDataMarketDeId"
}


mylog = logger.log("Flow")

url = url3
input = input3

@flow
def Call_api():
    prelog = get_run_logger()
    prelog.setLevel("DEBUG")
    
    mylog.info("Enter Flow : Call_api()")
    prelog.info("Enter Flow : Call_api()")
    prelog.debug("Enter Post_Request()")
    prelog.debug(f"url = {url}")
    prelog.debug(f"input={input}")
    
    
    output = Post_request(url,input)
    
    
    prelog.debug("Finish Post Requsest Function")
    prelog.debug(f"Get response:\n{output}")
    mylog.debug("Finish Call_api()")
    
if __name__ == "__main__":
    Call_api()