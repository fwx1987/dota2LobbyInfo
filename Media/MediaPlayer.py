import pygame,os



def play_music(filename):

    pygame.mixer.init()

    print(os.path.exists("Chat_wheel_2017_frog.mp3"))


    pygame.mixer.music.load("Chat_wheel_2017_frog.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


if __name__ == "__main__":
    play_music("Chat_wheel_2017_frog.mp3")