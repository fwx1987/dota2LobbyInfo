from util.algorithm import  _matrix_generation

class Lobby:

    number_of_player=0
    list_of_player_id=[]

    lobby_martix_initalized=False
    lobby_martix = {}  # to generate lobby matrix results.


    def __init__(self,list_of_player_id):
        self.list_of_player_id = list_of_player_id


    def get_lobby_matrix(self):
        if not self.lobby_martix_initalized:
            self.initialize_lobby_matrix()

        return self.lobby_martix

    def initialize_lobby_matrix(self):
        self.lobby_martix = _matrix_generation(self.list_of_player_id)

    def get_lobby_from_log_file(self):
        pass


if __name__ == "__main__":
    print("--start--")
    lobby = Lobby(['133032984','162841707'])

    print(lobby.get_lobby_matrix())