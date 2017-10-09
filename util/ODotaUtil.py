import requests,time,json
__player_refreshed__ = None
__player_data__ = None
__recent_match__ =None
__heroes__ = None

def odota_get_recent_match(account_id):
    global __recent_match__,__player_refreshed__,__player_data__

    if __player_refreshed__ != account_id:
        odota_refresh_player(account_id)




    odota_get_player(account_id)


    r = requests.get("https://api.opendota.com/api/players/"+str(account_id)+"/recentMatches")
    __recent_match__ = r.json()
    return __recent_match__


def odota_get_player(account_id):
    global __player_data__
    if odota_refresh_player(account_id):
        r = requests.get("https://api.opendota.com/api/players/"+str(account_id))

        if r.status_code == 200:
            __player_data__ = r.json()

            return __player_data__


def odota_refresh_player(account_id):
    global __player_refreshed__
    if __player_refreshed__ == None or __player_refreshed__!=account_id:
        r = requests.post("https://api.opendota.com/api/players/"+str(account_id)+"/refresh")
    else:
        return True

    if r.status_code == 200:
        __player_refreshed__ = account_id
        return True
    else:
        return False


def odota_get_hero_name(hero_id):
    global __heroes__
    if not __heroes__ :

        with open("D:/PycharmProjects/dota2LobbyInfo/data/res/heroes.json", 'r') as file:
            content = file.read()
            __heroes__ = json.loads(content)


    for hero in __heroes__["heroes"]:
        if hero["id"]==hero_id:
            return hero["localized_name"]

    pass
def odota_get_hero_images(hero_id,img_attr="url_small_portrait"):
    global __heroes__
    if not __heroes__ :

        with open("D:/PycharmProjects/dota2LobbyInfo/data/res/heroes.json", 'r') as file:
            content = file.read()
            __heroes__ = json.loads(content)

    for hero in __heroes__["heroes"]:
        if hero["id"]==hero_id:
            return hero[img_attr]

class Player:

    def __init__(self,account_id):
        self.account_id = account_id
        self.player_data = odota_get_player(account_id)
        self.recent_match_data = odota_get_recent_match(account_id)
        self.name = ""
        self.avatar = ""
        self.solo_mmr = 0
        self.group_mmr = 0
        self.mmr_estimate = 0
        self.recent_match = []
        self.gpm_hisotry = []
        self.matches_win_history = []
        self.is_processed =  False

    def process_odota_data(self):

        #player info
        try:
            self.name = self.player_data['profile']['personaname']
        except KeyError as e:
            pass

        try:
            self.avatar = self.player_data['profile']['avatar']

        except KeyError as e:
            pass
        self.solo_mmr = self.player_data['solo_competitive_rank']
        self.group_mmr = self.player_data['competitive_rank']

        try:

            self.mmr_estimate = self.player_data['mmr_estimate']['estimate']
        except Exception:
            self.mmr_estimate = 0

        self.recent_match = []
        self.gpm_hisotry = []
        self.matches_win_history = []


        #recent match info, maximum 5 matches
        index = 0
        for match in self.recent_match_data:
            if index<5:
                #get match win history
                if match['player_slot'] <50:
                    if match['radiant_win']:
                        match['win_lose'] = 1
                        self.matches_win_history.append(1)
                    else:
                        match['win_lose'] = -1
                        self.matches_win_history.append(-1)
                else:
                    if match['radiant_win']:
                        match['win_lose'] = -1
                        self.matches_win_history.append(-1)
                    else:
                        match['win_lose'] = 1
                        self.matches_win_history.append(1)


                if match['start_time']>time.time()-2*24*60*60:
                    if match['start_time']>time.time()-8*60*60:
                        match['period'] = "last_8hrs"
                    else:
                        if match['start_time']>time.time()-24*60*60:
                            match['period'] = "last_1day"
                        else:
                            match['period'] = "last_2days"
                    self.gpm_hisotry.append(match['gold_per_min'])
                    self.recent_match.append(match)
                else:

                    match['period'] = "2days before"
                    self.gpm_hisotry.append(match['gold_per_min'])
                    self.recent_match.append(match)

                index+=1

        self.is_processed = True

    def to_html_source_json(self):
        if self.is_processed == False:
            self.process_odota_data()
        result = []
        json_text ={}
        json_text['name']= self.name
        json_text['account_id']= self.account_id
        json_text['avatar']= self.avatar
        json_text['solo_mmr']= self.solo_mmr
        json_text['group_mmr']= self.group_mmr
        json_text['mmr_estimate']= self.mmr_estimate
        self.matches_win_history.reverse()
        json_text['matches_win_history']= self.matches_win_history
        json_text['gpm_hisotry']=self.gpm_hisotry
        json_text['class'] = "player"

        result.append(json_text)

        #simply retrun all match details for html to process
        for match in self.recent_match:
            match['hero_name'] = odota_get_hero_name(match['hero_id'])
            match['hero_img'] = odota_get_hero_images(match['hero_id'])
            match['class']="hero"

            result.append(match)

        return result

if __name__ == "__main__":
    odota_get_player(132044155)