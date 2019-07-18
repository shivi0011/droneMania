# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
from PIL import Image
from numpy import*
from array import *
import numpy as np


# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (768, 256)         #(640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(768, 256))         #(640, 480))
 
# allow the camera to warmup
time.sleep(0.1)
imageCounter=1

w, h = 256, 256;
e = [[0 for a in range(w)] for b in range(h)] 
e_par = [[0 for a in range(w)] for b in range(h)]

kernel_img = np.zeros((h,w,3), np.uint8)   #===
#print(blank_img.shape)
cv2.imwrite("kernel.bmp", kernel_img)

b_im = cv2.imread('kernel.bmp',1) #===
#print(b_im.shape)

for i in range(256):    # For every pixel:
    for j in range(256):
        if(i==0):
            e[i][j] = (17*i*j+19*j+29)%256
            #print(e[i][j])
            b_im[i][j]= e[i][j]
        else:
            e[i][j] = (e[i-1][j]+i)%256
            b_im[i][j]= e[i][j]

cv2.imwrite("kernel.bmp", b_im)    #this img is kernel


# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array
     
    #print(image.s)
    # show the frame
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF
    fileCaptured = "images/"+str(imageCounter)+".bmp"
    cv2.imwrite(fileCaptured, image)
    
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    #-----------------------------------------------------------

    im = cv2.imread('20.bmp',1) #===  #0 for grayscale , 1 for colored

    #---------------------------------------------         
        
    pixelEnc = np.zeros((h,768,3), np.uint8)  #===2304
    cv2.imwrite("enc/"+str(imageCounter)+".bmp", pixelEnc)
    #print('pixelEnc.shape = ',pixelEnc.shape)

    for i in range(0,h,256):
        for j in range(0,768,256):   #2304
            for k in range(0,256,1):
                for l in range(0,256,1):
                    pixelEnc[i+k][j+e[k][l]] = im[i+k][j+l]    #reversed the order
                    
                    
    cv2.imwrite("enc/"+str(imageCounter)+".bmp", pixelEnc)   #now this is having garbled image

    if(imageCounter == 10):
        exit(0)
    #-----------------------------------------

    # Decryption
    #-----------------------------------------------------------
    for i in range(0,256,1):
        for j in range(0,256,1):
            e_par[i][e[i][j]] = j;
        
    qpixelMap = cv2.imread('enc/'+str(imageCounter)+'.bmp',1)  #===
    #print('qpixelMap.shape =',qpixelMap.shape)
    pixelDec = np.zeros((h,768,3), np.uint8)     #====2304


    for i in range(0,h,256):
        for j in range(0,768,256):  #2304
            for k in range(0,256,1):
                for l in range (0,256,1):
                    #print(j+e_par[k][l],i+k,j+l,i+k)
                    pixelDec[i+k][j+e_par[k][l]] = qpixelMap[i+k][j+l]
                    
                    
    cv2.imwrite("dec/"+str(imageCounter)+".bmp", pixelDec)             


    imageCounter=imageCounter+1 


    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
 


