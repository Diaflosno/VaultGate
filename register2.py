import cv2
import numpy as np
import os
import shutil
import sys
import time
from entrenador import Rostro #ESTA IMPORTACION ES PARA PODER ENTRENAR AL ROSTRO


def registro(name):
	camera = cv2.VideoCapture(0)

	camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
	camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

	faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

	dirName = f"./{name}"
	print(dirName)
	if not os.path.exists(dirName):
		os.makedirs(dirName)
		print("Se ha creado el directorio para la persona")
		print("MIRA A LA CAMARA")
	else:
		print("Esa persona ya se encuentra registrada")
		print("No se puede crear otro directorio")
		sys.exit()

	count = 0
	inicio = time.time()
	while True:
		ret, frame = camera.read()
		if not ret:
			break
		if time.time() - inicio >20:
			print("Se ha alcanzado el tiempo limite, vuelva a intentar mas tarde")
			shutil.rmtree(dirName)
			break
		
		gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
		faces = faceCascade.detectMultiScale(gray, scaleFactor = 1.5, minNeighbors =5)
		for (x,y,w,h) in faces:
			roiGray = gray[y:y+h, x:x+w]
			fileName = f"{dirName}/{name}_{str(count)}.jpg"
			cv2.imwrite(fileName, roiGray)
			cv2.imshow('face',roiGray)
			cv2.rectangle(frame,(x, y), (x+w, y+h),(0,255,0), 2)
			count += 1
		cv2.imshow('frame', frame)
		
		key = cv2.waitKey(1)
		if key == 27 or count >= 50:
			Rostro()
			break
	camera.release()
	cv2.destroyAllWindows()
