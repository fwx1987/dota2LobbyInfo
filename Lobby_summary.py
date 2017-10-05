

from SteamServerLog import ServerLogReader
from SteamMemberInfo import SteamMemberInfo
import os,json
import fileinput
from util import ODotaUtil
from shutil import copyfile
import time
import webbrowser


def generate_summary_html_report(player_array):

    fileDir = os.path.dirname(os.path.realpath('__file__'))

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
            generate_summary_html_report(newcoming)

            print('generate report done within:'+str(round((time.time()-starttime),2)))

            latest = newcoming

            url = "D:/PycharmProjects/dota2LobbyInfo/report/summary.html"
            webbrowser.open(url,new=0)
        else:
            print("start to sleep 5 seconds")
            time.sleep(5)
            times +=1
            newcoming = ServerLogReader.get_lobby_members()
