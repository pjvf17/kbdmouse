import pyautogui
from pynput import keyboard
import sys
import math
import threading

# 
lock = threading.Lock()
sem = threading.Semaphore(2)
scrollLock = threading.Lock()
scrollSem = threading.Semaphore(2)

# will store the Listener object from pynput.keyboard, for use in stop() function
listener = None
# Stores which direction we're moving, vector of [x,y]
curAng = [0,0]
# Stores the speed at which we're moving
speed = 4
# Conttrols
hold = False
drag = False
pre = 1
paused = False
pauseKey = "y"
scrolling = 0
inScrollLoop = False
moving = False

# Stores a index of key, [hotkey] pairs
keyMemo = {}

def moveLoop():
    global pre
    global curSpeed
    global speed
    global drag
    global moving
    while (curAng[0] != 0 or curAng[1] != 0):
        pyautogui.PAUSE = 0
        curSpeed = speed * pre
        x, y = pyautogui.position()
        ogX = x
        ogY = y
        time = 0.01
        if (drag == True):
            pyautogui.mouseDown()
            curSpeed = curSpeed*100
            time = .3
            x,y = pyautogui.position()
        pyautogui.moveTo(x+curAng[0]*curSpeed,y+curAng[1]*curSpeed, time)
        if (drag == True):
            pyautogui.mouseUp()
            pyautogui.moveTo(ogX,ogY)
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

def reset():
    global curAng
    global speed
    curAng = [0,0]
    speed = 4

def speed_change(change,check=True, setVal=False):
    global pre
    global speed
    if (setVal):
        speed = change
        return
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

def macro1():
    xBound,yBound = pyautogui.size()
    x = xBound/2
    y = yBound/2

    pyautogui.PAUSE = 0
    pyautogui.moveTo(10,y, 0.01)
    for j in range (1):
        pyautogui.mouseDown(button="left")
        for i in range (7):
            pyautogui.moveTo(math.pow(i,4), y)
        pyautogui.mouseUp(button="left")
    pyautogui.PAUSE = 0.1
    
class HotKey:
    def __init__(self, press, release, priority = 0):
        self.press = press
        self.release = release
        self.pressed = False
        self.priority = priority

def click(button, press):
    if (press):
        pyautogui.mouseDown(button=button)
    else:
        pyautogui.mouseUp(button=button)

def moveToMap():
    x,y = pyautogui.size()
    pyautogui.moveTo(.83*x, 0.83*y)

def toggleHold():
    global hold
    hold = not hold
#     print(hold)

def toggleDrag():
    global drag
    drag = True

def center():
    x,y = pyautogui.size()
    pyautogui.moveTo(x/2,y/2)

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
    frozenset(('ctrl_r', 'g')): HotKey(stop,()),
    frozenset(('ctrl', 'g')): HotKey(stop,()),
    frozenset(('l')): HotKey(lambda: reset(), lambda:()),
    frozenset(('m')): HotKey(lambda: moveToMap(), lambda:()),
    frozenset((',')): HotKey(lambda: toggleHold(), lambda:()),
    frozenset(('.')): HotKey(lambda: center(), lambda:()),
    frozenset(('g')): HotKey(lambda: click("left", True), lambda: click("left", False)),
    # left
    frozenset(('o')): HotKey(lambda: angle(-1,0),lambda: dangle(-1,0, True)),
    # right
    frozenset(('e')): HotKey(lambda: angle(1,0), lambda: dangle(1,0, True)),
    # up
    frozenset(('t')): HotKey(lambda: angle(0,1), lambda: dangle(0,1, True)),
    # down
    frozenset(('n')): HotKey(lambda: angle(0,-1), lambda: dangle(0,-1, True)),
    frozenset({'shift'}): HotKey(lambda: speed_change(10, False), lambda: speed_change(-10, False)),
    frozenset({'shift_r'}): HotKey(lambda: speed_change(10, False), lambda: speed_change(-10, False)),
    frozenset({'h'}): HotKey(lambda: scroll(-10), lambda: scroll(-10),
                             priority=1),
    frozenset({'backspace'}): HotKey(lambda: scroll(10), lambda: scroll(-10)),
   # frozenset({'cmd'}): HotKey(lambda: scroll(10), lambda: scroll(-10)),
    #frozenset({'cmd_r'}): HotKey(lambda: scroll(10), lambda: scroll(-10)),
    # pause:
    frozenset(('ctrl_r', pauseKey)): HotKey(lambda: pause(),lambda: ()),
#    frozenset(('alt_r')): HotKey(lambda: speed_change(1, False, True), lambda: speed_change(4, False, True)),
    frozenset(('ctrl', pauseKey)): HotKey(lambda: pause(),lambda: ()),
 #   frozenset(('alt')): HotKey(lambda: speed_change(1, False, True), lambda: speed_change(4, False, True)),
    frozenset(('q')): HotKey(lambda: speed_change(5),lambda: ()),
    frozenset(('j')): HotKey(lambda: speed_change(-5),lambda: ()),
    frozenset(('k')): HotKey(lambda: toggleDrag(), lambda: ()),
    frozenset(('1')): HotKey(lambda: prefix(1), lambda: ()),
    frozenset(('2')): HotKey(lambda: prefix(2), lambda: ()),
    frozenset(('3')): HotKey(lambda: prefix(3), lambda: ()),
    frozenset(('4')): HotKey(lambda: prefix(4), lambda: ()),
    frozenset(('5')): HotKey(lambda: prefix(5), lambda: ()),
    frozenset(('6')): HotKey(lambda: prefix(6), lambda: ()),
    frozenset(('7')): HotKey(lambda: prefix(7), lambda: ()),
    frozenset(('8')): HotKey(lambda: prefix(8), lambda: ()),
    frozenset(('9')): HotKey(lambda: prefix(9), lambda: ()),
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
            if (bind[1].priority > 0):
                return
    print("end check section")
    
# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
