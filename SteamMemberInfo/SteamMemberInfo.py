import dota2api
import json,time,os
from operator import itemgetter,attrgetter
import sqlite3
from util  import Util
import os.path
__steam_api_key__= None
__game_data__ = None

__heroes__ = None

def get_member_game_history(user_dota2_id):
    api = dota2api.Initialise("4B1FD9D1888114755F2A9C7B5788A085")
    try:
        hist = api.get_match_history(account_id=user_dota2_id,matches_requested=100,min_players=10)
    except Exception:
        hist = None
    return hist

def get_game_details(dota2_game_id):
    api = dota2api.Initialise("4B1FD9D1888114755F2A9C7B5788A085")
    global __game_data__
    if not __game_data__ or __game_data__['match_id'] !=  dota2_game_id:
        #print("start to get game details: "+str(dota2_game_id))
        #__game_data__ =  api.get_match_details(match_id=dota2_game_id)


        if Util.db_is_match_exist(dota2_game_id):
            __game_data__ = json.loads(Util.db_get_match_details(dota2_game_id))
        else:
            __game_data__ = api.get_match_details(match_id=dota2_game_id)
            Util.db_insert_match_details(dota2_game_id,json.dumps(__game_data__))
        return __game_data__
'''
        game_file =  "D:/PycharmProjects/data/game/"+str(dota2_game_id)+".txt"
        if os.path.exists(game_file):
            #print ("has exsting file:"+game_file)
            with open(game_file, 'r') as file:
                content = file.read()
                __game_data__ = json.loads(content)
        else:
            __game_data__ = api.get_match_details(match_id=dota2_game_id)
            with open(game_file, 'w') as file:
                 file.write(json.dumps(__game_data__))
    #with open('file.txt', 'w') as file:
    #     file.write(json.dumps(__game_data__))
    #with open('file.txt', 'r') as file:
    #     content = file.read()
    #__game_data__ = json.loads(content)
    return __game_data__
'''
def export_dict_to_file(dict,file):
    pass
def get_game_player_gpm(dota2_game_id,dota2_player_id):
    global __game_data__
    if not __game_data__ or __game_data__['match_id'] !=  dota2_game_id:
        __game_data__ = get_game_details(dota2_game_id)


    for player in __game_data__['players']:
        if player['account_id'] == dota2_player_id:
           return player['gold_per_min']
        else:
            pass
    return 0


def get_game_player_kda(dota2_game_id,dota2_player_id):
    global __game_data__
    if not __game_data__ or __game_data__['match_id'] !=  dota2_game_id:
        __game_data__ = get_game_details(dota2_game_id)

    for player in __game_data__['players']:
        if player['account_id'] == dota2_player_id:
           return (player['kills']+player['assists'])/player['deaths']
    return 0

def get_game_player_hero(dota2_game_id,dota2_player_id):
    global __game_data__
    if not __game_data__ or __game_data__['match_id'] !=  dota2_game_id:
        __game_data__ = get_game_details(dota2_game_id)

    for player in __game_data__['players']:
        if player['account_id'] == dota2_player_id:
           return player['hero_id']


    return 0


def is_game_player_win(dota2_game_id,dota2_player_id):
    global __game_data__
    if not __game_data__ or __game_data__['match_id'] !=  dota2_game_id:
        __game_data__ = get_game_details(dota2_game_id)

    player_slot = 0
    radiant_win = __game_data__['radiant_win']
    for player in __game_data__['players']:
        if player['account_id'] == dota2_player_id:
            player_slot = player['player_slot']

            break

    if player_slot<=4 and player_slot>=0:

        if radiant_win:
            return True
        else:
            return False

    else:
        if radiant_win:
            return False
        else:
            return True

class HeroRecord:
    '''hero_id = 0
    number_of_games = 0
    win_rate = 0
    gpm_for_win = 0
    gpm_for_lose = 0
    number_of_win = 0
    number_of_lose = 0
    total_gpm_for_win = 0
    total_gpm_for_lose = 0'''

    def __init__(self,hero_id,win,gpm,is_last_24_hrs_match=False):
        self.hero_id = hero_id
        self.number_of_games = 0
        self.win_rate = 0
        self.gpm_for_win = 0
        self.gpm_for_lose = 0

        self.number_of_win = 0
        self.number_of_lose = 0
        self.total_gpm_for_win = 0
        self.total_gpm_for_lose = 0
        self.total_avg_gpm = 0
        self.last_24_hrs_win = 0
        self.last_24_hrs_lose = 0
        self.last_24_hrs_win_rate = 50.00
        self.hero_win_history = []
        self.hero_gpm_history =[]

        self.update_with_game(win,gpm,is_last_24_hrs_match)



    def update_with_game(self,win,gpm,is_last_24_hrs_match = False):
        self.number_of_games = self.number_of_games+1

        if win:
            self.number_of_win = self.number_of_win+1
            self.total_gpm_for_win = self.total_gpm_for_win + gpm
            self.gpm_for_win = round(self.total_gpm_for_win/self.number_of_win,2)

            if is_last_24_hrs_match:
                self.last_24_hrs_win +=1
            self.hero_win_history.append(1)
        else:
            self.number_of_lose = self.number_of_lose+1
            self.total_gpm_for_lose = self.total_gpm_for_lose +gpm
            self.gpm_for_lose = round(self.total_gpm_for_lose / self.number_of_lose,2)
            if is_last_24_hrs_match:
                self.last_24_hrs_lose +=1
            self.hero_win_history.append(-1)
        if (self.last_24_hrs_win+self.last_24_hrs_lose) > 0:
            self.last_24_hrs_win_rate = round(self.last_24_hrs_win/(self.last_24_hrs_lose+self.last_24_hrs_win),2)
        self.hero_gpm_history.append(gpm)
        self.total_avg_gpm = round((self.total_gpm_for_lose+self.total_gpm_for_win)/(self.number_of_games),2)

        self.win_rate = round((self.number_of_win / self.number_of_games) * 100, 2)


    def output(self):
        print("hero id: "+str(self.hero_id))
        print("number of games: "+str(self.number_of_games))
        pass

class MemberInfo:
    #repostiory data
    ''' member_id = ""
    member_raw_history = ""
    member_last_60_days_history =[]
    #all hero date
    number_heros_played = 0
    total_games = 0
    total_avg_gpm = 0
    total_win_rate = 0
    total_avg_win_gpm =0
    total_avg_lose_gpm = 0
    #specific hero data
    hero_record = [] '''

    def __init__(self,member_id):
        self.member_id = member_id
        self.member_raw_history = get_member_game_history(self.member_id)
        self.member_last_60_days_history = []
        self.number_heros_played = 0
        self.total_games = 0
        self.total_avg_gpm = 0
        self.total_win_rate = 0
        self.total_avg_gpm = 0
        self.total_avg_win_gpm = 0
        self.total_avg_lose_gpm = 0
        self.hero_record = []
        self.last_24_hrs_win = 0
        self.last_24_hrs_lose = 0
        self.last_24_hrs_win_rate = 50.00
        self.win_history = []
        self.gpm_history = []
        self.crawl_60_days_history()

    def crawl_60_days_history(self):

        if self.member_raw_history == None:
            self.member_last_60_days_history = None
            return
            pass
        temp_list = self.member_raw_history['matches']
        for match in temp_list:
            if match['start_time'] >=time.time()-30*24*60*60 :

                self.member_last_60_days_history.append(match)


        print (self.member_last_60_days_history)

        print(len(self.member_last_60_days_history))


    def process(self):

        #temp data
        number_of_win=0
        number_of_lose = 0
        hero_playing = 0
        total_gpm = 0
        total_win_gpm =0
        total_lose_gpm = 0
        hero_playing = 0
        is_win = False
        game_gpm = 0
        if self.member_last_60_days_history ==None:
            return
        number_of_match = len(self.member_last_60_days_history)

        if number_of_match==0:
            return
        for match in self.member_last_60_days_history:
            fresh_hero = True
            match_id = match['match_id']
            #get number of win games
            #get number of lose games
            is_win = is_game_player_win(match_id,self.member_id)
            hero_playing = get_game_player_hero(match_id,self.member_id)
            game_gpm = get_game_player_gpm(match_id,self.member_id)
            self.gpm_history.append(game_gpm)
            is_last_24_hrs_match = False
            if match['start_time'] >=time.time()-24*60*60 :
                is_last_24_hrs_match = True
            if is_win:
                if is_last_24_hrs_match :
                    self.last_24_hrs_win += 1
                number_of_win = number_of_win+1
                total_win_gpm = total_win_gpm + game_gpm
                self.win_history.append(1)
            else:
                if is_last_24_hrs_match :
                    self.last_24_hrs_lose += 1
                number_of_lose = number_of_lose+1
                total_lose_gpm = total_lose_gpm + game_gpm
                self.win_history.append(-1)
            #get total gpm for all heros
            total_gpm = total_gpm + game_gpm

            for hero in self.hero_record:
                if hero.hero_id == hero_playing:
                    fresh_hero = False
                    hero.update_with_game(is_win,game_gpm,is_last_24_hrs_match)

            if fresh_hero:
                self.hero_record.append(HeroRecord(hero_playing,is_win,game_gpm,is_last_24_hrs_match))
        if (self.last_24_hrs_win+self.last_24_hrs_lose) > 0:
            self.last_24_hrs_win_rate = round(self.last_24_hrs_win/(self.last_24_hrs_lose+self.last_24_hrs_win),2)
        #get overall statics for all heroes

        self.number_heros_played = len(self.hero_record)
        self.total_games = number_of_match
        self.total_avg_gpm = round(total_gpm / self.total_games,2)

        #self.total_avg_gpm = total_gpm / self.total_games
        self.total_win_rate = round(number_of_win *100 / self.total_games,2)

        if number_of_win == 0:
            self.total_avg_win_gpm = 0
        else:
            self.total_avg_win_gpm = round(total_win_gpm/number_of_win,2)

        if number_of_lose == 0:
            self.total_avg_lose_gpm = 0
        else:
            self.total_avg_lose_gpm = round(total_lose_gpm/number_of_lose,2)

        self.sort_hero_record()


    def sort_hero_record(self):

        self.hero_record = sorted(self.hero_record,key=attrgetter('number_of_games'),reverse=True)
        pass

    def output(self):
        if self.total_games == 0 :
            print("this player "+ str(self.member_id) +" seems didnt enable game history")
            return
        print("Plyaer id: "+str(self.member_id))

        print("total games: "+str(self.total_games))
        print("total hero played: "+str(self.number_heros_played))

        print("total avg gpm: "+str(self.total_avg_gpm))
        print("total win rate: "+str(self.total_win_rate))
        print("total avg win gpm: "+str(self.total_avg_win_gpm))
        print("total avg lose gpm: "+str(self.total_avg_lose_gpm))
        print("last 24 hrs win rate: " + str(self.last_24_hrs_win_rate))
        print("last 24 hrs win : " + str(self.last_24_hrs_win))
        print("last 24 hrs lose : " + str(self.last_24_hrs_lose))
        print("total number of heroes record collected:"+str(len(self.hero_record)))

        for hero in self.hero_record:
            print ("hero id:"+str(hero.hero_id))
            print ("hero played times:"+str(hero.number_of_games))
            hero.win_rate = round(hero.win_rate,2)
            print ("hero win rate: "+str(hero.win_rate))
            print ("gpm for win: "+str(hero.gpm_for_win))
            print ("gpm for lose: "+str(hero.gpm_for_lose))

    #output to json text
    def to_json(self):
        json_text= {}
        json_text['account_id']= self.member_id
        json_text['account_name'] = get_player_summary(self.member_id,"personaname")
        json_text['account_avatar'] = get_player_summary(self.member_id,"avatar")
        json_text['account_avatarmedium'] = get_player_summary(self.member_id,"avatarmedium")
        json_text['account_avatarfull'] = get_player_summary(self.member_id,"avatarfull")
        json_text['total_games'] = self.total_games
        json_text['total_hero_played'] = self.number_heros_played
        json_text['total_hero_played'] = self.number_heros_played
        json_text['total_avg_gpm'] = self.total_avg_gpm
        json_text['total_win_rate'] = self.total_win_rate
        json_text['total_avg_win_gpm'] = self.total_avg_win_gpm
        json_text['total_avg_lose_gpm'] = self.total_avg_lose_gpm
        json_text['last_24_hrs_win_rate'] = self.last_24_hrs_win_rate
        json_text['last_24_hrs_win'] = self.last_24_hrs_win
        json_text['last_24_hrs_lose'] = self.last_24_hrs_lose
        json_text['total_number_of_heroes_record_collected'] = len(self.hero_record)
        self.win_history.reverse()
        json_text['win_history'] = self.win_history[-10:]
        self.gpm_history.reverse()

        if len(self.gpm_history)>5:
            self.gpm_history.append(100)
            self.gpm_history.append(200)
            self.gpm_history.append(300)
            self.gpm_history.append(400)
            self.gpm_history.append(500)
            self.gpm_history.append(600)
            self.gpm_history.append(700)
            self.gpm_history.append(800)
            self.gpm_history.append(900)

        json_text['gpm_history'] = self.gpm_history[-19:]
        objective_json = json_text
        if len(self.hero_record) == 0:

            return objective_json

        else:
            index = 0
            temp_obj = []
            for hero in self.hero_record:
                if index ==0 or hero.number_of_games>=5:
                    hero_record = {}
                    hero_record['hero_id'] = hero.hero_id
                    hero_record['hero_name'] = get_hero_name(hero.hero_id)
                    hero_record['hero_full_image'] = get_hero_images(hero.hero_id,"url_full_portrait")
                    hero_record['hero_sb_image'] = get_hero_images(hero.hero_id)
                    hero_record['hero_lg_image'] = get_hero_images(hero.hero_id,"url_large_portrait")
                    hero_record['hero_vert_image'] = get_hero_images(hero.hero_id,"url_vertical_portrait")
                    hero_record['games_played'] = hero.number_of_games
                    hero_record['win_rate'] = hero.win_rate
                    hero_record['total_avg_gpm'] = hero.total_avg_gpm
                    hero_record['gpm_for_win'] = hero.gpm_for_win
                    hero_record['gpm_for_lose'] = hero.gpm_for_lose
                    hero_record['last_24_hrs_win_rate'] = hero.last_24_hrs_win_rate
                    hero_record['last_24_hrs_win'] = hero.last_24_hrs_win
                    hero_record['last_24_hrs_lose'] = hero.last_24_hrs_lose

                    hero.hero_win_history.reverse()
                    hero_record['hero_win_history'] = hero.hero_win_history[-5:]
                    hero.hero_gpm_history.reverse()
                    if len(hero.hero_gpm_history)>=5:
                        hero.hero_gpm_history.append(100)
                        hero.hero_gpm_history.append(200)
                        hero.hero_gpm_history.append(300)
                        hero.hero_gpm_history.append(400)
                        hero.hero_gpm_history.append(500)
                        hero.hero_gpm_history.append(600)
                        hero.hero_gpm_history.append(700)
                        hero.hero_gpm_history.append(800)
                        hero.hero_gpm_history.append(900)
                    hero_record['hero_gpm_history'] = hero.hero_gpm_history[-14:]
                    index += 1
                    temp_obj.append(hero_record)

            json_text['hero_records'] = temp_obj

            objective_json = json_text


            return objective_json
        pass

def init_steam_api_key(name):
    global __steam_api_key__
    if not __steam_api_key__:
        __steam_api_key__ = name

    f = open('steam.config', 'r')
    for line in f:
        if "Key:" in line:
            __steam_api_key__ = line.split("Key:",1)[1].strip()

    print(__steam_api_key__)


def get_hero_name(hero_id):
    global __heroes__
    if not __heroes__ :

        with open("D:/PycharmProjects/dota2LobbyInfo/data/res/heroes.json", 'r') as file:
            content = file.read()
            __heroes__ = json.loads(content)


    for hero in __heroes__["heroes"]:
        if hero["id"]==hero_id:
            return hero["localized_name"]

    pass
def get_hero_images(hero_id,img_attr="url_small_portrait"):
    global __heroes__
    if not __heroes__ :

        with open("D:/PycharmProjects/dota2LobbyInfo/data/res/heroes.json", 'r') as file:
            content = file.read()
            __heroes__ = json.loads(content)

    for hero in __heroes__["heroes"]:
        if hero["id"]==hero_id:
            return hero[img_attr]

def get_player_summary(dota2_id,attribute="personaname"):
    api = dota2api.Initialise("4B1FD9D1888114755F2A9C7B5788A085")

    response = api.get_player_summaries(dota2_id)

    for item in response['players']:
        return (item[attribute])



if __name__ == "__main__":
    #medusa = MemberInfo(444025333)
    medusa = MemberInfo(132044155)
    print(medusa.member_id)

    medusa.process()
    medusa.output()
    print(medusa.to_json())
'''    get_player_summary(132044155)
    medusa = MemberInfo(132044155)
    print(medusa.member_id)
    medusa.process()
    medusa.output()
    print(medusa.to_json())
    print(get_hero_images(1,"url_large_portrait"))
    #get_game_details(3463314239)
    #print(os.getcwd())
    #objs = [HeroRecord(101,1,100),HeroRecord(201,2,100),HeroRecord(200,3,1000)]
    #objs = sorted(objs,key=attrgetter('number_of_games'),reverse=True)
    #for obj in objs:
    #    obj.output()
    pass
'''