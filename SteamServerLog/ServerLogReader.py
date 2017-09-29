
class LatestLobby:
    raw_string=""


    def __init__(self, raw_string):
        self.raw_string = raw_string

    def output_raw(self):
        print(self.raw_string)

    def get_lobby_members(self):

        i=0
        str = self.raw_string.split("(",1)[1].split(")",1)


        #print(str[0])


        members = []
        members.append(self.between(self.raw_string, "0:[U:1:","]"))
        members.append(self.between(self.raw_string, "1:[U:1:", "]"))
        members.append(self.between(self.raw_string, "2:[U:1:", "]"))
        members.append(self.between(self.raw_string, "3:[U:1:", "]"))
        members.append(self.between(self.raw_string, "4:[U:1:", "]"))
        members.append(self.between(self.raw_string, "5:[U:1:", "]"))
        members.append(self.between(self.raw_string, "6:[U:1:", "]"))
        members.append(self.between(self.raw_string, "7:[U:1:", "]"))
        members.append(self.between(self.raw_string, "8:[U:1:", "]"))
        members.append(self.between(self.raw_string, "9:[U:1:", "]"))
        return members


    def between(self,value, a, b):
        # Find and validate before-part.

        pos_a = value.find(a)

        pos_b = pos_a+value[pos_a:].find(b)

        return value[pos_a+len(a):pos_b]
        if pos_a == -1: return ""
        # Find and validate after part.
        pos_b = value.lfind(b)
        if pos_b == -1: return ""
        # Return middle part.
        adjusted_pos_a = pos_a + len(a)
        if adjusted_pos_a >= pos_b: return ""
        return value[adjusted_pos_a:pos_b]





def get_lobby_members():
    #f = open('C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\dota\server_log.txt', 'r')
    f = open('D:\Files\PersonalFolders\Dota2\server_log.txt', 'r')
    lastline = ""
    for line in f:
        if "Lobby" in line:
            lastline = line
    last = LatestLobby(lastline)

    print(last.output_raw())
    print(last.get_lobby_members())
    return last.get_lobby_members()

if __name__ == "__main__":
    t=[]
    y=[]
    t = get_lobby_members()
    y = get_lobby_members()

    print (t==y)
