import sqlite3
import threading,time
conn = None



def connect():

    connection = sqlite3.connect('D:/PycharmProjects/dota2LobbyInfo/data/game/game.db')

    return connection
def db_insert_match_details(match_id,match_details,is_processed=False):

    conn = connect()
    cursor = conn.cursor()


    statement = 'insert into steam_match_details (match_id,match_details) values (?,?)'
    cursor.execute(statement,(match_id,match_details))
    conn.commit()



def db_is_match_exist(match_id):

    conn = connect()
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

    conn = connect()
    cursor = conn.cursor()

    statement = 'select match_details from steam_match_details where match_id='+str(match_id)

    cursor.execute(statement)

    row = cursor.fetchone()
    conn.close()
    conn = None
    return row[0]


if __name__ == "__main__":

    threading._start_new_thread(print_out,("test123",))


    #dota_insert_match_details(123,'123')
    #dota_is_match_exist(123)
    #dota_get_match_details(123)