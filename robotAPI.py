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
def move(direction, steps, pace):
	dog.pace(pace)
	stepSize = 10 # valor default definido
	
	paceMap = {
		"slow": 2.0,
		"normal": 4.0,
		"high": 6.0,
		
	}
	
	stepsFreq = paceMap.get(pace.lower())
	
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
	
	
	

def walk_in_place(legHeight, timeToSleep, pace):
	
	dog.pace(pace)
	
	dog.mark_time(legHeight)
	time.sleep(timeToSleep)
	dog.stop()
	

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
	

def leg(leg, x, y, z):
    
    legMap = {
        "fl": 1,  
        "fr": 2,  
        "br": 3, 
        "bl": 4,
    }

    leg_id = legMap.get(leg.lower())

    dog.leg(leg_id, [x, y, z])
    #time.sleep(1)
    

def leg_motor(leg_str, motor, value):
    legMap = {
        "fl": 1,
        "fr": 2,
        "br": 3,
        "bl": 4,
    }

    posMap = {
        "b": 1,  # bottom
        "m": 2,  # middle
        "t": 3,  # top
    }

    leg_id = legMap[leg_str.lower()]
    pos_id = posMap[motor.lower()]

    motor_id = leg_id * 10 + pos_id

    dog.motor(motor_id, value)
    #time.sleep(1)
   

def pushups():
	dog.motor(31, 73)
	dog.motor(41, 73)
	dog.motor(32, 93)
	dog.motor(42, 93)
	time.sleep(1)
	
	for _ in range(5):
		dog.motor(12, 45)
		dog.motor(22, 45)
		dog.motor(11, 30)
		dog.motor(21, 30)
		time.sleep(1.5)
		
		dog.motor(12, 90)
		dog.motor(22, 90)
		dog.motor(11, -20)
		dog.motor(21, -20)
		time.sleep(1.5)

	time.sleep(0.5)
	dog.reset()
	
def wave():
	dog.action(13)
	time.sleep(7)
	

def worm_dance(sleep):
	
	dog.translation("z", 75)
	time.sleep(1)
	dog.periodic_rot("p", 2.5) 
	time.sleep(sleep)
	dog.periodic_rot("p", 0)
	
def tail_whip():
	
	dog.translation("x", -35)
	time.sleep(0.5)
	dog.attitude("p", 15)
	time.sleep(0.5)
	
	for _ in range(8):
		dog.attitude("y", 3)
		time.sleep(0.2)
		dog.attitude("y", -3)
		time.sleep(0.2)
		
	dog.reset()
	
def lie_down(sleep):
	dog.motor(31, 73)
	dog.motor(41, 73)
	dog.motor(32, 93)
	dog.motor(42, 93)
	
	time.sleep(1)
	
	dog.motor(12, 80)
	dog.motor(22, 80)
	dog.motor(11, -38)
	dog.motor(21, -38)
	dog.motor(13, 31)
	dog.motor(43, 31)
	
	time.sleep(sleep)
	dog.reset()
	
def sit():
	dog.translation("x", -35)
	dog.attitude("p", -20)
	leg_motor("bl", "b", -25)
	leg_motor("br", "b", -25)
	leg_motor("bl", "m", 60)
	leg_motor("br", "m", 60)
	leg_motor("fl", "b", 43)
	leg_motor("fr", "b", 43)
	time.sleep(2)
	
def give_paw():
	dog.reset()
	
	dog.translation("x", -35)
	dog.attitude("p", -20)
	robotAPI.leg_motor("bl", "b", -25)
	robotAPI.leg_motor("br", "b", -25)
	robotAPI.leg_motor("bl", "m", 60)
	robotAPI.leg_motor("br", "m", 60)
	robotAPI.leg_motor("fl", "b", 43)
	robotAPI.leg_motor("fr", "b", 43)
	dog.motor([13,23], [-5, -5])
	time.sleep(1)
	dog.motor(12, -20)
	time.sleep(0.5)
	dog.motor(11, 0)
	time.sleep(3)
	dog.motor(12, 20)
	time.sleep(0.5)
	dog.reset()
	
def paw_wave():
	dog.reset()
	
	dog.translation("x", -35)
	dog.attitude("p", -20)
	leg_motor("bl", "b", -25)
	leg_motor("br", "b", -25)
	leg_motor("bl", "m", 60)
	leg_motor("br", "m", 60)
	leg_motor("fl", "b", 43)
	leg_motor("fr", "b", 43)
	dog.motor([13,23], [-5,-5])
	time.sleep(2)
	
	for _ in range(4):
		
		dog.motor([12, 11], [-50,-65])
		time.sleep(1)
		dog.motor([12, 11], [40,43])
		
		time.sleep(0.7)
        
		dog.motor([22, 21], [-50,-65])
		time.sleep(1)
		dog.motor([22, 21], [40,43])
		time.sleep(0.7)
		
	dog.reset()
	
def salsa_dance():
	dog.reset()
	time.sleep(0.5)
    
	for _ in range(6):
		dog.translation("y", 20)
		dog.attitude("r", 15)
		time.sleep(0.5)
        
		dog.translation("y", 0)
		dog.attitude("r", 0)
		time.sleep(0.3)
        
        
		dog.translation("y", -20)
		dog.attitude("r", -15)
		time.sleep(0.5)
        
        
		dog.translation("y", 0)
		dog.attitude("r", 0)
		time.sleep(0.3)
    
	dog.reset()

def periodic_translation(direction, period, time_to_sleep):
	
	periodMap = {
        "slow": 8,  
        "medium": 4,  
        "fast": 1.5,
	}
    
	pace = periodMap[period.lower()]
    
	dog.periodic_tran(direction, pace)
	time.sleep(time_to_sleep)
	dog.periodic_tran(direction, 0)

def periodic_rotation(direction, period, time_to_sleep):
	
	periodMap = {
        "slow": 8,  
        "medium": 4,  
        "fast": 1.5, 
	}
    
	pace = periodMap[period.lower()]
    
	dog.periodic_rot(direction, pace)
	time.sleep(time_to_sleep)
	dog.periodic_rot(direction, 0)
	
def motor_speed(speed):
	dog.motor_speed(speed)
        
#========================================
#				   Arm
#========================================

def pick_obj():
	body_attitude("pf", 15)
	claw(0)
	arm_position(120, -60)
	time.sleep(0.5)
	claw(255)
	dog.reset()
	time.sleep(2)
	
	

def drop_obj():
	body_attitude("pf", 15)
	claw(255)
	arm_position(120, -20)
	time.sleep(0.5)
	claw(0)
	dog.reset()
	time.sleep(2)
	

def open_claw():
	dog.claw(0)
	time.sleep(1)
	

def close_claw():
	dog.claw(255)
	time.sleep(1)
	

def claw(val):
	dog.claw(val)
	time.sleep(1)
	

def arm_position(x, z):
	dog.arm(x, z)
	time.sleep(2)
	
	
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
	
def reset_arm():
	dog.arm_mode(0)
	arm_position(-40,28)
	
def arm_mode(mode):
	dog.arm_mode(mode)
	
#def reset_arm():
#	dog.arm(0, 0) #o dog.reset() da reset ao cao todo, dai testar se da para evitar isso
#	time.sleep(1)
#	return True


#========================================
#				   Display
#========================================

def text_on_screen_center(text, color):
	edu.lcd_clear()
	fontSize = 30
	screen_w = 320
	screen_h = 240  
	char_w = fontSize * 0.5
	text_w = len(text) * char_w
	
	x = int((screen_w - text_w) / 2)
	y = int((screen_h - fontSize) / 2)

	edu.lcd_text(x, y, text, color, fontSize)
	
def happy_face():
	edu.lcd_clear()
	edu.lcd_picture("faces/happy_face.png", 5, 0)
	
def sad_face():
	edu.lcd_clear()
	edu.lcd_picture("faces/sad_face.png", 5, 0)

def excited_face():
	edu.lcd_clear()
	edu.lcd_picture("faces/excited_face.png", 5, 0)

def sleepy_face():
	edu.lcd_clear()
	edu.lcd_picture("faces/sleepy_face.png", 5, 0)

def angry_face():
	edu.lcd_clear()
	edu.lcd_picture("faces/angry_face.png", 5, 0)

def scared_face():
	edu.lcd_clear()
	edu.lcd_picture("faces/scared_face.png", 5, 0)

def tongue_face():
	edu.lcd_clear()
	edu.lcd_picture("faces/tongue_face.png", 5, 0)	
	
	
def draw_line(x1, y1, x2, y2, color=(255, 255, 255), width=1):
    edu.lcd_line(x1, y1, x2, y2, color=color, width=width)

def draw_arc(x1, y1, x2, y2, angle0, angle1, color=(255, 255, 255), width=1):
    edu.lcd_circle(x1, y1, x2, y2, angle0, angle1, color=color, width=width)

def draw_rectangle(x1, y1, x2, y2, fill=None, outline=(255, 255, 255), width=1):
    edu.lcd_rectangle(x1, y1, x2, y2, fill=fill, outline=outline, width=width)

def draw_text(x, y, content, color=(255, 255, 255), fontsize=16):
    edu.lcd_text(x, y, content, color=color, fontsize=fontsize)
    
def screen_clear():
	edu.lcd_clear()

#========================================
#				   AI (Recognition)
#========================================
def detect_good():
	start = time.time()	
	while time.time() - start < 20:
		result = edu.gestureRecognition()
		print(result)
		
		if result != None:
			ges, (x,y) = result
			if ges == "Good":
				time.sleep(2)
				edu.lcd_clear()
				return True
	edu.lcd_clear()	
	return False

def detect_ok():
	start = time.time()	
	while time.time() - start < 20:
		result = edu.gestureRecognition()
		print(result)
		
		if result != None:
			ges, (x,y) = result
			if ges == "Ok":
				time.sleep(2)
				edu.lcd_clear()
				return True
	edu.lcd_clear()
	return False
	
def detect_number(number):
	start = time.time()	
	while time.time() - start < 20:
		result = edu.gestureRecognition()
		print(result)
		
		if result != None:
			numb, (x,y) = result
			if int(numb) == number:
				time.sleep(2)
				edu.lcd_clear()
				return True
	edu.lcd_clear()
	return False
	
def detect_happy():
	start = time.time()	
	while time.time() - start < 20:
		result = edu.emotion()
		print(result)
		
		if result != None:
			emotion, (x,y) = result
			if emotion == "Happy":
				time.sleep(2)
				edu.lcd_clear()
				return True
	edu.lcd_clear()
	return False

def detect_sad():
	start = time.time()	
	while time.time() - start < 20:
		result = edu.emotion()
		print(result)
		
		if result != None:
			emotion, (x,y) = result
			if emotion == "Sad":
				time.sleep(2)
				edu.lcd_clear()
				return True
	edu.lcd_clear()
	return False
	
def detect_angry():
	start = time.time()	
	while time.time() - start < 20:
		result = edu.emotion()
		print(result)
		
		if result != None:
			emotion, (x,y) = result
			if emotion == "Angry":
				time.sleep(2)
				edu.lcd_clear()
				return True
	edu.lcd_clear()
	return False

def detect_neutral():
	start = time.time()	
	while time.time() - start < 20:
		result = edu.emotion()
		print(result)
		
		if result != None:
			emotion, (x,y) = result
			if emotion == "Neutral":
				time.sleep(2)
				edu.lcd_clear()
				return True
	edu.lcd_clear()
	return False
	
#Deteta apos ter 3 valores iguais seguidos, se nao detetar, segue
def detect_age(interval, inside):
	start = time.time()	
	confirmation = 0
	isInside = str(inside).lower() == "true"
	
	while time.time() - start < 20:
		result = edu.agesex()
		print(result)
		
		if result != None:
			sex, age, (x,y) = result
			
			if(isInside):
				
				if (age == interval):
					confirmation += 1
				else:
					confirmation = 0
					
			else:	
					
				if (age != interval):
					confirmation += 1
				else:
					confirmation = 0
			
			if confirmation >= 3:
				time.sleep(2)
				edu.lcd_clear()
				return True
				
	edu.lcd_clear()
	return False

#========================================
#				   Sounds 
#========================================
def bark():
	edu.xgoSpeaker("sounds/bark.mp3")
	return True

def whine():
    edu.xgoSpeaker("sounds/whine.mp3")
    return True

def howl():
    edu.xgoSpeaker("sounds/howl.mp3")
    return True

def growl():
    edu.xgoSpeaker("sounds/growl.mp3")
    return True

def sleep():
    edu.xgoSpeaker("sounds/sleep.mp3")
    return True


#========================================
#				   Sensors 
#========================================
def update_sensor_display(roll, pitch, yaw):
	edu.lcd_clear()
	edu.lcd_text(20, 60,  f"Roll:  {roll}°",  (255, 255, 255), 30)
	edu.lcd_text(20, 100, f"Pitch: {pitch}°", (255, 255, 255), 30)
	edu.lcd_text(20, 140, f"Yaw:   {yaw}°",   (255, 255, 255), 30)
    
def read_roll():
	roll  = dog.read_roll()
	pitch = dog.read_pitch()
	yaw   = dog.read_yaw()
	update_sensor_display(roll, pitch, yaw)
	return float(roll)
	
def read_pitch():
	roll  = dog.read_roll()
	pitch = dog.read_pitch()
	yaw   = dog.read_yaw()
	update_sensor_display(roll, pitch, yaw)
	return float(pitch)

def read_yaw():
	roll  = dog.read_roll()
	pitch = dog.read_pitch()
	yaw   = dog.read_yaw()
	update_sensor_display(roll, pitch, yaw)
	return float(yaw)
	
def read_battery():
	bat = dog.read_battery()
	return float(bat)
	
#FAZER DO READ_MOTOR() que da os valores todos?
