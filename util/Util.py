import sqlite3
import threading,time

import requests
conn = None
__recent_match__ = None
__player_summary__ = None

def db_connect():

    connection = sqlite3.connect('D:/PycharmProjects/game.db')

    return connection
def db_insert_match_details(match_id,match_details,is_processed=False):

    conn = db_connect()
    cursor = conn.cursor()


    statement = 'insert into steam_match_details (match_id,match_details) values (?,?)'
    cursor.execute(statement,(match_id,match_details))
    conn.commit()



def db_is_match_exist(match_id):

    conn = db_connect()
    cursor = conn.cursor()

    statement = 'select * from steam_match_details where match_id='+str(match_id)

    cursor.execute(statement)

    if len(cursor.fetchall()) == 1:
        conn.close()
        conn = None
        return True
    else:
        conn.close()
        conn = None
        return False

def db_get_match_details(match_id):

    conn = db_connect()
    cursor = conn.cursor()

    statement = 'select match_details from steam_match_details where match_id='+str(match_id)

    cursor.execute(statement)

    row = cursor.fetchone()
    conn.close()
    conn = None
    return row[0]


def odota_get_recent_match(account_id):
    global __recent_match__
    r = requests.get("https://api.opendota.com/api/players/"+account_id+"/recentMatches")
    __recent_match__ = r.json()
    return __recent_match__


def odota_get_win_history(account_id):
    pass

def odota_get_gpm_history(account_id):
    pass

class Dota2Dict(dict):
    pass


if __name__ == "__main__":
    r = requests.get("https://api.opendota.com/api/players/132044155/recentMatches")
    print(r.json())


    #dota_insert_match_details(123,'123')
    #dota_is_match_exist(123)
    #dota_get_match_details(123)