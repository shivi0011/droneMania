# import the necessary packages

from PIL import Image
from numpy import*


from array import *

w, h = 256, 256;
e = [[0 for a in range(w)] for b in range(h)] 
e_par = [[0 for a in range(w)] for b in range(h)]

for i in range(0,256,1):
    for j in range(0,256,1):
        if(i==0):
            e[i][j] = (17*i*j+19*j+29)%256
            #print(e[i][j])
        else:
            e[i][j] = (e[i-1][j]+i)%256

import numpy as np
from PIL import Image
im = Image.open('20.bmp')
print(im.size)

#pixelM = im.load()
#pixelMap = [[0 for a in range(256)] for b in range(768*3)] 
pixelMap = np.zeros((256,768))  
pixelMap = im.load()
 

img = Image.new( im.mode, im.size)
#pixelsN = img.load()


col = img.size[0]
row = img.size[1]
pixelsNew = np.zeros((256,768))
print('---'+pixelsNew.size)
pixelsNew = img.load()
#print(pixelsNew.)
print('row - '+str(row))
print('col - '+str(col))


for i in range(0,256,256):
    for j in range(0,2304,256):
        for k in range(0,256,1):
            for l in range(0,256,1):
                #print(i+k,j+e[k][l],i+k,j+l)
                #pixelsNew[i+k,j+e[k][l]] = pixelMap[i+k,j+l]
                pixelsNew[i+k][j+e[k][l]] = pixelMap[i+k][j+l]
                
        print('j = '+str(j))
    print('i = '+str(i))
        #if 205 in pixelMap[i,j]:
         #   pixelMap[i,j] = (0,0,0,255)
        #else:
         #   pixelsNew[i,j] = pixelMap[i,j]
#img.show()
img.save("enc2.bmp")



#https://stackoverflow.com/questions/32694007/opencv-python-how-to-change-image-pixels-values-using-a-formula

# Decryption

for i in range(0,256,1):
    for j in range(0,256,1):
        e_par[i][e[i][j]] = j;
    

imm = Image.open('enc2.bmp')
print('col - row -- '+str(imm.size))

qpixelMap = np.zeros((256,2304)) 
qpixelMap = imm.load()
imm.save("enc2_.bmp")

img_deq = Image.new(imm.mode, imm.size)
#pixelDeq = img_deq.load()
pixelDeq = np.zeros((256,2304))  
col = img_deq.size[0]
row = img_deq.size[1]

img_deq.save("enc2_1.bmp")

for i in range(0,256,256):
    for j in range(0,2304,256):
        for k in range(0,256,1):
            for l in range (0,256,1):
                pixelDeq[i+k][j+e_par[k][l]] = qpixelMap[i+k][j+l]   #pixelDeq[i+k,j+e_par[k][l]] = pixelsNew[i+k,j+l]
                #print(i+k,j+e_par[k][l])
            #print('k = '+str(k))
        print('j = '+str(j))
    print('i = '+str(i))
#pixelDeq[0,0] = 255

img_deq.save("dec2.bmp")


#scan = 256
#pixel = 256 * 9