import time
import cv2#need to install
import mediapipe as mp #need to install
import pyautogui as mouse #need to install
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume #need to install

# initialize mediapipe
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=2, min_detection_confidence=0.87)

# Initialize the webcam
cap = cv2.VideoCapture(0)

def VolumeAdj(n):
     # Get default audio device using PyCAW
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    # Get current volume 
    currentVolumeDb = volume.GetMasterVolumeLevel()
    print((n-0.5)*(-60))
    if ((n-0.5)*(-60)<0):
        volume.SetMasterVolumeLevel((n-0.5)*(-60), None)
    
def frameOut():
    _, frame = cap.read()
    x, y, c=frame.shape
    frame = cv2.flip(frame, 1)
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(framergb)
    landmarks=[]
    rtn=[]
    hand=""
    if result.multi_hand_landmarks:
        
        for handslms in result.multi_hand_landmarks:
            for lm in handslms.landmark:
                lmx = lm.x
                lmy = lm.y
                landmarks.append([lmx, lmy])
        #getting the x & y coordiante values of thumb, index and middle finger tips
        x1,y1=landmarks[4][0],landmarks[4][1]#thumb
        x2,y2=landmarks[8][0],landmarks[8][1]#index
        x3,y3=landmarks[12][0],landmarks[12][1]#middle
        #getting the mid point coordinate values of the thumb-index and thumb-middle
        midMiddlePercXvalue,midMiddlePercYvalue=((x1+x3)/2),((y1+y3)/2)
        midIndexPercXvalue,midIndexPercYvalue=((x1+x2)/2),((y1+y2)/2)
        #getting the diatance between thumb-index and thumb-middle
        middleDistance=(((x1-x3)**2)+((y1-y3)**2))**0.5
        indexDistance=(((x1-x2)**2)+((y1-y2)**2))**0.5
        # check if it is left or right
        if landmarks[4][0] > landmarks[20][0]:
            hand="left"
        else:
            hand="right"
        #return values of all the essential variables
        rtn=[hand,indexDistance,midIndexPercXvalue,midIndexPercYvalue,middleDistance,midMiddlePercXvalue,midMiddlePercYvalue]
        return rtn
    return ["",0,0,0,0,0,0]

Ln0=Ln1=Ln2=Ln3=0
Rn0=Rn1=Rn2=Rn3=0
prevMidIndexPercXvalue=0
prevMidIndexPercYvalue=0

hold=0
t=0.1
st=2
while(True):
    handDetected,indexDistance,midIndexPercXvalue,midIndexPercYvalue,middleDistance,midMiddlePercXvalue,midMiddlePercYvalue=frameOut()
    if(handDetected=="right"):
        #left click and right click opretions
        Ln3=int(indexDistance*10)
        Rn3=int(middleDistance*10)
        if  0 in (Ln0,Ln1,Ln2,Ln3) and any([Ln0,Ln1,Ln2,Ln3]) and (Ln0!=0 and Ln3!=0):
                mouse.click()
                # print("Lclick",Ln0,Ln1,Ln2,Ln3)
                Ln0=Ln1=Ln2=Ln3=9
                t=0.1
        elif  0 in (Rn0,Rn1,Rn2,Rn3) and any([Rn0,Rn1,Rn2,Rn3]) and (Rn0!=0 and Rn3!=0):
                mouse.rightClick()
                # print("Rclick",Rn0,Rn1,Rn2,Rn3)
                Rn0=Rn1=Rn2=Rn3=9
                t=0.1
        #Left hold and right hold
        elif ("".join(map(str,(Ln0,Ln1,Ln2,Ln3)))=="0000"):
            mouse.moveRel(int((midIndexPercXvalue-prevMidIndexPercXvalue)*2560),int((midIndexPercYvalue-prevMidIndexPercYvalue)*1600))
            # print("L-holded")
            t=0
        elif ("".join(map(str,(Rn0,Rn1,Rn2,Rn3)))=="0000"):
            mouse.dragRel(int((midIndexPercXvalue-prevMidIndexPercXvalue)*2560),int((midIndexPercYvalue-prevMidIndexPercYvalue)*1600))
            # print("R-holded")
            t=0
        else:
             t=0.1
        
        prevMidIndexPercXvalue=midIndexPercXvalue
        prevMidIndexPercYvalue=midIndexPercYvalue
        Ln0,Ln1,Ln2=Ln1,Ln2,Ln3
        Rn0,Rn1,Rn2=Rn1,Rn2,Rn3
    #different set of commands for left hand
    elif handDetected=="left":
        Ln3=int(indexDistance*10)
        Rn3=int(middleDistance*10)
        #left index click to click "left"
        if  0 in (Ln0,Ln1,Ln2,Ln3) and any([Ln0,Ln1,Ln2,Ln3]) and (Ln0!=0 and Ln3!=0):
                mouse.press('left')
                # print("Lclick",Ln0,Ln1,Ln2,Ln3)
                Ln0=Ln1=Ln2=Ln3=9
                t=0.1
        #left middle click to click "right"
        elif  0 in (Rn0,Rn1,Rn2,Rn3) and any([Rn0,Rn1,Rn2,Rn3]) and (Rn0!=0 and Rn3!=0):
                mouse.press('right')
                # print("Rclick",Rn0,Rn1,Rn2,Rn3)
                Rn0=Rn1=Rn2=Rn3=9
                t=0.1
        #hold down left index to increase or decrease volume.
        elif ("".join(map(str,(Ln0,Ln1,Ln2,Ln3)))=="0000"):
            if(hold<0):
                VolumeAdj(midIndexPercYvalue)
                hold=10
                # print("L-holded")
            else:
                 hold-=1
            t=0
        else:
             t=0.1
        prevMidIndexPercXvalue=midIndexPercXvalue
        prevMidIndexPercYvalue=midIndexPercYvalue
        Ln0,Ln1,Ln2=Ln1,Ln2,Ln3
        Rn0,Rn1,Rn2=Rn1,Rn2,Rn3
    
    time.sleep(t)
