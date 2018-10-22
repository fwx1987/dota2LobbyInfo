import os,socket
import time,logging,logging.handlers
date_today = time.strftime('%Y%m%d')
log_file = "log/Nvidia_recorder_"+date_today+".log"
handler = logging.handlers.RotatingFileHandler(log_file, maxBytes = 1024*1024, backupCount = 5) # 实例化handler
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
formatter = logging.Formatter(fmt)   # 实例化formatter
handler.setFormatter(formatter)      # 为handler添加formatter
logger = logging.getLogger('ServerLogReader')  # 获取名为tst的logger
logger.addHandler(handler)  # 为logger添加handler
logger.setLevel(logging.DEBUG)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)
logger.addHandler(consoleHandler)

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


def get_server_log_file():
    if socket.gethostname() == "DESKTOP-Wenxiang":
        f1 = 'C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\dota\server_log.txt'
        f2 = 'C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\dota\server_log.txt'
    else:
        f1 = 'C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\dota\server_log.txt'
        f2 = 'C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\dota\server_log.txt'
    f =open(f1,'r')
    if os.stat(f1).st_mtime > os.stat(f2).st_mtime:
        f = open(f1,'r')
    else:
        f = open(f2,'r')
    return f


def get_lobby_members():
    #tasks = os.popen("tasklist | findstr dota2.exe")


    lastline = ""
    for line in get_server_log_file:
        if "Lobby" in line:
            lastline = line
    last = LatestLobby(lastline)


    return last.get_lobby_members()

def get_player_status():
    status = ""

    tasks = os.popen("tasklist | findstr dota2.exe")
    if len(os.popen("tasklist |findstr dota2.exe").read()) <= 0:
        #logger.info("dota2.exe is found")
        return "game_not_started"
    for line in get_server_log_file():
        if "Lobby" in line:
            status = "in_game"
            if "10:[U:1:" in line:
                status = status+"_watching"
        if "loopback:" in line:
            status = "idle"
    logger.info("player is in status:"+status+"")
    return status

if __name__ == "__main__":
    t = get_lobby_members()

    player_slot=0

    for member in t:
        print(member)

