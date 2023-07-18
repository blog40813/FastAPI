import logging
import os 
import time
from configs import *

def log(log_name):
    # logger 命名為：file_conversion
    logger = logging.getLogger(log_name)
    # 設置級別
    logger.setLevel(logging.DEBUG)
    # 紀錄格式
    formatter = logging.Formatter('%(asctime)s | FastAPI | %(levelname)s : %(message)s (%(name)s)', datefmt="%Y-%m-%d %H:%M:%S")

    logdir = LOG_PATH

    # 建立以日期開頭的 log 文件
    logtime = time.strftime('%Y-%m-%d')
    logFileExtension = "log"
    logfile_list = list()
    logfile_list.append(logtime)
    logfile_list.append(logFileExtension)
    logFileName_extension = '.'.join(logfile_list)
    logfile = os.path.join(logdir, logFileName_extension)

    fh = logging.FileHandler(logfile, mode='a')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger

if __name__ == '__main__':
    logger = log()
    logger.debug('__debug__')
    logger.warning('__warning__')
    logger.info('__info__')
    logger.error('__error__')
