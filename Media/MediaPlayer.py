import pygame,os
import time



def play_music(filename):

    pygame.mixer.init()
    if filename == "":
        pygame.mixer.music.load(os.path.join(os.getcwd(),"Media","Chat_wheel_2017_frog.mp3"))
        pygame.mixer.music.play()
    else:
        pygame.mixer.music.load(os.path.join(os.getcwd(), "Chat_wheel_2017_frog.mp3"))
        pygame.mixer.music.play()

    print("1:"+str(time.time()))
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    print("2:" + str(time.time()))
if __name__ == "__main__":

    time.sleep(10)
    print("0:" + str(time.time()))
    play_music("Chat_wheel_2017_frog.mp3")
    time.sleep(10)
    print("0:" + str(time.time()))
    play_music("Chat_wheel_2017_frog.mp3")
    time.sleep(10)
    print("0:" + str(time.time()))
    play_music("Chat_wheel_2017_frog.mp3")
    time.sleep(10)
    print("0:" + str(time.time()))
    play_music("Chat_wheel_2017_frog.mp3")
    time.sleep(10)
    print("0:" + str(time.time()))
    play_music("Chat_wheel_2017_frog.mp3")
    time.sleep(10)
    print("0:" + str(time.time()))
    play_music("Chat_wheel_2017_frog.mp3")