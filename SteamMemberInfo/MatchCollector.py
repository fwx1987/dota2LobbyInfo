import dota2api
import SteamMemberInfo
import threading
import time
def collect_match_details(threadname,start_sequence_num,end_sequence_num):
    api = dota2api.Initialise("4B1FD9D1888114755F2A9C7B5788A085")
    seq_num = start_sequence_num
#2945963526


    while (seq_num < end_sequence_num):
        try:

            print("thread:"+str(threadname) +" get match history from seq num: " + str(seq_num) + " count:100")
            all = api.get_match_history_by_seq_num(seq_num, matches_requested=100)


            match_id = ""
            if all['status'] == 1:

                for match in all['matches']:
                    match_id = match['match_id']
                    SteamMemberInfo.get_game_details(match_id)
                    seq_num = match['match_seq_num']

            else:
                print("stopped at " + str(seq_num))
                break

            if seq_num>end_sequence_num:
                break

        except Exception as e:
            print("thread:"+str(threadname) +" " +str(e))
            pass
            #with open("seq_num", 'a') as file:
            #    file.write("start at:" + str(start_sequence_num) + " and ends at: " + str(seq_num))



    print("stopped at " + str(seq_num))
    with open("seq_num", 'a') as file:
        file.write("start at:"+str(start_sequence_num) + " and ends at: "+str(seq_num))

class collectorThread (threading.Thread):
   def __init__(self, threadID, name, start_seq,end_seq):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.start_seq = start_seq
      self.end_seq = end_seq

   def run(self):
      print ("Starting " + self.name)
      collect_match_details(self.name, self.start_seq,self.end_seq)
      print ("Exiting " + self.name)


if __name__ == "__main__":
    '''    collect_match_details("test",2945965711,2945966711) 

    seq = 2945970601

    increase = 500

    thread1 = collectorThread(1,"thread-1",seq,seq+increase)
    seq = seq+increase
    thread2 = collectorThread(2, "thread-2", seq,seq+increase)


    print("start time is "+str(time.time()))
    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    print("end time is " + str(time.time()))
    pass
    

 '''

    api = dota2api.Initialise("4B1FD9D1888114755F2A9C7B5788A085")
    api.get_match_history_by_seq_num()


