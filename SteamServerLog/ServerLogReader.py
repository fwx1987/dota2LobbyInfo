import os,socket
import time,logging,logging.handlers
import config,sys

config.get_root_directory()


logger = logging.getLogger(__name__)


#recommended setting:
# 1080 p 60 FPS, 20m bitrate.
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

    if sys.platform == "win32":
        pass
    #HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Steam App 570
        import errno, os, winreg
        proc_arch = os.environ['PROCESSOR_ARCHITECTURE'].lower()

        if proc_arch == 'x86' or proc_arch == 'amd64':
            arch_keys = {winreg.KEY_WOW64_32KEY, winreg.KEY_WOW64_64KEY}
        else:
            raise Exception("Unhandled arch: %s" % proc_arch)

        for arch_key in arch_keys:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", 0, winreg.KEY_READ | arch_key)
            for i in range(0, winreg.QueryInfoKey(key)[0]):
                skey_name = winreg.EnumKey(key, i)
                skey = winreg.OpenKey(key, skey_name)
                try:
                    #print(winreg.QueryValueEx(skey, 'DisplayName')[0])
                    #print(winreg.QueryValueEx(skey, 'InstallLocation')[0])
                    if winreg.QueryValueEx(skey, 'DisplayName')[0] == "Dota 2":
                        log_file = winreg.QueryValueEx(skey, 'InstallLocation')[0] +"\\game\\dota\\server_log.txt"
                        logger.debug("get dota2 log file at :"+log_file)
                        return open(log_file,'r')

                except OSError as e:
                    if e.errno == errno.ENOENT:
                        # DisplayName doesn't exist in this skey
                        pass
                finally:
                    skey.Close()
        return None
    else:
        raise Exception ("Unknown platform detected:"+str(sys.platform))
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
    for line in get_server_log_file():
        if "Lobby" in line:
            lastline = line
    last = LatestLobby(lastline)

    logger.info("get lobby info as :"+str(last.get_lobby_members()))

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
    logger.info("test")
    player_slot=0

    for member in t:
        print(member)

