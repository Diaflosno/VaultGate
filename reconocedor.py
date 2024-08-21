import cv2
import numpy as np
import pickle
from time import sleep
import time
import RPi.GPIO as gpio
from datetime import datetime
import mysql.connector as mysql
from pruebaservo import movimientoAbrir, verde


gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)



def getID(conexion, nombre):
	cur = conexion.cursor()
	sql2 = "SELECT idusuario FROM usuario WHERE nombre = %s"
	val = (nombre,)
	cur.execute(sql2, val)
	resultado = cur.fetchall()
	for row in resultado:
		ide = row[0]
	return ide

def aperturaDB(conexion,ID):
	cur = conexion.cursor()
	sql = "INSERT INTO apertura(fecha,hora,idusuario) VALUES(%s, %s, %s)"
	val = (datetime.today().strftime('%Y-%m-%d'), datetime.today().strftime('%H:%M:%S'), ID)
	cur.execute(sql, val)
	conexion.commit()


	


def Reconocedor(miConexion):
	with open('labels','rb') as f:
		dicti = pickle.load(f)

	THRESHOLD_CONFIDENCE = 90

	camera = cv2.VideoCapture(0)
	camera.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
	camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

	faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
	recognizer = cv2.face.LBPHFaceRecognizer_create()
	recognizer.read('trainer.yml')

	font = cv2.FONT_HERSHEY_SIMPLEX
	inicio = time.time()
	flag = True
	while flag:
		ret, frame = camera.read()
		if not ret:
			break
		if time.time() - inicio >3:
			print("Se ha alcanzado el tiempo limite, vuelva a intentar mas tarde")
			break
		
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		faces = faceCascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
		
		for (x, y, w, h) in faces:
			roiGray = gray[y:y+h, x:x+w]
			id_, conf = recognizer.predict(roiGray)
			if conf < THRESHOLD_CONFIDENCE:
				
				for name, value in dicti.items():
					if value == id_:
						print("USUARIO IDENTIFICADO")
						print(f"USUARIO: {name}")
						aperturaDB(miConexion,getID(miConexion,name))
						verde()
						movimientoAbrir()
						flag = False
			 
			else:
				print("Usuario no detectado")

				
				cv2.rectangle(frame,(x, y), (x+w, y+h), (255,0,0),2)
			cv2.imshow('Reconocimiento facial', frame)
		key = cv2.waitKey(1) & 0xFF
		if key == 27:
			break
	camera.release()
	cv2.destroyAllWindows()