import mouse
import keyboard
import time
import win32api, win32con
import PySimpleGUI as sg
import math
import winsound

#Sound
f1 = 1200  # Set Frequency 
f2 = 800
f3 = 2000
f_m1 = 523
f_m2 = 587
f_m3 = 659
f2 = 800
d1 = 500  # Set Duration
d2 = 1000


# No Recoil State
isNoRecoil = False
# is M key pressed
isMkeyPressed = False
# is tab key pressed
isTabkeyPressed = False
#is UI Open
isUIOpen = False

# Weapon Mode
WeaponMode = "Auto"
#Recoil Alleviation Parameters
ra_1 = 5
ra_2 = 5
ra_3 = 5

#Measuring Point
point_1=[0,0]
point_2=[0,0]
#Matching Point
match_1=[0,0]
match_2=[0,0]

#Measuring / Matching mode switch parameters
isMeasuring = False
isMatching = False

#index of inputing point
i_point = 1
m_point = 1

#Pixel distance % Real Distance
mDistance = 0
realDistance = 0

#Conversion Scale
scale=0

def SetRecoilParameters(x1,x2,x3):

    layout = [[sg.Text('Please Input Recoil Alleviation Parameters')],      
                 [sg.Text('Auto')],    
                 [sg.Slider(range=(1, 100), orientation='h', size=(34, 20), default_value=x1)],
                 [sg.Text('Semi')],
                 [sg.Slider(range=(1, 100), orientation='h', size=(34, 20), default_value=x2)],
                 [sg.Text('Semi-ForcedAuto')],
                 [sg.Slider(range=(1, 100), orientation='h', size=(34, 20), default_value=x3)],
                 [sg.Text('   ')],
                 [sg.Submit(), sg.Cancel()]]     

    window = sg.Window('Window Title', layout)    

    event, values = window.read() 
    window.close()
    global ra_1,ra_2,ra_3
    try:
        ra_1=(int(values[0]))
        ra_2=(int(values[1]))
        ra_3=(int(values[2]))
    except:
        pass

SetRecoilParameters(ra_1,ra_2,ra_3)

print('PUBG Assistant Activated')
print('Press Ctrl+Enter to activate Recoil Alleviation')
print('Press Shift+Enter to adjust the Compensation Value')
print('Press Ctrl+1/Ctrl+2/Ctrl+3 to switch to Different Mode')

while 1:
    if keyboard.is_pressed('esc'):
        while keyboard.is_pressed('esc'):
            continue
        isTabkeyPressed = False
        isMkeyPressed = False

    elif keyboard.is_pressed('tab'):
        while keyboard.is_pressed('tab'):
            continue
        if isTabkeyPressed == False:
            isTabkeyPressed = True
        if isMkeyPressed == True:
            isMkeyPressed = False
        print("Tab:",isTabkeyPressed)

    elif keyboard.is_pressed('m'): 
        while keyboard.is_pressed('m'):
            continue 
        if isMkeyPressed == False:
            isMkeyPressed = True
            print("Measure Mode",isMkeyPressed)
        if isTabkeyPressed == True:
            isTabkeyPressed = False

 #----------------No Recoil-----------------------------------------------------------
    elif keyboard.is_pressed('shift+enter'):
        SetRecoilParameters(ra_1,ra_2,ra_3)

    elif keyboard.is_pressed('ctrl+enter'): 
        while keyboard.is_pressed('ctrl+enter'):
            continue
        if isNoRecoil == False:
            while keyboard.is_pressed('ctrl+enter'):
                continue
            isNoRecoil = True
            winsound.Beep(f3, 250)
            winsound.Beep(f3, 250)
            #print("No Recoil:",isNoRecoil)
        elif isNoRecoil == True:
            while keyboard.is_pressed('ctrl+enter'):
                continue
            isNoRecoil = False
            winsound.Beep(f3, d1)
            #print("No Recoil:",isNoRecoil)
        #sg.popup_timed("No Recoil:",isNoRecoil,"Weapon Mode",WeaponMode,location = (100,100),auto_close_duration=0.3)
    
    elif keyboard.is_pressed('ctrl+1'):
        while keyboard.is_pressed('ctrl+1'):
            continue
        winsound.Beep(f_m1, d1)
        WeaponMode = "Auto"
        #print("Weapon Mode:",WeaponMode)
        #sg.popup_timed("Weapon Mode:",WeaponMode,location = (100,100),auto_close_duration=0.3)

    elif keyboard.is_pressed('ctrl+2'):
        while keyboard.is_pressed('ctrl+1'):
            continue
        winsound.Beep(f_m2, d1)
        WeaponMode = "Semi"
        #print("Weapon Mode:",WeaponMode)
        #sg.popup_timed("Weapon Mode:",WeaponMode,location = (100,100),auto_close_duration=0.3)

    elif keyboard.is_pressed('ctrl+3'):
        while keyboard.is_pressed('ctrl+3'):
            continue
        winsound.Beep(f_m3, d1)
        WeaponMode = "Semi-ForcedAuto"
        #print("Weapon Mode:",WeaponMode)
        #sg.popup_timed("Weapon Mode:",WeaponMode,location = (100,100),auto_close_duration=0.3)

    elif keyboard.is_pressed('Up'):
        while keyboard.is_pressed('Up'):
            continue
        winsound.Beep(f1, d1)
        if WeaponMode == "Auto":
            ra_1+=1
            print("ra_1:",ra_1)
        elif WeaponMode == "Semi":
            ra_2+=1
            print("ra_2:",ra_2)
        elif WeaponMode == "Semi-ForcedAuto":
            ra_3+=1
            print("ra_3:",ra_3)
        
    elif keyboard.is_pressed('Down'):
        while keyboard.is_pressed('Down'):
            continue
        winsound.Beep(f2, d1)
        if WeaponMode == "Auto":
            ra_1-=1
            print("ra_1:",ra_1)
        elif WeaponMode == "Semi":
            ra_2-=1
            print("ra_2:",ra_2)
        elif WeaponMode == "Semi-ForcedAuto":
            ra_3-=1
            print("ra_3:",ra_3)
        

    if isTabkeyPressed or isMkeyPressed:
        isUIOpen = True
    else:
        isUIOpen = False

    while (win32api.GetAsyncKeyState(0x01)&0x8000 and isUIOpen==False):
        if isNoRecoil and WeaponMode == "Auto":
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,0,ra_1,0,0)
            time.sleep(0.01)
        elif isNoRecoil and WeaponMode == "Semi-ForcedAuto":
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,0,ra_3,0,0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
            time.sleep(0.03)
        elif isNoRecoil and WeaponMode == "Semi":
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,0,ra_2,0,0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
            time.sleep(0.01)
    #-----------------------------------------------------------------------------------
    #----------------------------Map Measure-------------------------------------------

    while isTabkeyPressed:
        if keyboard.is_pressed('tab'):
            while keyboard.is_pressed('tab'):
                continue
            isTabkeyPressed = False
            print("Tab:",isTabkeyPressed)

        elif keyboard.is_pressed('esc'):
            while keyboard.is_pressed('esc'):
                continue
            isTabkeyPressed = False
            print("Tab:",isTabkeyPressed)

        elif keyboard.is_pressed('m'):
            while keyboard.is_pressed('m'):
                continue
            isTabkeyPressed = False
            isMkeyPressed = True
            print("Tab:",isTabkeyPressed)
            print("Measure Mode",isMkeyPressed)
            

    while isMkeyPressed:
        if keyboard.is_pressed('m'): 
            while keyboard.is_pressed('m'):
                continue
            isMkeyPressed = False
            print("Measure Mode",isMkeyPressed)

        elif keyboard.is_pressed('esc'): 
            while keyboard.is_pressed('esc'):
                continue
            isMkeyPressed = False
            print("Measure Mode",isMkeyPressed)

        elif keyboard.is_pressed('tab'): 
            while keyboard.is_pressed('tab'):
                continue
            isTabkeyPressed = True
            isMkeyPressed = False
            print("Measure Mode",isMkeyPressed)
            print("Tab:",isTabkeyPressed)

    time.sleep(0.05)
    
    
