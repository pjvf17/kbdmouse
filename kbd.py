import pyautogui
from pynput import keyboard
import sys
import math
import threading
import asyncio

# 
lock = threading.Lock()
sem = threading.Semaphore(2)
scrollLock = threading.Lock()
scrollSem = threading.Semaphore(2)

# will store the Listener object from pynput.keyboard, for use in stop() function
listener = None
# Stores which direction we're moving, vector of [x,y]
curAng = [0,0]
SPEED_DEFAULT = 4.0
# Stores the speed at which we're moving
speed = SPEED_DEFAULT
# Conttrols
hold = False
drag = False
pre = 1.0
paused = False
pauseKey = "'"
scrolling = 0
inScrollLoop = False
moving = False
# Gets the original location of X and Y, Used so that we can store
# floating point loacations even though you can't have the mouse in
# half a pixel
X, Y = pyautogui.position()

# Stores a index of key, [hotkey] pairs
keyMemo = {}

def moveLoop():
    global pre
    global speed
    global drag
    global moving
    global X
    global Y
    while (curAng[0] != 0 or curAng[1] != 0):
        pyautogui.PAUSE = 0
        curSpeed = speed * pre
        ogX = X
        ogY = Y
        if (drag == True):
            pyautogui.mouseDown()
            curSpeed = curSpeed*100
            time = .3
            X,Y = pyautogui.position()
        X = X+curAng[0]*curSpeed
        Y = Y+curAng[1]*curSpeed
        pyautogui.moveTo(X+curAng[0]*curSpeed,Y+curAng[1]*curSpeed)
        if (drag == True):
            pyautogui.mouseUp()
            pyautogui.moveTo(ogX,ogY)
            X,Y = pyautogui.position()            
        drag = False
        pre = 1
    moving = False
    
def scrollLoop():
    global scrolling
    global inScrollLoop
    while (scrolling != 0):
        pyautogui.scroll(scrolling)
    inScrollLoop = False

def lockScroll():
    global scrollLock
    global inScrollLoop
    global scrollSem
    r1 = scrollSem.acquire(blocking=False)
    if (r1):
        r2 = scrollLock.acquire()
        if (inScrollLoop == False):
            inScrollLoop = True
            t = threading.Thread(target=scrollLoop)
            t.start()
            t.join()
            scrollSem.release()
            scrollLock.release()
        else:
            scrollLock.release()
            scrollSem.release()
        
def scroll(amt, hold=True):
    global pre
    global scrolling
    if (hold):
        scrolling = amt if scrolling == 0 else 0
        t = threading.Thread(target=lockScroll)
        t.start()
        return
    pyautogui.scroll(amt*pre)
    pre = 1
        
def lockAngle():
    global lock
    global sem
    global moving
    # Outer doesn't block
    r1 = sem.acquire(blocking=False)
    if (r1):
        # Inner does, allowing percisely one thread to wait for moveLoop to complete
        r2 = lock.acquire()
        if (moving == False):
            moving = True
            t = threading.Thread(target=moveLoop)
            t.start()
            t.join()
            sem.release()
            lock.release()
        else:
            lock.release()
            sem.release()
        
def angle(x,y):
    global curAng
    global moving
    global lock
    curAng[0] += x
    curAng[1] += y
    t = threading.Thread(target=lockAngle)
    t.start()
    
def dangle(x,y, checkHold):
    global curAng
    global hold
    if ((checkHold == True and hold == False) or checkHold == False):
        curAng[0] -= x
        curAng[1] -= y
        t = threading.Thread(target=lockAngle)
        t.start()

def resetAngle():
    global curAng
    curAng = [0,0]

def resetSpeed():
    global speed
    speed = SPEED_DEFAULT

def resetHold():
    global hold
    hold = False

def reset():
    resetHold()
    resetAngle()
    resetSpeed()
    


def speedChange(change,check=True, setVal=False):
    global pre
    global speed
    if (setVal):
        speed = change
        return
    # If check is on (default), then the amount speed changes is based off current speed
    # It will change more at higher pre values, and less at lower
    if (check):
        if (change > 0):
            speed = speed + change*pre if speed > 5 else speed + 1*pre
        if (change < 0):
            speed = speed + change*pre if speed > 5 else speed - 1*pre
    else:
        speed = speed + change*pre
    pre = 1

def stop():
    global listener
    listener.stop()
    sys.exit()

def prefix(i):
    global pre
    pre = i

# def macro1():
#     xBound,yBound = pyautogui.size()
#     x = xBound/2
#     y = yBound/2

#     pyautogui.PAUSE = 0
#     pyautogui.moveTo(10,y, 0.01)
#     for j in range (1):
#         pyautogui.mouseDown(button="left")
#         for i in range (7):
#             pyautogui.moveTo(math.pow(i,4), y)
#         pyautogui.mouseUp(button="left")
#     pyautogui.PAUSE = 0.1

def click(button, press):
    if (press):
        pyautogui.mouseDown(button=button)
    else:
        pyautogui.mouseUp(button=button)

def moveToMap():
    global X
    global Y
    moveTo(.83,.83);

def moveTo(x, y, perc=True):
    global X
    global Y
    
    if (perc):
        xBound,yBound = pyautogui.size()
        pyautogui.moveTo(xBound*x,yBound*y);
    else:
        pyautogui.moveTo(x,y);
    X,Y = pyautogui.position();
    
def toggleHold():
    global hold
    hold = not hold
    if (not hold): resetAngle()
#     print(hold)

def toggleDrag():
    global drag
    drag = True

def center():
    global X
    global Y
    x,y = pyautogui.size()
    pyautogui.moveTo(x/2,y/2)
    X,Y = pyautogui.position();

def pause():
    global paused
    global curAng
    global scrolling
    global moving
    global inScrollLoop
    paused = not paused
    scrolling = 0
    curAng = [0,0]
    inScrollLoop = False
    moving = False
    # If paused, reset all keybinds
    if (paused):     
        for hotkey in hotkeys:
            hotkeys[hotkey].pressed = False
    print("in pause function")

    
# function lookup table for HotKey init
actions = {
    "angle": angle,
    "dangle": dangle,
    "reset": reset,
    "moveTo": moveTo,
    "center": center,
    "speedChange": speedChange,
    "toggleHold": toggleHold,
    "click": click,
    "pause": pause,
    "quit": stop,
    "scroll": scroll,
}

actionsKeys = list(actions.keys())

actionArgs = {
    "angle": ["x", "y"],
    "dangle": ["x", "y"],
    "reset": [],
    "moveTo": ["x", "y", "perc"],
    "center": [],
    "speedChange": ["change", "check", "setVal"],
    "toggleHold": [],
    "click": ["button", "press"],
    "pause": [],
    "quit": [],
    "scroll": ["amount", "hold"],
}

class HotKey:
    def __init__(self, press, release, pressArgs=None, releaseArgs=None, priority = 0):
        self.pressString = press
        self.releaseString = release
        self.pressArgs = pressArgs
        self.releaseArgs = releaseArgs
        self.press = self.create_action_lambda(press, pressArgs)
        self.release = self.create_action_lambda(release, releaseArgs)
        self.pressed = False
        self.priority = priority

    def create_action_lambda(self, action, args):
        if action is None:
            return lambda: ()
        if args is None:
            # print(action)
            return lambda: actions.get(action)()
        return lambda: actions.get(action)(*args)
        
    def __repr__(self):
        return f"""press={self.pressString}{f', args: {self.pressArgs}' if self.pressArgs is not None else ''} | release={self.releaseString}, {f'args: {self.releaseArgs}' if self.releaseArgs is not None else ''}"""



#1: oeuhtn
#1.5: i
#2: \qjkm
#3: ',.pgl
#4: yfidxb
#5: 123456789

# asdwrzc reserved (unfortunately)

# shift + #1, etc

# oeuhtn
# uh = scroll up, down
# o = left, e = right
# t = up, n = down
# \qjkm
# m = map
# q, = speed up, j = speed down
# k, followed by direction, short drag

# ',.pgl
# g = click
# l = reset movement
# , = hold
# . = center

# 123456789: prefix for repitition/magnitude    

# Define hotkey with set: action (func, or something else? I think func)
hotkeys = {
    frozenset(('ctrl_r', 'g')): HotKey("stop", "stop"),
    frozenset(('ctrl', 'g')): HotKey("stop", "stop"),
    frozenset(('l')): HotKey("reset", None),
    frozenset(('m')): HotKey("moveTo", None, pressArgs=[.83,.83]),
    frozenset(('f')): HotKey("moveTo", None, pressArgs=[0.05, 0.5]),
    frozenset(('c')): HotKey("moveTo", None, pressArgs=[0.95, 0.5]),
    frozenset((',')): HotKey("toggleHold", None),
    frozenset(('.')): HotKey("center", None),
    frozenset(('g')): HotKey("click", "click", pressArgs=["left", True], releaseArgs=["left", False]),
    # left
    frozenset(('o')): HotKey("angle", "dangle", pressArgs=[-1, 0], releaseArgs=[-1, 0, True]),
    # right
    frozenset(('e')): HotKey("angle", "dangle", pressArgs=[1, 0], releaseArgs=[1, 0, True]),
    # up
    frozenset(('t')): HotKey("angle", "dangle", pressArgs=[0, 1], releaseArgs=[0, 1, True]),
    # down
    frozenset(('n')): HotKey("angle", "dangle", pressArgs=[0, -1], releaseArgs=[0, -1, True]),
    frozenset({'shift'}): HotKey("speedChange", "speedChange", pressArgs=[10, False], releaseArgs=[SPEED_DEFAULT, False, True]),
    frozenset({'\\'}): HotKey("speedChange", "speedChange", pressArgs=[50, False, True], releaseArgs=[SPEED_DEFAULT, False, True]),
    frozenset({'u'}): HotKey("speedChange", "speedChange", pressArgs=[0.6, False, True], releaseArgs=[SPEED_DEFAULT, False, True]),
    frozenset({'h'}): HotKey("scroll", "scroll", pressArgs=[-15], releaseArgs=[-15], priority=1),
    frozenset({'k'}): HotKey("scroll", "scroll", pressArgs=[-15], releaseArgs=[-15], priority=1),
    frozenset({'backspace'}): HotKey("scroll", "scroll", pressArgs=[15], releaseArgs=[-15]),
    frozenset(('ctrl_r', pauseKey)): HotKey("pause", None),
    frozenset(('ctrl', pauseKey)): HotKey("pause", None),
    # frozenset(('1')): HotKey("prefix", None, pressArgs=[1]),
    # frozenset(('2')): HotKey("prefix", None, pressArgs=[2]),
    # frozenset(('3')): HotKey("prefix", None, pressArgs=[3]),
    # frozenset(('4')): HotKey("prefix", None, pressArgs=[4]),
    # frozenset(('5')): HotKey("prefix", None, pressArgs=[5]),
    # frozenset(('6')): HotKey("prefix", None, pressArgs=[6]),
    # frozenset(('7')): HotKey("prefix", None, pressArgs=[7]),
    # frozenset(('8')): HotKey("prefix", None, pressArgs=[8]),
    # frozenset(('9')): HotKey("prefix", None, pressArgs=[9]),
}


pressed = set(())

# Return an array of hotkeys that 'key' is in
def setsContainingKey(key):
    # If already found, return
    if (keyMemo.get(key, -1) != -1):
        return keyMemo.get(key)
    # Otherwise loop through all hotkeys
    for hotkey in hotkeys:
        if (key in hotkey):
            # If not yet made an array, make one
            if (keyMemo.get(key, -1) == -1):
                keyMemo[key] = [[hotkey, hotkeys[hotkey]]]
            # else just append
            else:
                keyMemo[key].append([hotkey, hotkeys[hotkey]])
    return keyMemo.get(key)
    
def on_press(key):
    print("press: ", key)
    try:
        pressed.add(key.name)
        keybind_check(key.name, True, pressed)
        print("after add: ", pressed)
    except AttributeError:
        pressed.add(key.char.lower())
        keybind_check(key.char.lower(), True, pressed)
        print("after add: ", pressed)
    except Exception as e:
        print(e)
        return

def on_release(key):
    # Catching weird error
    if(hasattr(key, "char") and key.char == None):
        print("weird?: ", key)
        return
    try:
        print("release: ", key)
        if(hasattr(key, "name")):
            keybind_check(key.name, False, pressed)
            pressed.remove(key.name)
        if(hasattr(key, "char")):
            keybind_check(key.char.lower(), False, pressed)
            pressed.remove(key.char.lower())
        print("after release: ", pressed)
    except Exception as e:
        print(e)
        

# press = true, false
def keybind_check(key,press, pressed):
    global paused
    sets = setsContainingKey(key)
    if (sets == None):
        return
    # Special check for pause keybind
    # Allow a passthrow to keybind check while paused iff
    # key == pausekey && press
    if (paused and (key != pauseKey or not press)):
        return
    for bind in sets:
        if (bind[0].issubset(pressed)):
            if (press):
                if (bind[1].pressed == False):
                    print("in")
                    bind[1].pressed = True
                    bind[1].press()
            else:
                bind[1].release()
                bind[1].pressed = False
            # honestly not sure what this is doing   
            if (bind[1].priority > 0):
                return
    print("end check section")

# Collect events until released
def run():
    with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
        listener.join()