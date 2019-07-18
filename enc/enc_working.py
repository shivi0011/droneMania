from PIL import Image
from numpy import*


from array import *

w, h = 256, 256;
e = [[0 for a in range(w)] for b in range(h)] 
e_par = [[0 for a in range(w)] for b in range(h)]

'''
img = Image.new( 'L', (256,256), "red") # Create a new black image
pixels = img.load() # Create the pixel map
print(pixels)
#pixels.reshape()
'''
from PIL import Image
import cv2
#im = Image.open('20.bmp').convert('L')
#orig_data = []
im = cv2.imread('20.bmp',0)   #0 for grayscale , 1 for colored
#orig_data.append (im)
#print('orig_data.shape[0] = ',orig_data.shape[0])
#orig_data.reshape(orig_data.shape[0],256)
print(im.shape)
print(im[0][0])
im[0][0] = 255
'''
cv2.imshow('20.bmp',im)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''

import numpy as np
blank_img = np.zeros((h,w,1), np.uint8)
#print(blank_img.shape)
cv2.imwrite("blank.bmp", blank_img)

b_im = cv2.imread('blank.bmp',0)
print(b_im.shape)

for i in range(256):    # For every pixel:
    for j in range(256):
        if(i==0):
            e[i][j] = (17*i*j+19*j+29)%256
            #print(e[i][j])
            b_im[i][j]= e[i][j]
        else:
            e[i][j] = (e[i-1][j]+i)%256
            b_im[i][j]= e[i][j]

cv2.imwrite("blank.bmp", b_im)    #blank img is kernel

#--------------------------------------------

#allocate bigger size and read the image in it
pixelOrig = np.zeros((h,2304,1), np.uint8)   #pixelOrig is array containing all 0  -- h,w,channel

for i in range(h):  #height
    for j in range(768):  #width
        pixelOrig[i][j] = im[i][j]

cv2.imwrite("pixelsOrig.bmp", pixelOrig)     #now pixelOrig is of h x 2304 size and having original image
print('pixelOrig.shape = ',pixelOrig.shape)
#---------------------------------------------
#timg = Image.fromarray(pixelOrig)
#timg.save('testt.bmp')

#import scipy.misc
#scipy.misc.imsave('outfi.jpg', pixelOrig)
#print(pixOrig)

#import matplotlib
#matplotlib.image.imsave('name.png', pixelOrig)
    
'''
for i in range(0,2304):   #col
    for j in range(0,256):   #row
        if(i<769 and j<256):
            #pixelOrig[i][j] = im[i][j]
            pixelOrig.append(im[i][j])
'''            
    
pixelsNew = np.zeros((h,2304,1), np.uint8)
cv2.imwrite("pixelsNew.bmp", pixelsNew)
print('pixelsNew.shape = ',pixelsNew.shape)

for i in range(0,h,256):
    for j in range(0,2304,256):
        for k in range(0,256,1):
            for l in range(0,256,1):
                #print(i+k,j+e[k][l],i+k,j+l)
                #pixelsNew[i+k,j+e[k][l]] = pixelMap[i+k,j+l]
                #print('---'+str(pixelsNew[j+e[k][l],i+k]))
                #print('==='+str(pixelMap[j+l,i+k]))
                pixelsNew[i+k][j+e[k][l]] = pixelOrig[i+k][j+l]
                
                
cv2.imwrite("pixelsNew.bmp", pixelsNew)   #now this is having garbled image

#-----------------------------------------

# Decryption

for i in range(0,256,1):
    for j in range(0,256,1):
        e_par[i][e[i][j]] = j;
        
qpixelMap = cv2.imread('pixelsNew.bmp',0)
print('qpixelMap.shape =',qpixelMap.shape)
pixelDec = np.zeros((h,2304,1), np.uint8)   


for i in range(0,h,256):
    for j in range(0,2304,256):
        for k in range(0,256,1):
            for l in range (0,256,1):
                print(j+e_par[k][l],i+k,j+l,i+k)
                pixelDec[i+k][j+e_par[k][l]] = qpixelMap[i+k][j+l]
                
                
cv2.imwrite("pixelDec.bmp", pixelDec)             


#------Now crop it----------------------------
'''
from PIL import Image
img1 = Image.open("pixelDec.bmp")

crop_rectangle = (0, 0, 768, 256)
cropped_im = img1.crop(crop_rectangle)
cropped_im.save('pixelDecCropped.bmp')
'''

