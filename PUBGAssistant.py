import mouse
import keyboard
import time
import win32api, win32con
import PySimpleGUI as sg
import math

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
ra_1 = 10
ra_2 = 15
ra_3 = 10

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
print('Press M to switch to Different Mode')
while 1:
    if keyboard.is_pressed('esc'):
        while keyboard.is_pressed('esc'):
            continue
        if isTabkeyPressed == True:
            isTabkeyPressed = False
        if isMkeyPressed == True:
            isMkeyPressed = False
            isMeasuring = False

    if keyboard.is_pressed('tab'):
        while keyboard.is_pressed('tab'):
            continue
        if isTabkeyPressed == True:
            isTabkeyPressed = False
        elif isTabkeyPressed == False:
            isTabkeyPressed = True     

    if isTabkeyPressed or isMkeyPressed:
        isUIOpen = True
    else:
        isUIOpen = False

    #----------------No Recoil-----------------------------------------------------------
    if keyboard.is_pressed('shift+enter'):
        SetRecoilParameters(ra_1,ra_2,ra_3)

    if keyboard.is_pressed('ctrl+enter'): 
        while keyboard.is_pressed('ctrl+enter'):
            continue
        sg.theme('DarkAmber')

        if isNoRecoil == False and keyboard.is_pressed('ctrl+enter')!=True:
            while keyboard.is_pressed('ctrl+enter'):
                continue
            isNoRecoil = True
            #print("No Recoil:",isNoRecoil)
        elif isNoRecoil == True and keyboard.is_pressed('ctrl+enter')!=True:
            while keyboard.is_pressed('ctrl+enter'):
                continue
            isNoRecoil = False
            #print("No Recoil:",isNoRecoil)

        sg.popup_timed("No Recoil:",isNoRecoil,"Weapon Mode",WeaponMode,location = (100,100),auto_close_duration=1)
    
    if keyboard.is_pressed('ctrl+1'):
        while keyboard.is_pressed('ctrl+1'):
            continue
        WeaponMode = "Auto"
        #print("Weapon Mode:",WeaponMode)
        sg.popup_timed("Weapon Mode:",WeaponMode,location = (100,100),auto_close_duration=1)
    if keyboard.is_pressed('ctrl+2'):
        while keyboard.is_pressed('ctrl+2'):
            continue
        WeaponMode = "Semi"
        #print("Weapon Mode:",WeaponMode)
        sg.popup_timed("Weapon Mode:",WeaponMode,location = (100,100),auto_close_duration=1)
    if keyboard.is_pressed('ctrl+3'):
        while keyboard.is_pressed('ctrl+3'):
            continue
        WeaponMode = "Semi-ForcedAuto"
        #print("Weapon Mode:",WeaponMode)
        sg.popup_timed("Weapon Mode:",WeaponMode,location = (100,100),auto_close_duration=1)


    if (win32api.GetAsyncKeyState(0x01)&0x8000 and isUIOpen==False):
        if isNoRecoil and WeaponMode == "Auto":
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,0,ra_1,0,0)
            time.sleep(0.01)
        elif isNoRecoil and WeaponMode == "Semi-ForcedAuto":
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,0,ra_3,0,0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
            time.sleep(0.01)
        elif isNoRecoil and WeaponMode == "Semi":
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,0,ra_2,0,0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
            time.sleep(0.03)
    #-----------------------------------------------------------------------------------
    #----------------------------Map Measure-------------------------------------------
    if keyboard.is_pressed('m'): 
        while keyboard.is_pressed('m'):
            continue
        if keyboard.is_pressed('m')==False:
            if isMkeyPressed == True:
                isMkeyPressed = False
            elif isMkeyPressed == False:
                isMkeyPressed = True

            if isMeasuring == False:
                isMeasuring = True
                isMatching = False
                print("Measure Mode",isMeasuring)
                #sg.popup_timed("Measure Mode",isMeasuring,location = (100,100),auto_close_duration=0.5)
            else:
                isMeasuring = False
                print("Measure Mode",isMeasuring)
                #sg.popup_timed("Measure Mode",isMeasuring,location = (100,100),auto_close_duration=0.5)
                
    # Click to input 1st point and 2nd point of matching
    if (win32api.GetAsyncKeyState(0x01)&0x8000) and isMeasuring and keyboard.is_pressed('ctrl'):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
        if m_point == 1:
            match_1=win32api.GetCursorPos()
            #print("Match Point1:")
            #print(match_1)
            sg.popup_timed("Match Point 1",match_1,location = (100,100),auto_close_duration=0.5)
            m_point=2
        elif m_point == 2:
            match_2=win32api.GetCursorPos()
            #print("Match Point2:")
            #print(match_2)
            sg.popup_timed("Match Point 2",match_2,location = (100,100),auto_close_duration=0.5)
            m_point=1
            mDistance = math.sqrt((match_2[0]-match_1[0])*(match_2[0]-match_1[0])+(match_2[1]-match_1[1])*(match_2[1]-match_1[1]))
            #print("Pixel Distance",mDistance) 
            #sg.popup_timed("Pixel Distance",mDistance,location = (100,100),auto_close_duration=1)
            scale = 1/mDistance*100

    # Click to input 1st point and 2nd point of measuring
    if (win32api.GetAsyncKeyState(0x01)&0x8000) and isMeasuring:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)      
        if i_point == 1:
            point_1=win32api.GetCursorPos()
            #print("Point1:")
            #print(point_1)
            sg.popup_timed("Point1",point_1,location = (100,100),auto_close_duration=0.5)
            i_point=2
        elif i_point == 2:
            point_2=win32api.GetCursorPos()
            #print("Point2:")
            #print(point_2)
            sg.popup_timed("Point2",point_2,location = (100,100),auto_close_duration=0.5)
            i_point=1
            realDistance = math.sqrt((point_2[0]-point_1[0])*(point_2[0]-point_1[0])+(point_2[1]-point_1[1])*(point_2[1]-point_1[1]))
            realDistance=realDistance*scale
            #print("Real Distance",realDistance) 
            sg.popup_timed("Real Distance",realDistance,location = (100,100),auto_close_duration=2)
    
    if mouse.is_pressed('MWHEELUP'):
        print("Scroll up" )
        #pass
    time.sleep(0.01)
    
    
