import os,time,logging,logging.handlers
from pynput.keyboard import Key,Controller
from SteamServerLog import ServerLogReader
from Media import MediaPlayer
videoRecordingFolder = "/Users/wenxiang/PycharmProjects/dota2LobbyInfo/data/video/"

videoRecordingFolder = "D://dota video//Nvidia"


wait_action_time= 10

date_today = time.strftime('%Y%m%d')
log_file = "log/Nvidia_recorder_"+date_today+".log"
handler = logging.handlers.RotatingFileHandler(log_file, maxBytes = 1024*1024, backupCount = 5) # 实例化handler
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
formatter = logging.Formatter(fmt)   # 实例化formatter
handler.setFormatter(formatter)      # 为handler添加formatter
logger = logging.getLogger('CallNvidiaRecording')  # 获取名为tst的logger
logger.addHandler(handler)  # 为logger添加handler
logger.setLevel(logging.DEBUG)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)
logger.addHandler(consoleHandler)


' get folder file total size.'
def getFolderTotalSize(folder):
    size = 0
    '''
    for file in os.listdir(folder):
        if not os.path.isdir(file):
            size = size + os.path.getsize(folder+"/"+file)
        else:
            size = size + getFolderTotalSize(file)
    return size
    '''
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size
def is_video_recording():
    size = getFolderTotalSize(videoRecordingFolder)

    logger.info("before jugding, folder size is:"+str(size))

    time.sleep(wait_action_time)

    new_size= getFolderTotalSize(videoRecordingFolder)

    if new_size - size >0:

        print("file size is increasing, the video is recording")
        return True
    else:
        logger.info("folder size not increasing")

        return False

    '''
    video_files = os.listdir(videoRecordingFolder)
    print(video_files)
    for item in video_files:
        print(item)
        if item.endswith("1"):

            logger.info("after jugding, folder size is:" + str(size))
            return True
        else:
            logger.info(" no temp file found")
            logger.info("after jugding, folder size is:" + str(size))
            return False
    return False
    '''

def is_process_running():
    if len(os.popen("tasklist |findstr dota2.exe").read()) > 0:
        logger.info("dota2.exe is found")
        return True
    else:
        logger.info("dota2 is not lunched")
        return False

def start_video_recording():
    #emit_hot_key("Alt+F9")
    MediaPlayer.play_music("")
    if is_video_recording() == True:

        pass
    else:
        emit_hot_key("Alt+F9")

def emit_hot_key(hot_key):
    return True
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

def stop_video_recording():

    if is_video_recording():
        #emit_hot_key("Alt+F9")
        MediaPlayer.play_music("")
    else:
        #MediaPlayer.play_music("")
        return

if __name__ == "__main__":


    start_time = time.time()
    #loop for 8 hours
    while (time.time() - start_time) < 8 * 60 * 60:
        if not is_process_running():
            logger.info("dota2 process not found, wait for 5 seconds to check again...")
            time.sleep(wait_action_time)
        else:
            status = ServerLogReader.get_player_status()
            times = 0 # interactively increase wait time if the mode is keep on in game.
            if status == "in_game":
                if is_video_recording() == True:

                    times = times+1
                    if times*wait_action_time<60:
                        logger.info("Recording is in progress, wait for "+str(times*wait_action_time)+" seconds to check again...")
                        time.sleep(wait_action_time*times)
                else:
                    logger.info("Recording starting, wait for "+str(wait_action_time)+"seconds to check again...")
                    #start_video_recording()
                    time.sleep(wait_action_time)
            if status == "idle" or status == "in_game_watching":
                logger.info("Recording stopping, wait for "+str(wait_action_time)+"seconds to check again...")
                stop_video_recording()
                time.sleep(wait_action_time)
        time.sleep(wait_action_time)




'''
    emit_hot_key("Alt+F9")
    logger.info("===size===")
    logger.info(os.path.getsize(videoRecordingFolder))


    pass'''