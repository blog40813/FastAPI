
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
    a = output.text
    mylog.debug(f"Get response:\n{a}")
    return a
        
    