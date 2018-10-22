import os,time,logging,logging.handlers
from pynput.keyboard import Key,Controller
videoRecordingFolder = "/Users/wenxiang/PycharmProjects/dota2LobbyInfo/data/video/"


date_today = time.strftime('%Y%m%d')
log_file = "log/Nvidia_recorder_"+date_today+".log"
handler = logging.handlers.RotatingFileHandler(log_file, maxBytes = 1024*1024, backupCount = 5) # 实例化handler
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
formatter = logging.Formatter(fmt)   # 实例化formatter
handler.setFormatter(formatter)      # 为handler添加formatter
logger = logging.getLogger('tst')  # 获取名为tst的logger
logger.addHandler(handler)  # 为logger添加handler
logger.setLevel(logging.DEBUG)

def is_Video_recording():
    size = os.path.getsize(videoRecordingFolder)

    logger.info("before jugding, folder size is:"+str(size))

    time.sleep(5)

    new_size= os.path.getsize(videoRecordingFolder)

    if new_size - size >0:

        print("file size is incrasing, the video is recording")
        return True
    else:
        logger.info("folder size not increasing")
    video_files = os.listdir(videoRecordingFolder)
    print(video_files)
    for item in video_files:
        print(item)
        if item.endswith("1"):
            logger.info("temp file found")
            logger.info("after jugding, folder size is:" + str(size))
            return True
        else:
            logger.info(" no temp file found")
            logger.info("after jugding, folder size is:" + str(size))
            return False
    return False


def is_process_running():
    if len(os.popen("tasklist |findstr dota2.exe").read()) > 0:
        logger.info("dota2.exe is found")
        return True
    else:
        logger.info("dota2 is not lunched")
        return False


def emit_hot_key(hot_key):
    logger.info(hot_key.split("+"))
    keyboard = Controller()

    items =  hot_key.split("+")
    for item in items:

        if item == "Ctrl":
            keyboard.press(Key.ctrl)
        if item == "Tab":
            keyboard.press(Key.tab)
        if item == "F9":
            keyboard.press(Key.f9)
        if item == "Alt":
            keyboard.press(Key.alt)

    for item in items:
        if item == "Ctrl":
            keyboard.release(Key.ctrl)
        if item == "Tab":
            keyboard.release(Key.tab)
        if item == "F9":
            keyboard.release(Key.f9)
        if item == "Alt":
            keyboard.release(Key.alt)

    return True

if __name__ == "__main__":


    is_Video_recording()

    emit_hot_key("Ctrl+Tab")
    logger.info("===size===")
    logger.info(os.path.getsize(videoRecordingFolder))


    pass