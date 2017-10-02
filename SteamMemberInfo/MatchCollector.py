import dota2api
import SteamMemberInfo
if __name__ == "__main__":
    api = dota2api.Initialise("4B1FD9D1888114755F2A9C7B5788A085")

    seq_num = 2945923382
    seq_num = seq_num +1
    count=100
    while(count>0):
        print('get match history from seq num: '+str(seq_num)+ " count:100")
        all = api.get_match_history_by_seq_num(seq_num,matches_requested = 100)
        print(all['status'])

        match_id = ""
        if all['status'] == 1:

            for match in all['matches']:
                match_id = match['match_id']
                SteamMemberInfo.get_game_details(match_id)
                seq_num = match['match_seq_num']

        else:
            print("stopped at "+str(seq_num))
            break
        count= count-1
    print("stopped at " + str(seq_num))


