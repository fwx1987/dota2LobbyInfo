import sqlite3


conn = None



def connect():
    global conn
    if conn == None:
        conn = sqlite3.connect('D:/PycharmProjects/dota2LobbyInfo/data/game/game.db')

    return conn
def dota_insert_match_details(match_id,match_details,is_processed=False):
    global conn,cursor

    if conn == None or cursor ==None:
        conn = connect()
        cursor = conn.cursor()


    statement = 'insert into steam_match_details (match_id,match_details) values (?,?)'
    cursor.execute(statement,(match_id,match_details))
    conn.commit()



def dota_is_match_exist(match_id):
    global conn,cursor

    if conn == None or cursor ==None:
        conn = connect()
        cursor = conn.cursor()

    statement = 'select * from steam_match_details where match_id='+str(match_id)

    cursor.execute(statement)

    if len(cursor.fetchall()) == 1:

        return True
    else:

        return False

def dota_get_match_details(match_id):
    global conn,cursor

    if conn == None or cursor ==None:
        conn = connect()
        cursor = conn.cursor()

    statement = 'select match_details from steam_match_details where match_id='+str(match_id)

    cursor.execute(statement)

    row = cursor.fetchone()
    return row[0]



if __name__ == "__main__":

    #dota_insert_match_details(123,'123')
    #dota_is_match_exist(123)
    dota_get_match_details(123)