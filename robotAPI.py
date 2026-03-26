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
	time.sleep(0.5)
	return True

def rotate(direction, angle):
	anglePerSec = 30
	
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
	time.sleep(0.5)
	return True	
	
	
def rotateWithYaw(direction, angle):
	dog.reset()
	yaw_init = dog.read_yaw()
	anglePerSec = 30
	
	dirMap = {
		"l":  1,
		"r": -1,
	}
	
	dr = dirMap.get(direction.lower())
	step = anglePerSec * dr
	
	dog.turn(step)
	
	while True:
		yaw_actual = dog.read_yaw()
		rotate = abs(yaw_actual - yaw_init)
		#print(rotate)
		time.sleep(0.1) #para sincronizar os prints (antes pareciam sempre muito meh)
		
		if(rotate >= angle):
			break
		
	dog.stop()
	time.sleep(0.5)
	return True	
	
	

def walk_in_place(legHeight, timeToSleep):
	
	dog.mark_time(legHeight)
	time.sleep(timeToSleep)
	dog.stop()
	return True

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
	return True

def body_attitude(direction, value):

	dirMap = {
		"rr":  ("r", 1),
		"rl":  ("r", -1),
		"pf":  ("p", 1),
		"pb":  ("p", -1),
		"yl":  ("y", 1),
		"yr":  ("y", -1),
	}

	dr = dirMap.get(direction.lower())
	axis, aux = dr

	val = value * aux

	dog.attitude(axis, val)
	time.sleep(1)
	return True

#IMPORTANT ->  ainda falta as translacoes e rotacoes periodicas()


def push_ups(value):
	
	dog.leg(3, [0, 0, 80])   
	dog.leg(4, [0, 0, 80]) 
	time.sleep(0.6) 
	
	for _ in range(value):
		
		# DESCER
		time.sleep(0.2)
		dog.leg(1, [0, 0, 75])
		dog.leg(2, [0, 0, 75])  
		time.sleep(0.4)

		#SUBIR
		dog.leg(1, [0, 0, 90])
		dog.leg(2, [0, 0, 90])
		time.sleep(0.4)

	dog.reset()
	

def worm_dance(sleep):
	
	dog.translation("z", 75)
	time.sleep(1)
	dog.periodic_rot("p", 2.5) #entre 2 e 3 deve ser o ideal
	time.sleep(sleep)
	dog.periodic_rot("p", 0)
	
def tail_whip(sleep):
	
	body_translation("b", 35)
	body_attitude("pf", 15)
	dog.periodic_tran("y", 1.5)
	
	time.sleep(sleep)
	dog.reset()
	

#========================================
#				   Arm
#========================================

def pick_obj():
	robotAPI.body_attitude("pf", 15)
	robotAPI.claw(0)
	robotAPI.arm_position(120, -60)
	time.sleep(0.5)
	robotAPI.claw(255)
	dog.reset()
	time.sleep(2)
	return True
	

def drop_obj():
	robotAPI.body_attitude("pf", 15)
	robotAPI.claw(255)
	robotAPI.arm_position(120, -20)
	time.sleep(0.5)
	robotAPI.claw(0)
	dog.reset()
	time.sleep(2)
	return True

def open_claw():
	dog.claw(0)
	time.sleep(1)
	return True

def close_claw():
	dog.claw(255)
	time.sleep(1)
	return True

def claw(val):
	dog.claw(val)
	time.sleep(1)
	return True

def arm_position(x, z):
	dog.arm(x, z)
	time.sleep(2)
	return True
	
def handshake():
	body_translation("f", 35)
	time.sleep(0.4)
	
	for _ in range(3):
		dog.arm(140,20)
		time.sleep(0.5)
		dog.arm(140,50)
		time.sleep(0.5)
	
	time.sleep(1)
	dog.reset()	
	

#def reset_arm():
#	dog.arm(0, 0) #o dog.reset() da reset ao cao todo, dai testar se da para evitar isso
#	time.sleep(1)
#	return True

