#import das bibliotecas
import os
import cv2 #bibliotecaopencv
import numpy as np
import math
cap = cv2.VideoCapture(0) #variaveldearmazenamento das imagens

#laço de leitura da camera
while(1): 
    #verifica o objeto mão na camera
    try
    
    ret, frame = cap.read()
    frame=cv2.flip(frame,1)
    kermel = np.one((3,3),np.uinst8)

    #definindo as regioes de interesse (o quadrado em cima da mão para avaliar os movimentos na região definida para analise)
    roi=frame[100:300, 100:300]

    cv2.rectangle(frame,(100,100),(300,300),(0,255,0)0)

    hsv = cv2.cvtColor(roi, cv2.COLOR_BGRHSV)
