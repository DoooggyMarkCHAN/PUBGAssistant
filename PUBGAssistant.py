import mouse
import keyboard
import time
import win32api, win32con
import PySimpleGUI as sg
import math

# No Recoil State
isNoRecoil = False
# Weapon Mode
WeaponMode = "Auto"

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



while 1:
    #----------------No Recoil-----------------------------------------------------------
    if keyboard.is_pressed('ctrl+enter'): 
        time.sleep(0.2)
        sg.theme('DarkAmber')
        
        if isNoRecoil == False and keyboard.is_pressed('ctrl+enter')!=True:
            isNoRecoil = True
            print("No Recoil:",isNoRecoil)


        elif isNoRecoil == True and keyboard.is_pressed('ctrl+enter')!=True:
            isNoRecoil = False
            print("No Recoil:",isNoRecoil)

        sg.popup_timed("No Recoil:",isNoRecoil,"Weapon Mode",WeaponMode,location = (100,100),auto_close_duration=1)

    if keyboard.is_pressed('ctrl+1'):
        time.sleep(0.2)
        WeaponMode = "Auto"
        print("Weapon Mode:",WeaponMode)
        sg.popup_timed("Weapon Mode:",WeaponMode,location = (100,100),auto_close_duration=1)
    if keyboard.is_pressed('ctrl+2'):
        time.sleep(0.2)
        WeaponMode = "Semi"
        print("Weapon Mode:",WeaponMode)
        sg.popup_timed("Weapon Mode:",WeaponMode,location = (100,100),auto_close_duration=1)
    if keyboard.is_pressed('ctrl+3'):
        time.sleep(0.2)
        WeaponMode = "Semi-ForcedAuto"
        print("Weapon Mode:",WeaponMode)
        sg.popup_timed("Weapon Mode:",WeaponMode,location = (100,100),auto_close_duration=1)


    if (win32api.GetAsyncKeyState(0x01)&0x8000):
        if isNoRecoil and WeaponMode == "Auto":
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,0,10,0,0)
            time.sleep(0.01)
        elif isNoRecoil and WeaponMode == "Semi-ForcedAuto":
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,0,10,0,0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
            time.sleep(0.01)
        elif isNoRecoil and WeaponMode == "Semi":
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,0,15,0,0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
            time.sleep(0.03)
    #-----------------------------------------------------------------------------------
    #----------------------------Map Measure-------------------------------------------
    if keyboard.is_pressed('ctrl+p'): 
        time.sleep(0.2) #avoid multiple activation 
        if keyboard.is_pressed('ctrl+p')==False:
            if isMeasuring == False:
                isMeasuring = True
                isMatching = False
                print("Measure Mode",isMeasuring)
                sg.popup_timed("Measure Mode",isMeasuring,location = (100,100),auto_close_duration=1)
            else:
                isMeasuring = False
                print("Measure Mode",isMeasuring)
                sg.popup_timed("Measure Mode",isMeasuring,location = (100,100),auto_close_duration=1)

    # Press ( ctrl + l ) to activate matching mode
    if keyboard.is_pressed('ctrl+l'): 
        time.sleep(0.2) #avoid multiple activation 
        if keyboard.is_pressed('ctrl+l')==False:
            if isMatching == False:
                isMatching = True
                isMeasuring = False
                print("Matching Mode",isMatching)
                sg.popup_timed("Matching Mode",isMatching,location = (100,100),auto_close_duration=1)
            else:
                isMatching = False
                print("Matching Mode",isMatching)       
                sg.popup_timed("Matching Mode",isMatching,location = (100,100),auto_close_duration=1)
                
    # Click to input 1st point and 2nd point of matching
    if (win32api.GetAsyncKeyState(0x01)&0x8000) and isMatching:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
        if m_point == 1:
            match_1=win32api.GetCursorPos()
            print("Match Point1:")
            print(match_1)
            sg.popup_timed("Match Point 1",match_1,location = (100,100),auto_close_duration=0.5)
            m_point=2
        elif m_point == 2:
            match_2=win32api.GetCursorPos()
            print("Match Point2:")
            print(match_2)
            sg.popup_timed("Match Point 2",match_2,location = (100,100),auto_close_duration=0.5)
            m_point=1
            mDistance = math.sqrt((match_2[0]-match_1[0])*(match_2[0]-match_1[0])+(match_2[1]-match_1[1])*(match_2[1]-match_1[1]))
            print("Pixel Distance",mDistance) 
            #sg.popup_timed("Pixel Distance",mDistance,location = (100,100),auto_close_duration=1)
            scale = 1/mDistance*100

    # Click to input 1st point and 2nd point of measuring
    if (win32api.GetAsyncKeyState(0x01)&0x8000) and isMeasuring:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
        if i_point == 1:
            point_1=win32api.GetCursorPos()
            print("Point1:")
            print(point_1)
            sg.popup_timed("Point1",point_1,location = (100,100),auto_close_duration=0.5)
            i_point=2
        elif i_point == 2:
            point_2=win32api.GetCursorPos()
            print("Point2:")
            print(point_2)
            sg.popup_timed("Point2",point_2,location = (100,100),auto_close_duration=0.5)
            i_point=1
            realDistance = math.sqrt((point_2[0]-point_1[0])*(point_2[0]-point_1[0])+(point_2[1]-point_1[1])*(point_2[1]-point_1[1]))
            realDistance=realDistance*scale
            print("Real Distance",realDistance) 
            sg.popup_timed("Real Distance",realDistance,location = (100,100),auto_close_duration=2.5)
        #pass
    time.sleep(0.01)
    
    
