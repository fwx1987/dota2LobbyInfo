from pynput.keyboard import Key, Listener as KeyListener
from pynput.mouse import Listener as MouseListener
import json
import time

key_seq = []

def on_press(key):
    print('{0} pressed'.format(
        key))
    global key_seq
    key_seq.append(key)

def on_release(key):
    print('{0} release'.format(
        key))
    if key == Key.esc:
        # Stop listener
        return False

def on_move(x, y):
    print('Pointer moved to {0}'.format(
        (x, y)))

def on_click(x, y, button, pressed):
    print('{0} at {1} button'.format(
        'Pressed' if pressed else 'Released',
        (x, y)))
    print(button)
    global key_seq
    if pressed:
        key_seq.append(button.name)

    '''if not pressed:
        # Stop listener
        return False
    '''
def on_scroll(x, y, dx, dy):
    print('Scrolled {0}'.format(
        (x, y)))
# Collect events until released

'''with KeyListener(
        on_click=on_click,
        on_scroll=on_scroll,
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
'''

def append_balls(current_balls,key):
    pass

def append_skills(current_skills,key):
    pass

key_listener = KeyListener(
        on_press=on_press,
        on_release=on_release)

mouse_listener = MouseListener(
        on_click=on_click,

        on_release=on_release)

key_listener.start()
mouse_listener.start()

start_time = time.time()

while (time.time() - start_time) < 8 * 60 * 60:
    time.sleep(6)

    current_balls = []
    current_skills = []
    last_key = None
    skill_D = None
    skill_F = None
    if (len(key_seq)!=0):
        key = key_seq.pop(0)
        if key=='left':
            if last_key == 'd' or last_key =='f':
                pass
            else:
                pass
        if key== 'q' or key=='w' or key=='e':
            current_balls = append_balls(current_balls,key)
        if key=='r':
            current_skills = append_skills(current_skills,key)
        if key=='d' or key=='f':

            pass

        if last_key is None:
            pass
        else:
            last_key= key


class Invoker:
    current_balls = []
    current_skills = []
    skill_D = None
    skill_F = None

    skills = []
    cool_down =[]
    img =[]
    skill_cast=[]

    ##https://dota2.gamepedia.com/Invoker

    def __init__(self):
        with open("sample.json", 'r') as file:
            content = json.loads(file.read())
            for skill in content:
                self.skills.append(skill['skill_name'])
                self.cool_down.append(skill['cool_down'])
                self.skill_cast.append(skill['skill_cast'])
                self.img.append(skill['img'])

    def invoke_ball(self,key):
        if len(self.current_balls)!=3:
            print('error, ball number incorrect')

        self.current_balls.sort()
        pass

    def invoke_skill(self):
        self.skill_F = self.skill_D

        pass
    def cast_skill(self):
        pass
