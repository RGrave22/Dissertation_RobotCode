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
	step_size = 10
	steps_freq = 2.0 # o robo no modo slow da 2 passos por s
	
	time_to_sleep = steps * (1.0/steps_freq)
	
	dir_map = {
		"f": ("x", 1),
		"b": ("x", -1),
		"l": ("y", 1),
		"r": ("y", -1)
	}
	
	
	dr = dir_map.get(direction.lower())
	axis, aux = dr
	
	stepS = step_size * aux
	dog.move(axis, stepS)
	time.sleep(time_to_sleep)
	dog.stop()
	return true
