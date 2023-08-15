from prefect import flow,get_run_logger
from request import *
import logger
from configs import *
# 禁用不安全請求警告

url0 = 'http://140.96.111.93:8000/plot_all'
input = 'excel'


@flow
def Plot():
    prelog = get_run_logger()
    prelog.setLevel("DEBUG")
    url = url0 + f"?input={input}"
    
    mylog.info("Enter Flow : Plot()")
    prelog.info("Enter Flow : Plot()")
    prelog.debug("Enter File_request()")
    prelog.debug(f"url = {url}")
    
    output = File_request(url)
    
    prelog.debug("Finish Post Requsest Function")
    prelog.debug(f"Get response:\n{output}")
    mylog.debug("Finish Plot()")
    
if __name__ == "__main__":
    Plot()