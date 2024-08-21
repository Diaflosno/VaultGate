import RPi.GPIO as gpio
from time import sleep
from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
import time
import mysql.connector as mysql
from registro2 import registro #ACUERDATE DE USAR ESTA IMPORTACION, ES PARA PODER REGISTRAR A UN USUARIO
from entrenador import Rostro #ESTA IMPORTACION ES PARA PODER ENTRENAR AL ROSTRO
from reconocedor import Reconocedor,aperturaDB
from pruebaservo import movimientoAbrir,movimientoCerrar,iniciarServo
gpio.setmode(gpio.BOARD)

lcd = LCD()

def safe_exit(signum,frame):
	exit(1)
	
signal(SIGTERM,safe_exit)
signal(SIGHUP, safe_exit)

G = 40
R = 38
B = 36

gpio.setup(R, gpio.OUT)
gpio.setup(G, gpio.OUT)
gpio.setup(B, gpio.OUT)

trig = 8
echo = 10
gpio.setup(trig, gpio.OUT)
gpio.setup(echo, gpio.IN)

boton1 = 35
boton2 = 33
boton3 = 31
boton4 = 29
gpio.setup(boton1, gpio.IN)
gpio.setup(boton2, gpio.IN)
gpio.setup(boton3, gpio.IN)
gpio.setup(boton4, gpio.IN)



def rojo():
	gpio.output(R, gpio.HIGH)
	gpio.output(G, gpio.LOW)
	gpio.output(B, gpio.LOW)
def verde():
	gpio.output(R, gpio.LOW)
	gpio.output(G, gpio.HIGH)
	gpio.output(B, gpio.LOW)
def blanco():
	gpio.output(R, gpio.HIGH)
	gpio.output(G, gpio.HIGH)
	gpio.output(B, gpio.HIGH)



#######################################################################################################################################################
#FUNCIONES QUE HACEN USO DE BASE DE DATOS

class DatabaseMySQL:
		
	#FUNCION PARA PODER BUSCAR UN CODIGO DE INVITADO EQUIVALENTE AL INSERTADO EN EL CONTROLADOR
	def buscarCodigo(codigo):
		miConexion = mysql.connect(user='u744130986_VaultGate', password='BXueQ@vEB;g1',host='oaxacapower.org', db='u744130986_VaultGate')
		cur = miConexion.cursor()
		sql = "SELECT * FROM invitados WHERE codigoa = %s"
		val = (codigo,)
		cur.execute(sql,val)
		resultado = cur.fetchall()
		if len(resultado) == 0:
			rojo()
			print("NO EXISTE INVITADO CON ESE CODIGO!")
			lcd.text("ACCESO DENEGADO!",1)
			lcd.text("",2)
		else:
			for row in resultado:
				print(row)
			verde()
			lcd.text("ACCESO CONCEDIDO!",1)
			lcd.text("ABRIENDO PUERTA",2)
			movimientoAbrir()
			aperturaDB(miConexion, 1000)
			
			
	#FUNCION PARA REGISTRAR ROSTRO USANDO LA CLAVEU Y EL NOMBRE DE LA PERSONA
	def registrarRostro(claveU, conexion):
		cur = conexion.cursor()
		sql = "SELECT nombre FROM usuario WHERE claveU = %s"
		val = (claveU,)
		cur.execute(sql,val)
		resultado = cur.fetchall()
		if len(resultado) == 0:
			print("NO EXISTE USUARIO CON ESE CODIGO!")
		else:
			for row in resultado:
				print(row)
				registro(row[0])
				Rostro()
				print("Ya chequea si esta la carpeta")

	def estadoMotor(distancia, conexion):
		cur = conexion.cursor()
		sql = "SELECT motor FROM puertaS"
		sql2 = "UPDATE puertaS SET motor='off'"
		cur.execute(sql)
		resultado = cur.fetchall()
		for row in resultado:
			print(row[0])
			if row[0] == 'on':
				if distancia < 14:
					print("ABRIENDO PUERTA")
					movimientoAbrir()
					sleep(2)
					cur.execute(sql2)
					miConexion.commit()
					print("MOTOR PUESTO EN ESTADO OFF")
				else:
					print("CERRANDO PUERTA")
					movimientoCerrar()
					sleep(2)
					cur.execute(sql2)
					miConexion.commit()
					print("MOTOR PUESTO EN ESTADO OFF")

			
	#FUNCION PARA REGISTRAR EN LA BASE DE DATOS QUE LA PUERTA ACTUALMENTE SE ENCUENTRA ABIERTA	
	def abrirStatus(Distancia, conexion):
		cur = conexion.cursor()
		sql = "UPDATE puertaS SET status=1"
		sql2 = "UPDATE puertaS SET status=0"
		print("Se ha actualizado exitosamente el estado de la puerta")
		if Distancia < 10:
			cur.execute(sql2)
			miConexion.commit()

		else:
			cur.execute(sql)
			miConexion.commit()

			
			

		
################################################################################################################################################################################################

#FUNCION PARA PODER INGRESAR UN CODIGO DE INVITADO VALIDO A LA FUNCION DE BUSCAR INVITADO
def nuevoInvitado():
	codigoU = ""
	lcd.text("ENTER YOUR",1)
	lcd.text("GUEST CODE:",2)
	while len(codigoU) < 4:
		b1 = gpio.input(boton1)
		b2 = gpio.input(boton2)
		b3 = gpio.input(boton3)
		b4 = gpio.input(boton4)
		if b1 == 1:
			codigoU += "1"
			print(codigoU)
			lcd.text(codigoU,1)
			lcd.text("",2)
			sleep(0.5)
		elif b2 == 1:
			codigoU += "2"
			print(codigoU)
			lcd.text(codigoU,1)
			lcd.text("",2)
			sleep(0.5)
		elif b3 == 1:
			codigoU += "3"
			print(codigoU)
			lcd.text(codigoU,1)
			lcd.text("",2)
			sleep(0.5)
		elif b4 == 1:
			codigoU += "4"
			print(codigoU)
			lcd.text(codigoU,1)
			lcd.text("",2)
			sleep(0.5)
	codigoint = int(codigoU)
	DatabaseMySQL.buscarCodigo(codigoint)
	
	
	
def buscarClaveU():
	codigoU = ""
	lcd.text("ENTER YOUR",1)
	lcd.text("claveU CODE:",2)
	while len(codigoU) < 4:
		b1 = gpio.input(boton1)
		b2 = gpio.input(boton2)
		b3 = gpio.input(boton3)
		b4 = gpio.input(boton4)
		if b1 == 1:
			codigoU += "1"
			print(codigoU)
			lcd.text(codigoU,1)
			lcd.text("",2)
			sleep(0.5)
		elif b2 == 1:
			codigoU += "2"
			print(codigoU)
			lcd.text(codigoU,1)
			lcd.text("",2)
			sleep(0.5)
		elif b3 == 1:
			codigoU += "3"
			print(codigoU)
			lcd.text(codigoU,1)
			lcd.text("",2)
			sleep(0.5)
		elif b4 == 1:
			codigoU += "4"
			print(codigoU)
			lcd.text(codigoU,1)
			lcd.text("",2)
			sleep(0.5)
	codigoint = int(codigoU)
	DatabaseMySQL.registrarRostro(codigoint, miConexion)
	
	
#########################################################################################################
##########################################################################################################
###########################################################################################################

iniciarServo()
miConexion = mysql.connect(user='u744130986_VaultGate', password='BXueQ@vEB;g1',host='oaxacapower.org', db='u744130986_VaultGate')
if miConexion.is_connected():
	print("CONECTADO EXITOSAMENTE A LA BASE DE DATOS")

try:
	while True:	
		blanco()
		b1 = gpio.input(boton1)
		b2 = gpio.input(boton2)
		b3 = gpio.input(boton3)
		b4 = gpio.input(boton4)
		
		#TODO ESTO ES LO QUE ESTABA EN VAULTMOVIL	
		gpio.output(trig, gpio.LOW)
		sleep(0.1)
		
		gpio.output(trig, gpio.HIGH)
		sleep(0.00001)
		gpio.output(trig, gpio.LOW)
		
		inicio = time.time()
		while gpio.input(echo) == 0:
			inicio = time.time()
			
		while gpio.input(echo) == 1:
			final = time.time()
		
			
		tiempo_transcurrido = final - inicio
		duracion = tiempo_transcurrido * 34000
		distancia = duracion / 2
		Distancia = round(distancia,2)
		print(Distancia)
		DatabaseMySQL.abrirStatus(Distancia, miConexion)
		DatabaseMySQL.estadoMotor(Distancia, miConexion)
        ################################################	

		if b1 == 1:
			nuevoInvitado()
			sleep(2)
		elif b2 == 1:
			buscarClaveU()
			sleep(2)
		elif b3 == 1:
			Reconocedor(miConexion)
				
		lcd.text("PRESS BUTTON 1",1)
		lcd.text("IF YOU ARE GUEST",2)
		sleep(1.5)
		lcd.text("PRESS BUTTON 2",1)
		lcd.text("TO REGISTER FACE",2)
		sleep(1.5)
		lcd.text("PRESS BUTTON 3",1)
		lcd.text("TO FACE RECON",2)
		sleep(1.5)

except KeyboardInterrupt:
    gpio.cleanup()