#Em principio esta API será para a primeira dificuldade
import os,time,sys,serial,subprocess,websocket,json,asyncio,websockets
from xgolib import XGO
from xgoedu import XGOEDU
import sys, socket
sys.path.append("..")

os.system('sudo chmod 777 /dev/ttyAMA0')
dog = XGO(port='/dev/ttyAMA0', version='xgolite')
edu= XGOEDU()

#========================================
#				Movement
#========================================
def move(direction, steps):
	dog.pace("slow")
	stepSize = 10 # valor default definido
	stepsFreq = 2.0 # o robo no modo slow da 2 passos por s
	
	timeToSleep = steps * (1.0/stepsFreq)
	
	dirMap = {
		"f": ("x", 1),
		"b": ("x", -1),
		"l": ("y", 1),
		"r": ("y", -1)
	}
	
	dr = dirMap.get(direction.lower())
	axis, aux = dr
	
	stepS = stepSize * aux
	dog.move(axis, stepS)
	time.sleep(timeToSleep)
	dog.stop()
	return true

def rotate(direction, angle):
	anglePerSec = 75
	
	timeToSleep = angle / anglePerSec
	
	dirMap = {
		"l":  1,
		"r": -1,
	}
	
	dr = dirMap.get(direction.lower())
	step = anglePerSec * dr
	
	dog.turn(step)
	time.sleep(timeToSleep)
	dog.stop()
	return true	

def walk_in_place(legHeight, timeToSleep):
	
	dog.mark_time(legHeight)
	time.sleep(timeToSleep)
	dog.stop()
	return true

def body_translation(direction, value):

	dirMap = {
		"f":  ("x", 1),
		"b":  ("x", -1),
		"l":  ("y", 1),
		"r":  ("y", -1),
		"z":  ("z", 1),
	}
	
	dr = dirMap.get(direction.lower())
	axis, aux = dr

	val = value * aux

	dog.translation(axis, val)
	time.sleep(1)
	return true

def body_attitude(direction, value):

	dirMap = {
		"rl":  ("r", 1),
		"rr":  ("r", -1),
		"pf":  ("p", 1),
		"pb":  ("p", -1),
		"yf":  ("y", 1),
		"yb":  ("y", -1),
	}

	dr = dirMap.get(direction.lower())
	axis, aux = dr

	val = value * aux

	dog.attitude(axis, val)
	time.sleep(1)
	return true

#IMPORTANT ->  ainda falta as translacoes e rotacoes periodicas()


#========================================
#				   Arm
#========================================

def pick_obj():
	dog.attitude("p",15) #testar se é este o valor correto para o robo se inclinar
	dog.claw(0)
	time.sleep(2)
	dog.arm_mode(1) #verificar se é preciso
	dog.arm(120,-70)
	time.sleep(2)
	dog.arm_mode(0) #verificar se é preciso
	dog.arm(-79, -94)
	dog.claw(255)
	dog.reset() #nao sei se é preciso
	return true

def open_claw():
	dog.claw(0)
	time.sleep(1)
	return true

def close_claw():
	dog.claw(255)
	time.sleep(1)
	return true

def claw(val):
	dog.claw(val)
	time.sleep(1)
	return true

def arm_position(x, z):
	dog.arm(x, z)
	time.sleep(1)
	return true

def reset_arm():
	dog.arm(0, 0) #o dog.reset() da reset ao cao todo, dai testar se da para evitar isso
	time.sleep(1)
	return true

