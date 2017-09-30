from SteamServerLog import ServerLogReader
from SteamMemberInfo import SteamMemberInfo
import os


def output_json_to_file(json_obj, file):

    if os.path.exists(file):
        print("file exist, deleting:" )
        os.remove(file)


    with open(file, 'w') as file:
        file.write(json_obj)

    pass


if __name__ == "__main__":
    latest = ServerLogReader.get_lobby_members()

    index = 0
    for player in latest:
        print(player)
        medusa = SteamMemberInfo.MemberInfo(int(player))
        medusa.process()
        medusa.output()

        print(medusa.to_json())
        output_json_to_file(medusa.to_json(),"D:/PycharmProjects/report/player"+str(index)+ ".json")
        index +=1

    '''
    medusa = SteamMemberInfo.MemberInfo(444025333)
    medusa.process()
    medusa.output()
    print(medusa.to_json())
    '''
