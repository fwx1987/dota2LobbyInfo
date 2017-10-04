
# -*- coding: UTF-8 -*-

from SteamServerLog import ServerLogReader
from SteamMemberInfo import SteamMemberInfo
import os,json
import fileinput
from shutil import copyfile
import time

import webbrowser

def output_json_to_file(json_obj, file):

    if os.path.exists(file):
        print("file exist, deleting:" )
        os.remove(file)


    with open(file, 'w') as file:
        file.write(json.dumps(json_obj))

    pass


def process_player_json(json_obj):

    all=[]
    player_text  = {}
    hero_text = {}

    player_text['player_slot'] = str(json_obj['player_slot'])
    player_text['account_name'] = json_obj['account_name']
    player_text['account_avatar'] = json_obj['account_avatar']
    player_text['total_games'] = json_obj['total_games']
    player_text['total_hero_played'] = json_obj['total_hero_played']
    player_text['total_avg_gpm'] = json_obj['total_avg_gpm']
    player_text['total_win_rate'] = json_obj['total_win_rate']
    player_text['total_avg_win_gpm'] = json_obj['total_avg_win_gpm']
    player_text['total_avg_lose_gpm'] = json_obj['total_avg_lose_gpm']
    player_text['last_24_hrs_win_rate'] = json_obj['last_24_hrs_win_rate']
    player_text['last_24_hrs_win'] = json_obj['last_24_hrs_win']
    player_text['last_24_hrs_lose'] = json_obj['last_24_hrs_lose']
    player_text['total_hero_played'] = json_obj['total_hero_played']
    player_text['win_history'] = json_obj['win_history']
    player_text['gpm_history'] = json_obj['gpm_history']

    hero_text['player_slot'] = "hero_"+str(json_obj['player_slot'])
    hero_text['account_name'] = json_obj['account_name']
    hero_text['account_avatar'] = json_obj['account_avatar']
    hero_text['total_games'] = json_obj['total_games']
    hero_text['total_hero_played'] = json_obj['total_hero_played']
    hero_text['total_avg_gpm'] = json_obj['total_avg_gpm']
    hero_text['total_win_rate'] = json_obj['total_win_rate']
    hero_text['total_avg_win_gpm'] = json_obj['total_avg_win_gpm']
    hero_text['total_avg_lose_gpm'] = json_obj['total_avg_lose_gpm']
    hero_text['last_24_hrs_win_rate'] = json_obj['last_24_hrs_win_rate']
    hero_text['last_24_hrs_win'] = json_obj['last_24_hrs_win']
    hero_text['last_24_hrs_lose'] = json_obj['last_24_hrs_lose']
    hero_text['total_hero_played'] = json_obj['total_hero_played']



    #if (len(json_obj['hero_records']) ==0):
    if (player_text['total_games']==0):
        all.append(player_text)
    else:

        index = 0
        for hero in json_obj['hero_records']:
            hero_text={}
            if index == 0:
                player_text['fav_hero'] = hero['hero_name']
                player_text['hero_sb_image'] = hero['hero_sb_image']
                player_text['hero_games_played'] = hero['games_played']
                player_text['hero_win_rate'] = hero['win_rate']
                player_text['hero_gpm_for_win'] = hero['gpm_for_win']
                player_text['hero_gpm_for_lose'] = hero['gpm_for_lose']
                player_text['hero_last_24_hrs_win_rate'] = hero['last_24_hrs_win_rate']
                player_text['hero_last_24_hrs_win'] = hero['last_24_hrs_win']
                player_text['hero_last_24_hrs_lose'] = hero['last_24_hrs_lose']
                player_text['hero_win_history'] = hero['hero_win_history']
                all.append(player_text)

                #first hero record
                hero_text['player_slot'] = "hero_"+str(json_obj['player_slot'])
                hero_text['account_name'] = hero['hero_name']
                hero_text['account_avatar'] = hero['hero_sb_image']
                hero_text['total_games'] = hero['games_played']
                hero_text['total_hero_played'] = "NA"
                hero_text['total_avg_gpm'] = hero['total_avg_gpm']
                hero_text['total_win_rate'] = hero['win_rate']
                hero_text['total_avg_win_gpm'] = hero['gpm_for_win']
                hero_text['total_avg_lose_gpm'] = hero['gpm_for_lose']
                hero_text['last_24_hrs_win_rate'] = hero['last_24_hrs_win_rate']
                hero_text['last_24_hrs_win'] = hero['last_24_hrs_win']
                hero_text['last_24_hrs_lose'] = hero['last_24_hrs_lose']
                hero_text['total_hero_played'] = "NA"
                hero_text['win_history'] = hero['hero_win_history']
                hero_text['win_history'] =  hero['hero_win_history']
                hero_text['gpm_history'] = hero['hero_gpm_history']
                all.append(hero_text)


            else:
                hero_text['player_slot'] = "hero_"+str(json_obj['player_slot'])
                hero_text['account_name'] = hero['hero_name']
                hero_text['account_avatar'] = hero['hero_sb_image']
                hero_text['total_games'] = hero['games_played']
                hero_text['total_avg_gpm'] = hero['total_avg_gpm']
                hero_text['total_hero_played'] = "NA"
                hero_text['total_avg_gpm'] = 0
                hero_text['total_win_rate'] = hero['win_rate']
                hero_text['total_avg_win_gpm'] = hero['gpm_for_win']
                hero_text['total_avg_lose_gpm'] = hero['gpm_for_lose']
                hero_text['last_24_hrs_win_rate'] = hero['last_24_hrs_win_rate']
                hero_text['last_24_hrs_win'] = hero['last_24_hrs_win']
                hero_text['last_24_hrs_lose'] = hero['last_24_hrs_lose']
                hero_text['total_hero_played'] = "NA"
                hero_text['win_history'] = hero['hero_win_history']
                hero_text['gpm_history'] = hero['hero_gpm_history']
                all.append(hero_text)


            index+=1
        if index==0:
            all.append(player_text)
            return all
    return all












    pass

def generate_html_report(player_list):
    radiant = []
    dire = []

    index = 0
    for player in player_list:
        print(player)
        member = SteamMemberInfo.MemberInfo(int(player))
        member.process()
        member.output()

        player_json = member.to_json()

        player_json['player_slot'] = index
        #print(medusa.to_json())
        print("before processing:")
        print(player_json)
        player_json = process_player_json(player_json)
        print("after processing:")
        print(player_json)

        for item in player_json:
            if index<=4:
                radiant.append(item)
            else:
                dire.append(item)
        index +=1

    if os.path.exists("D:/PycharmProjects/dota2LobbyInfo/report/report.html"):
        print("file exist, deleting:" )
        os.remove("D:/PycharmProjects/dota2LobbyInfo/report/report.html")

    copyfile("D:/PycharmProjects/dota2LobbyInfo/report/report - template.html","D:/PycharmProjects/dota2LobbyInfo/report/report.html")
    with fileinput.FileInput("D:/PycharmProjects/dota2LobbyInfo/report/report.html", inplace=True, backup='.bak') as file:
        for line in file:
            print(line.replace("var radianttabledata = @@", "var radianttabledata ="+json.dumps(radiant)+";"), end='')
    with fileinput.FileInput("D:/PycharmProjects/dota2LobbyInfo/report/report.html", inplace=True, backup='.bak') as file:
        for line in file:
            print(line.replace("var diretabledata = @@", "var diretabledata ="+json.dumps(dire)+";"), end='')

if __name__ == "__main__":




    latest = ServerLogReader.get_lobby_members()
    newcoming =latest

    print(latest==newcoming)
    times = 1

    start_time = time.time()
    latest = []
    while(time.time()-start_time)<8*60*60:

        if (latest!=newcoming):
            generate_html_report(newcoming)
            print('generate report done')

            latest = newcoming

            url = "D:/PycharmProjects/dota2LobbyInfo/report/report.html"
            webbrowser.open(url,new=0)
        else:
            print("start to sleep 5 seconds")
            time.sleep(5)
            times +=1
            newcoming = ServerLogReader.get_lobby_members()










