
import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning
import json
import os
import datetime
from datetime import datetime


import logger
from configs import *

mylog = logger.log("Function")


urllib3.disable_warnings(InsecureRequestWarning)

def Post_request(url,input):
    mylog.info("Enter Post Requsest Function")
    mylog.debug(f"url = {url}")
    mylog.debug(f"input={input}")
    output = requests.post(url,json=input,verify=False)
    response_text = json.loads(output.text)
    response_text = json.dumps(response_text,indent=2,ensure_ascii=False)
    mylog.debug(f"Get response:\n{response_text}")
    return response_text
        
def File_request(url):
    mylog.info("Enter File Requsest Function")
    mylog.debug(f"url = {url}")
    
    output = requests.post(url,verify=False)
    print (output.text)
    response_text = json.loads(output.text)
    response_text = json.dumps(response_text,indent=2,ensure_ascii=False)
    mylog.debug(f"Get response:\n{response_text}")
    return response_text
