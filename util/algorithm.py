


#0:[U:1:158185566] 1:[U:1:133032984] 2:[U:1:162841707] 3:[U:1:177808283] 4:[U:1:59926482] 5:[U:1:288359932] 6:[U:1:250199729] 7:[U:1:218382405] 8:[U:1:341415872] 9:[U:1:841369277] 10:[U:1:65203195] 11:[U:1:250555028]) (Party 25836599751562058 0:[U:1:250555028])
list = ["132044155","133032984","162841707","177808283","59926482","288359932","250199729","218382405","218382405","341415872","841369277"]


for x in list:
    print(x)

from multiprocessing.dummy import Pool as ThreadPool

def _matrix_generation(list_of_player):
    if len(list_of_player) == 0 :

        return {}

    else:
        matrix = {}
        for player in list_of_player:
            matrix[player] = get_player_in_lobby_matrix(player, list_of_player)

        return matrix
    pass

def get_player_in_lobby_matrix(player,list_of_player):
    if player not in list_of_player:
        return None
    else:
        player_matrix =[]
        for x in list_of_player:
            if x==player:
                player_matrix.append(None)
            else:
                pool = ThreadPool(len(list_of_player))
                print("start")
                results = pool.map(result,"123")
                pool.close()
                pool.join()
                print(results)

                print("end")


                player_matrix.append(0.5)
        return player_matrix


def result(what):
    return what