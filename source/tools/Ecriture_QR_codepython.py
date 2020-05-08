import qrcode 
import cv2
import numpy as np
import os
import PIL
from PIL import Image


message=["D0","D1","D2","A0","A1","A2","A3","A4","A5","B0","B1","B2","B3","B4","B5","C0","C1","C2"]

def generate(data, QRcode):
     img = qrcode.make(data) #generate QRcode     
     img.save(QRcode)     
     return img  
 
for i in range(len(message)):
    generate(message[i],message[i]+".png")
    
QRcode=[]
FIXE = 60 #en pixel fais environs 15cm

for element in os.listdir():
    if element.endswith('.png'):
        QRcode.append(element)
        basewidth = 60
        img = Image.open(element)
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
        img.save(element)
     

