from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import math
import RPi.GPIO as gpio

def cropping_colour(image):
    (cX, cY) = (image.shape[1], image.shape[0])
    limX = cX//3
    limY = cY//2
    image = image[limY+100:2*limY, limX:2*limX]
    return image

def cropping(image):
    (cX, cY) = (image.shape[1], image.shape[0])
    limX = cX//3
    limY = cY//2
    image = image[limY:2*limY, 0:cX]
    return image
    
def colour(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lowerBound=np.array([0,0,0])
    upperBound=np.array([180,255,60])
    mask=cv2.inRange(img,lowerBound,upperBound)
    l = []
    for i in mask:
        l.append(sum(i)/len(i))
    g = sum(l)/len(l)
    return g, mask
#    b,g,r = cv2.split(img)
#    b = sum(sum(b)/len(b))
#    g = sum(sum(g)/len(g))
#    r = sum(sum(r)/len(r))
#    #print(b,g,r)
#    return b,g,r, mask


def sobel(pic, n):
    if n==0:
        sobelp = cv2.Sobel(pic,cv2.CV_64F,1,0,ksize=5)
    else:
        sobelp = cv2.Sobel(pic,cv2.CV_64F,0,1,ksize=5)
    r, sobelp = cv2.threshold(sobelp,200,255,cv2.THRESH_BINARY)
    sobelp = np.uint8(sobelp)
    return r, sobelp

def masking(image):
  mask = np.zeros(image.shape[:2], dtype = "uint8")
  (cX, cY) = (image.shape[1] // 2, image.shape[0] // 2)
  cv2.rectangle(mask, (0, cY+40), (2*cX  , 2*cY), 255,-1)
  masked = cv2.bitwise_and(image, image, mask = mask)
  return masked

angle=0
minLineLength = 30
maxLineGap = 10
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(1)

def Lane_detection(frame, theta):
    img = frame.array
    image = cropping(img)
    imagec = cropping_colour(img)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 85, 85)
    lines = cv2.HoughLinesP(edged,1,np.pi/180,10,minLineLength,maxLineGap)
    if np.all(lines != None):
        for x in range(0, len(lines)):
            for x1,y1,x2,y2 in lines[x]:
                cv2.line(image,(x1,y1),(x2,y2),(0,255,0),2)
                theta=theta+math.atan2((y2-y1),(x2-x1)) #math.atan2 returns the angle between the lines
    threshold=6
    if(theta>threshold):
        print("left")
        return 1, image
    if(theta<-threshold):
        print("right")
        return 2, image
    if(abs(theta)<threshold):
        print("straight")
        return 3, image
    theta=0

def init():
    gpio.setmode(gpio.BCM)
    gpio.setup(17, gpio.OUT)
    gpio.setup(22, gpio.OUT)
    gpio.setup(23, gpio.OUT)
    gpio.setup(24, gpio.OUT)
    gpio.setup(25, gpio.OUT)
    gpio.setup(18, gpio.OUT)

def wait(tf):
#    init()
    gpio.output(17, False)
    gpio.output(22, False)
    gpio.output(23, False)
    gpio.output(24, False)
    time.sleep(tf)
#    gpio.cleanup()


def forward(tf,percentage,freq):
    init()
    gpio.output(17, True)
    gpio.output(22, False)
    gpio.output(23, True)
    gpio.output(24, False)
    
    p = gpio.PWM(18,freq)
    q = gpio.PWM(25,freq)
    p.start(percentage)
    q.start(percentage)
    time.sleep(tf)
    gpio.cleanup()


def reverse(tf,percentage,freq):
    init()
    gpio.output(17, False)
    gpio.output(22, True)
    gpio.output(23, False)
    gpio.output(24, True)

    p = gpio.PWM(18,freq)
    q = gpio.PWM(25,freq)
    p.start(percentage)
    q.start(percentage)
    time.sleep(tf)
    gpio.cleanup()

def left(tf,percentage,freq):
    init()
    gpio.output(17, True)
    gpio.output(22, False)
    gpio.output(23, False)
    gpio.output(24, False)
    p = gpio.PWM(18,freq)
    p.start(percentage)
    time.sleep(tf)
    gpio.cleanup()

def right(tf,percentage,freq):
    init()
    gpio.output(17, False)
    gpio.output(22, False)
    gpio.output(23, True)
    gpio.output(24, False)
    q = gpio.PWM(25,freq)
    q.start(percentage)
    time.sleep(tf)
    gpio.cleanup()

def sharp_left(tf,percentage,freq):
    init()
    gpio.output(17, True)
    gpio.output(22, False)
    gpio.output(23, False)
    gpio.output(24, True)
    p = gpio.PWM(18,freq)
    q = gpio.PWM(25,freq)
    p.start(percentage)
    q.start(percentage)
    time.sleep(tf)
    gpio.cleanup()

def sharp_right(tf,percentage,freq):
    init()
    gpio.output(17, False)
    gpio.output(22, True)
    gpio.output(23, True)
    gpio.output(24, False)
    p = gpio.PWM(18,freq)
    q = gpio.PWM(25,freq)
    p.start(percentage)
    q.start(percentage)
    time.sleep(tf)
    gpio.cleanup()





#def colour(img):
#    b,g,r = cv2.split(img)
#    b = sum(sum(b)/len(b))
#    g = sum(sum(g)/len(g))
#    r = sum(sum(r)/len(r))
#    return b,g,r



if __name__ == '__main__':
#    forward(2,50,100)
    dsn = [] #descision list
    init()
    gpio.output(17, True)
    gpio.output(22, False)
    gpio.output(23, True)
    gpio.output(24, False) 
    p = gpio.PWM(18,100)
    q = gpio.PWM(25,100)
    p.start(35)
    q.start(35)
    
    
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        output, fps = Lane_detection(frame, angle)
        imgc = cropping_colour(frame.array)
        dsn.append(output)
        if len(dsn) >= 5:
            if dsn.count(1) >= 3:
                #turn left
                #left(0.3,55,100)
                gpio.output(17, True)
                gpio.output(22, False)
                gpio.output(23, False)
                gpio.output(24, False)
                p.ChangeDutyCycle(50)
                dsn = []
            elif dsn.count(2) >= 3:
                #turn right
                #right(0.3,50,100)
                gpio.output(17, False)
                gpio.output(22, False)
                gpio.output(23, True)
                gpio.output(24, False)
                q.ChangeDutyCycle(45)
                dsn = []
            else:
                #forward(2,50,100)
                gpio.output(17, True)
                gpio.output(22, False)
                gpio.output(23, True)
                gpio.output(24, False)

                p.ChangeDutyCycle(45)
                q.ChangeDutyCycle(45)
                dsn = []
                
        g, m = colour(imgc)
        print(g)
        #print(b,g,r)
#        lim=100
        if g>=50: #we'll have to play around with the values
            #stop the car
            wait(2)
            print("STOOOP")
        cv2.imshow("Frame", m)
        key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)
        if key == ord("q"):
            gpio.cleanup()
            print("gpio clean up successful")
            break
        

