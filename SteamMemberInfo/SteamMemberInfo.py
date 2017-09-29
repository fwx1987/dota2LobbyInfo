
import dota2api
import json,time,os
from operator import itemgetter,attrgetter

__steam_api_key__= None
__game_data__ = None


def get_member_game_history(user_dota2_id):
    api = dota2api.Initialise("4B1FD9D1888114755F2A9C7B5788A085")
    hist = api.get_match_history(account_id=user_dota2_id,matches_requested=100,min_players=10)
    return hist

def get_game_details(dota2_game_id):
    api = dota2api.Initialise("4B1FD9D1888114755F2A9C7B5788A085")
    global __game_data__
    if not __game_data__ or __game_data__['match_id'] !=  dota2_game_id:
        print("start to get game details"+str(dota2_game_id))
        __game_data__ =  api.get_match_details(match_id=dota2_game_id)

    #with open('file.txt', 'w') as file:
    #     file.write(json.dumps(__game_data__))

    #with open('file.txt', 'r') as file:
    #     content = file.read()
    #__game_data__ = json.loads(content)
    return __game_data__

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
    hero_id = 0
    number_of_games = 0
    win_rate = 0
    gpm_for_win = 0
    gpm_for_lose = 0

    def __init__(self,hero_id,win,gpm):
        self.hero_id = hero_id
        self.update_with_game(win,gpm)



    def update_with_game(self,win,gpm):
        #before update
        number_of_win = round(self.win_rate*self.number_of_games)
        number_of_lose = self.number_of_games-number_of_win

        #update
        self.number_of_games = self.number_of_games +1

        if win:
            self.win_rate = 100*((self.number_of_games -1)*self.win_rate/100+1)/self.number_of_games
            self.gpm_for_win = (number_of_win*self.gpm_for_win+gpm)/self.number_of_games
        else:
            self.win_rate = 100*((self.number_of_games -1)*self.win_rate/100-1)/self.number_of_games
            self.gpm_for_lose = (number_of_lose*self.gpm_for_lose+gpm)/self.number_of_games
    def output(self):
        print("hero id: "+str(self.hero_id))
        print("number of games: "+str(self.number_of_games))
        pass
class MemberInfo:
    #repostiory data
    member_id = ""
    member_raw_history = ""
    member_last_60_days_history =[]

    #all hero date
    number_heros_played = 0
    total_games = 0
    total_avg_gpm = 0
    total_win_rate = 0
    total_avg_gpm = 0
    total_avg_win_gpm =0
    total_avg_lose_gpm = 0

    #specific hero data
    hero_record = []

    def __init__(self,member_id):
        self.member_id = member_id
        self.member_raw_history = get_member_game_history(self.member_id)
        self.crawl_60_days_history()

    def crawl_60_days_history(self):

        print(self.member_raw_history)

        temp_list = self.member_raw_history['matches']

        for match in temp_list:


            if match['start_time'] >=time.time()-60*24*60*60 :

                self.member_last_60_days_history.append(match)
                pass
        print (self.member_last_60_days_history)

        print(len(self.member_last_60_days_history))
        #self.member_raw_history['status'] =1
        #self.member_raw_history['num_results'] = 41
        #self.member_raw_history['matches'] = list
        #print(json_str)
        #print (json_str['num_results'])

        pass

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
        fresh_hero = True

        number_of_match = len(self.member_last_60_days_history)
        for match in self.member_last_60_days_history:
            match_id = match['match_id']
            #get number of win games
            #get number of lose games
            is_win = is_game_player_win(match_id,self.member_id)
            hero_playing = get_game_player_hero(match_id,self.member_id)
            game_gpm = get_game_player_gpm(match_id,self.member_id)
            if is_win:
                number_of_win = number_of_win+1
                total_win_gpm = total_win_gpm + game_gpm
            else:
                number_of_lose = number_of_lose+1
                total_lose_gpm = total_lose_gpm + game_gpm
            #get total gpm for all heros
            total_gpm = total_gpm + game_gpm

            for hero in self.hero_record:
                if hero.hero_id == hero_playing:
                    fresh_hero = False
                    hero.update_with_game(is_win,game_gpm)

            if fresh_hero:
                self.hero_record.append(HeroRecord(hero_playing,is_win,game_gpm))

        #get overall statics for all heroes

        self.number_heros_played = len(self.hero_record)
        self.total_games = number_of_match
        self.total_avg_gpm = total_gpm / self.total_games

        self.total_avg_gpm = total_gpm / self.total_games
        self.total_win_rate = number_of_win *100 / self.total_games

        if number_of_win == 0:
            self.total_avg_win_gpm = 0
        else:
            self.total_avg_win_gpm = total_win_gpm/number_of_win

        if number_of_lose == 0:
            self.total_avg_lose_gpm = 0
        else:
            self.total_avg_lose_gpm = total_lose_gpm/number_of_lose

        self.sort_hero_record()


    def sort_hero_record(self):

        self.hero_record = sorted(self.hero_record,key=attrgetter('number_of_games'),reverse=True)
        pass

    def output(self):
        print(self.member_id)
        print(self.hero_record)

        print("total games:"+str(self.total_games))
        print("total hero played:"+str(self.number_heros_played))

        print("total avg gpm:"+str(self.total_avg_gpm))
        print("total win rate:"+str(self.total_win_rate))
        print("total avg win gpm"+str(self.total_avg_win_gpm))
        print("total avg lose gpm"+str(self.total_avg_lose_gpm))
        print("total number of heros record collected:"+str(len(self.hero_record)))

        for hero in self.hero_record:
            print ("hero id:"+str(hero.hero_id))
            print ("hero played times:"+str(hero.number_of_games))
            print ("hero win rate"+str(hero.win_rate))
            print ("gpm for win"+str(hero.gpm_for_win))
            print ("gpm for lose"+str(hero.gpm_for_lose))


def init_steam_api_key(name):
    global __steam_api_key__
    if not __steam_api_key__:
        __steam_api_key__ = name

    f = open('steam.config', 'r')
    for line in f:
        if "Key:" in line:
            __steam_api_key__ = line.split("Key:",1)[1].strip()

    print(__steam_api_key__)




if __name__ == "__main__":
    medusa = MemberInfo(218444811)
    #print(medusa.member_id)
    medusa.process()
    medusa.output()

    #get_game_details(3463314239)
    #print(os.getcwd())

    #objs = [HeroRecord(101,1,100),HeroRecord(201,2,100),HeroRecord(200,3,1000)]

    #objs = sorted(objs,key=attrgetter('number_of_games'),reverse=True)

    #for obj in objs:
    #    obj.output()

    pass


