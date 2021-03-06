import sqlite3

conn = None
__recent_match__ = None
__player_summary__ = None

def db_connect():

    connection = sqlite3.connect('D:/PycharmProjects/game.db')

    return connection
def db_insert_match_details(match_id,match_details,is_processed=False):

    conn = db_connect()
    cursor = conn.cursor()

    try:
        statement = 'insert into steam_match_details (match_id,match_details) values (?,?)'
        cursor.execute(statement,(match_id,match_details))
        conn.commit()
    except Exception as e:
        conn.close()
        conn = None
        print (str(e) +"match id: "+str(match_id))


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





def odota_get_win_history(account_id):
    pass

def odota_get_gpm_history(account_id):
    pass

class Dota2Dict(dict):
    pass


if __name__ == "__main__":
    pass


    #dota_insert_match_details(123,'123')
    #dota_is_match_exist(123)
    #dota_get_match_details(123)