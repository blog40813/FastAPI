import os

CURRENT_PATH = os.getcwd()
LOG_PATH = os.path.join(CURRENT_PATH,"log")
STA_PATH = os.path.join(CURRENT_PATH,"sta")
ROUTER_PATH = os.path.join(CURRENT_PATH,"routers")
DATA_PATH = os.path.join(CURRENT_PATH,"data")

DATA_TXT_PATH = os.path.join(DATA_PATH,"txt")
DATA_TXT_FINISH_PATH = os.path.join(DATA_TXT_PATH,"finished")

DATA_CSV_PATH = os.path.join(DATA_PATH,"csv_xlsx")
DATA_CSV_FINISH_PATH = os.path.join(DATA_CSV_PATH,"finished")

DATA_USAGE_PATH = os.path.join(DATA_PATH,"usage")