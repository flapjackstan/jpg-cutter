import cv2
import numpy as np
import sys
#import matplotlib.pyplot as plt

import os
os.chdir('../')
scan_path = 'data/'
directory = os.listdir(scan_path)

for i in directory:
    print(i)
    #imread needs to be read in grayscale for threshhold to work
    img=cv2.imread(scan_path+i,0)
    
    if img is None:
        sys.exit("No input image")
    
    rgb=cv2.imread(scan_path+i,1)
    if img is None:
        sys.exit("No input image") #good practice
        
    #thresholding your image to keep all but the background (I took a version of your
    #image with a white background, you may have to adapt the threshold
    
    thresh=cv2.threshold(img, 200, 255, cv2.THRESH_BINARY_INV);
    res=thresh[1]
    
    #dilating the result to connect all small components in your image
    #I think this is where the color gets fucked
    kernel=cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
    for j in range(10):
        res=cv2.dilate(res,kernel)
    
    #Finding the contours
    contours,img2=cv2.findContours(res,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    cnt = contours[4]
    
    cpt=0
    MIN_SHAPE = np.asarray((1200, 1200))
    
    for contour in contours:
        #finding the bounding rectangle of your contours
        rect=cv2.boundingRect(contour)
        
        #cropping the image to the value of the bounding rectangle
        img2=rgb[rect[1]:rect[1]+rect[3],rect[0]:rect[0]+rect[2]]
        #if over 200kb
        if img2.size * img2.itemsize > 1000000:
            cv2.imwrite("output/"+i+'-'+str(cpt)+".jpg", img2)
            cpt=cpt+1;
        #print(cpt)
print('done')