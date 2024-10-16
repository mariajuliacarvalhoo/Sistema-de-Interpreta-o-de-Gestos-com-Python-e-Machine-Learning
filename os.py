#import das bibliotecas
import os
import cv2  # biblioteca opencv
import numpy as np
import math

cnt = 0  # Inicialização
defects = 0
cap = cv2.VideoCapture(0)  # variavel de armazenamento das imagens

# laço de leitura da camera
while(1):
    # verifica o objeto mão na camera
    try:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        kernel = np.ones((3, 3), np.uint8)  # Corrigido de kermel para kernel

        # definindo as regiões de interesse
        roi = frame[100:300, 100:300]
        cv2.rectangle(frame, (100, 100), (300, 300), (0, 255, 0), 0)

        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        # definindo cores pelo hsv
        lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin = np.array([20, 255, 255], dtype=np.uint8)

        # máscara de extração de contorno + filtro de dilatação
        mask = cv2.inRange(hsv, lower_skin, upper_skin)  
        mask = cv2.dilate(mask, kernel, iterations=4)  
        mask = cv2.GaussianBlur(mask, (5, 5), 100)

        # máscaras para construção de contorno
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # contorno máximo da mão
        cnt = max(contours, key=lambda x: cv2.contourArea(x))

        # definição aprox do contorno do objeto
        epsilon = 0.0005 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)

        # fazer um objeto convexo na estrutura da mão
        hull = cv2.convexHull(cnt)

        # definir contorno da área
        areahull = cv2.contourArea(hull)
        areacnt = cv2.contourArea(cnt)

        # definir área do objeto contornado com extração do valor do fundo
        arearatio = ((areahull - areacnt) / areacnt) * 100

        # encontrar defeitos no objeto convexo
        hull = cv2.convexHull(approx, returnPoints=False)
        defects = cv2.convexityDefects(approx, hull)

        l = 0

        # definindo a região de interesse
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            start = tuple(approx[s][0])
            end = tuple(approx[e][0])
            far = tuple(approx[f][0])

            # comprimento dos lados do triângulo
            a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
            b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
            c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)

            s = (a + b + c) / 2
            ar = math.sqrt(s * (s - a) * (s - b) * (s - c))

            # distância entre o ponto e o casco convexo
            d = (2 * ar) / a

            # ignore ângulos > 90 e ignore pontos muito próximos ao objeto convexo
            angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 57
            if angle <= 90 and d > 30:
                l += 1
                cv2.circle(roi, far, 3, [255, 0, 0], -1)

                # desenhar linhas ao redor da mão
                cv2.line(roi, start, end, [0, 255, 0], 2)

        l += 1

        # imprimir os gestos correspondentes
        font = cv2.FONT_HERSHEY_SIMPLEX
        if l == 1:  # gesto 1
            if areacnt < 2000:
                cv2.putText(frame, "Esperando dados", (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
            else:
                executado = False
                if arearatio < 12 and not executado:
                    cv2.putText(frame, '0 = Navegador', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
                    os.system("start Chrome.exe --window-size=800,600")
                    executado = True
                    break
                elif arearatio < 17.5:
                    cv2.putText(frame, '', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
                    os.system("start Arduino IDE.exe")
                else:
                    cv2.putText(frame, '1 = Word', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
                    os.system("start WINWORD.EXE --window-size=600,400")

        elif l == 2:
            cv2.putText(frame, '2 = Excel', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
            os.system("start Excel.exe --window-size=600,400")
            break

        elif l == 3:
            if arearatio < 27:
                cv2.putText(frame, '3 = Power Point', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
                os.system("start POWERPNT.EXE --window-size=600,400")
            else:
                cv2.putText(frame, 'ok', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)

        elif l == 4:
            cv2.putText(frame, '', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
            os.system("start firefox.exe")

        elif l == 5:
            cv2.putText(frame, '', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
            os.system("start Spyder.launch.pyw")

        elif l == 6:
            cv2.putText(frame, 'reposition', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)

        else:
            cv2.putText(frame, 'reposition', (10, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)

        # mostrar as janelas
        cv2.imshow('mask', mask)
        cv2.imshow('frame', frame)

    except:
        pass

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()
