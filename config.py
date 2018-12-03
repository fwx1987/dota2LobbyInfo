



import os,time,logging,logging.config





def get_root_directory():
    return os.path.dirname(os.path.realpath(__file__))

logging.config.fileConfig(get_root_directory()+"/config.ini")

'''
date_today = time.strftime('%Y%m%d')
log_file = get_root_directory()+"/log/Summary_generation_"+date_today+".log"


handler = logging.handlers.RotatingFileHandler(log_file, maxBytes = 1024*1024, backupCount = 5) # 实例化handler
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
formatter = logging.Formatter(fmt)   # 实例化formatter
handler.setFormatter(formatter)      # 为handler添加formatter
logger = logging.getLogger('App')  # 获取名为Lobby Summary的logger
logger.addHandler(handler)  # 为logger添加handler
logger.setLevel(logging.DEBUG)


logging.info("config file is loading")
'''
