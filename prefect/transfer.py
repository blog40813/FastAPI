from prefect import flow,get_run_logger
from request import *
import logger
from configs import *
# 禁用不安全請求警告

url = 'http://140.96.111.93:8000/usage_txt_to_csv_all'


@flow
def Excel():
    prelog = get_run_logger()
    prelog.setLevel("DEBUG")
    
    mylog.info("Enter Flow : Excel()")
    prelog.info("Enter Flow : Excel()")
    prelog.debug("Enter File_request()")
    prelog.debug(f"url = {url}")
    
    output = File_request(url)
    
    prelog.debug("Finish Post Requsest Function")
    prelog.debug(f"Get response:\n{output}")
    mylog.debug("Finish Call_api()")
    
if __name__ == "__main__":
    Excel()