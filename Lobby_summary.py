

from SteamServerLog import ServerLogReader
from SteamMemberInfo import SteamMemberInfo
import os,json
import fileinput
from util import ODotaUtil
from shutil import copyfile
import time
import webbrowser,threading


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
      print ("Starting thread: " + self.name +" to collect info for player: "+str(self.player_id))
      get_player_info_to_file(self.player_id, self.file,self.player_lobby)
      print ("collect info for player: "+str(self.player_id) + " finsihed")

def generate_summary_html_report(player_array):

    fileDir = os.path.dirname(os.path.realpath('__file__'))
    print(fileDir)
    template_report = os.path.join(fileDir, 'report\summary_template.html')
    target_report = os.path.join(fileDir, 'report\summary.html')


    radiant = []
    dire = []

    threads =[]
    for i in range (1,len(player_array)+1):
        player_id = player_array[i-1]
        file =  os.path.join(fileDir, 'report\player_temp_data\player_'+str(i)+".json")
        thread = Plyaer_Info_collector_Thread(i, "thread-"+str(i), player_array[i-1], file,i)
        thread.start()
        threads.append(thread)

    if os.path.exists(target_report):
        print("Target summary report file exist, deleting:")
        os.remove(target_report)

    copyfile(template_report, target_report)

    for thread in threads:
        thread.join()

    for i in range(1, len(player_array) + 1):
        file = os.path.join(fileDir, 'report\player_temp_data\player_' + str(i) + ".json")


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


def generate_summary_html_report2(player_array):

    fileDir = os.path.dirname(os.path.realpath('__file__'))
    print(fileDir)
    template_report = os.path.join(fileDir, 'report\summary_template.html')
    target_report = os.path.join(fileDir, 'report\summary.html')
    radiant = []
    dire = []

    index=0
    for player in player_array:
        player_Obj = ODotaUtil.Player(player)

        json_obj = player_Obj.to_html_source_json()
        if index<=4:

            for item in json_obj:
                item['player_lobby'] = index+1
                radiant.append(item)
        else:

            for item in json_obj:
                item['player_lobby'] = index+1
                dire.append(item)
        index+=1

    if os.path.exists(target_report):
        print("Target summary report file exist, deleting:" )
        os.remove(target_report)

    copyfile(template_report,target_report)
    with fileinput.FileInput(target_report, inplace=True, backup='.bak') as file:
        for line in file:
            print(line.replace("var radianttabledata = @@", "var radianttabledata ="+json.dumps(radiant)+";"), end='')
    with fileinput.FileInput(target_report, inplace=True, backup='.bak') as file:
        for line in file:
            print(line.replace("var diretabledata = @@", "var diretabledata ="+json.dumps(dire)+";"), end='')



if __name__ == "__main__":

    latest = []
    newcoming =ServerLogReader.get_lobby_members()
    times = 1

    start_time = time.time()
    latest = []
    while(time.time()-start_time)<8*60*60:

        if (latest!=newcoming):
            starttime = time.time()
            try:
                generate_summary_html_report(newcoming)
            except Exception as e:
                print("exception occured:"+str(e))
            print('generate report done within:'+str(round((time.time()-starttime),2)))

            latest = newcoming

            url = "D:/PycharmProjects/dota2LobbyInfo/report/summary.html"
            webbrowser.open(url,new=0)
        else:
            time.sleep(5)
            times +=1
            newcoming = ServerLogReader.get_lobby_members()
    
