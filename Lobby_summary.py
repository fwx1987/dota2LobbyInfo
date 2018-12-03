

from SteamServerLog import ServerLogReader
from SteamMemberInfo import SteamMemberInfo
import os,json
import fileinput
from util import ODotaUtil
from shutil import copyfile
import time
import webbrowser,threading
import logging,logging.handlers

import config

def get_player_info_to_file(player_id,file,player_lobby):
    player_Obj = ODotaUtil.Player(player_id)
    json_obj = player_Obj.to_html_source_json()

    all=[]
    ' add player lobby info into the json'
    for item in json_obj:
        item['player_lobby'] = player_lobby
        all.append(item)



    if os.path.exists(file):
        os.remove(file)

    with open(file, 'w') as file:
        logger.debug('get info for  player_id: '+str(player_id)+' '+'player_lobby: '+str(player_lobby)+' '+'successful, the content is '+json.dumps(all))
        file.write(json.dumps(all))


class Plyaer_Info_collector_Thread (threading.Thread):
   def __init__(self, threadID, name, player_id,file,player_lobby):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.player_id = player_id
      self.player_lobby = player_lobby
      self.file = file

   def run(self):
      logger.info ("Starting thread: " + self.name +" to collect info for player: "+str(self.player_id))
      get_player_info_to_file(self.player_id, self.file,self.player_lobby)
      logger.info ("collect info for player: "+str(self.player_id) + " finsihed")

def generate_summary_html_report(player_array):

    fileDir = os.path.dirname(os.path.realpath('__file__'))
    template_report = os.path.join(fileDir, 'report\summary_template.html')
    target_report = os.path.join(fileDir, 'report\summary.html')
    date_today = time.strftime('%Y%m%d')
    try:
        if not os.path.exists(os.path.join(fileDir,'report\\'+date_today+"\\")):
            os.mkdir(os.path.join(fileDir,'report\\'+date_today+"\\"))
    except Exception as e:
        logger.info("exception occured when creating date folder:"+str(e))
        pass
    seq = 0
    while True:
        seq = seq + 1
        if seq <= 9:
            str_seq = '0' + str(seq)
        else:
            str_seq = str(seq)
        target_report = os.path.join(fileDir, 'report\\' + date_today + '\\' + str(str_seq) + '\\summary.html')
        if not os.path.exists(target_report):
            try:
                os.mkdir(os.path.dirname(target_report))
            except Exception as e:
                logger.info("directory exist")
            copyfile(os.path.join(fileDir,'report\summary.js'), os.path.join(os.path.dirname(target_report),'summary.js'))
            break

    radiant = []
    dire = []

    threads =[]
    for i in range (1,len(player_array)+1):
        player_id = player_array[i-1]
        file =  os.path.join(os.path.dirname(target_report), 'player_' + str(i) + ".json")
        thread = Plyaer_Info_collector_Thread(i, "thread-"+str(i), player_array[i-1], file,i)
        thread.start()
        threads.append(thread)

    if os.path.exists(target_report):
        logger.info("Target summary report file exist, deleting:")
        os.remove(target_report)

    copyfile(template_report, target_report)

    for thread in threads:
        thread.join()

    for i in range(1, len(player_array) + 1):
        file = os.path.join(os.path.dirname(target_report), 'player_' + str(i) + ".json")


        with open(file, 'r') as file:
            content = json.loads(file.read())

            for record in content:
                if i <= 5:
                    radiant.append(record)
                else:
                    dire.append(record)



    with fileinput.FileInput(target_report, inplace=True, backup='.bak') as file:
        for line in file:
            print(line.replace("var radianttabledata = @@", "var radianttabledata ="+json.dumps(radiant)+";"), end='')
    with fileinput.FileInput(target_report, inplace=True, backup='.bak') as file:
        for line in file:
            print(line.replace("var diretabledata = @@", "var diretabledata ="+json.dumps(dire)+";"), end='')

    webbrowser.open(target_report,new=0)
'''
date_today = time.strftime('%Y%m%d')
log_file = "log/Summary_generation_"+date_today+".log"
handler = logging.handlers.RotatingFileHandler(log_file, maxBytes = 1024*1024, backupCount = 5) # 实例化handler
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
formatter = logging.Formatter(fmt)   # 实例化formatter
handler.setFormatter(formatter)      # 为handler添加formatter
logger = logging.getLogger('Lobby Summary')  # 获取名为Lobby Summary的logger
logger.addHandler(handler)  # 为logger添加handler
logger.setLevel(logging.DEBUG)
'''

logger = logging.getLogger(__name__)

def main():
    latest = []
    newcoming =ServerLogReader.get_lobby_members()
    times = 1

    start_time = time.time()
    latest = []
    while(time.time()-start_time)<8*60*60:
        '''iterative the app for running with 8 hours'''

        if (latest!=newcoming):
            logger.info('Start to capture information for :'+'，'.join(newcoming))
            starttime = time.time()
            try:
                generate_summary_html_report(newcoming)
            except Exception as e:
                logger.info("exception occured:"+str(e))
            logger.info('generate report done within:'+str(round((time.time()-starttime),2)))

            latest = newcoming


        else:
            time.sleep(5)
            times +=1
            newcoming = ServerLogReader.get_lobby_members()



if __name__ == "__main__":

    main()
