import os

CURRENT = os.getcwd()
LOG = os.path.join(CURRENT,"log")
STA = os.path.join(CURRENT,"sta")
ROUTER = os.path.join(CURRENT,"routers")
DATA = os.path.join(CURRENT,"data")

DATA_TXT = os.path.join(DATA,"txt")
DATA_TXT_FINISH = os.path.join(DATA_TXT,"finished")

DATA_CSV = os.path.join(DATA,"csv_xlsx")
DATA_CSV_FINISH = os.path.join(DATA_CSV,"finished")

DATA_USAGE = os.path.join(DATA,"usage")