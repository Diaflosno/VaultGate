import RPi.GPIO as gpio
from time import sleep
import time
from datetime import datetime


gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)

pinServo = 11
gpio.setup(pinServo, gpio.OUT)

p = gpio.PWM(pinServo, 50) #estamos guardanando que el ancho de hz de 50 p se guarde en esa variable
p.start(2.5) #estamos diciendo que arranque nuestro servo en 0 grados

def Motor():
	p.ChangeDutyCycle(2.5) #0 grados
	sleep(1)
	p.ChangeDutyCycle(10)
	sleep(1)
	print("HOLA")

def movimientoCerrar():
	p.ChangeDutyCycle(2.5)

def movimientoAbrir():
	p.ChangeDutyCycle(10.5)
	
def iniciarServo():
	p.ChangeDutyCycle(2.5)

	
G = 40
R = 38
B = 36

gpio.setup(R, gpio.OUT)
gpio.setup(G, gpio.OUT)
gpio.setup(B, gpio.OUT)

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
