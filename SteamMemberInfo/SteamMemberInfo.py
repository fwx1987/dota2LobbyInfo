
import dota2api

__steam_api_key__= None

def init_steam_api_key(name):
    global __steam_api_key__
    if not __steam_api_key__:
        __steam_api_key__ = name

    f = open('steam.config', 'r')
    for line in f:
        if "Key:" in line:
            __steam_api_key__ = line.split("Key:",1)[1].strip()

    print(__steam_api_key__)



def get_member_game_history(user_dota2_id):
    print(user_dota2_id)
    pass

if __name__ == "__main__":
    print (__steam_api_key__)
    init_steam_api_key("89")
    get_member_game_history("218444811")
    api = dota2api.Initialise("4B1FD9D1888114755F2A9C7B5788A085")
    hist = api.get_match_history(account_id=218444811,matches_requested=10,min_players=10)
    print(api.get_heroes())

    print(hist)

