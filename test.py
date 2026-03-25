import os,time,sys,serial,subprocess,websocket,json,asyncio,websockets
from xgolib import XGO
#from xgoedu import XGOEDU
from robotAPI import edu
import sys, socket, robotAPI
sys.path.append("..")
sys.path.append(".")

os.system('sudo chmod 777 /dev/ttyAMA0')
dog = XGO(port='/dev/ttyAMA0', version='xgolite')
#edu= XGOEDU()
version = dog.read_firmware()
dog_type = 'L'


subprocess.run(["sudo","pkill","-f","main.py"]) #Se nao for feito, nao funciona

#subprocess.run(["sudo", "systemctl", "restart", "NetworkManager"])



print(dog_type)
print(version)

bat = dog.read_battery()
print(bat)

hostname = socket.gethostname()
print(hostname)


connected_clients = set()

async def handler(websocket):
	connected_clients.add(websocket)
	print("Client connected")
	
	try:
		async for message in websocket:
			print(f"MSG: {message}")
			
			data = json.loads(message)
			
			try:
				if(data.get("type") == "python_code"):
					code = data["code"]
					exec(code)
					
					
			except json.JSONDecodeError:
				print("Invalid JSON")
				
	except websockets.exceptions.ConnectionClosed as e:
		print(f"Connection closed code: {e.code}")
	except Exception as e:
		print(f"Error on handler: {e}")
	finally:
		print("Client disconnected")
	
	
	
def smooth_wave(reps=4):
    import math

    steps = 15          
    max_angle = 15
    delay = 0.1        

    for _ in range(reps):
        for i in range(steps):
            
            angle = max_angle * math.sin(2 * math.pi * i / steps)
            dog.attitude('p', int(angle))
            time.sleep(delay)

    dog.reset()
	
	
def main():
	dog.reset()
	
	#dog.action(21)
	
	#robotAPI.push_ups(5)
	
	print(dog.read_battery())
	
	
	#robotAPI.body_translation("b", 35)
	#robotAPI.body_attitude("pf", 15)
	#dog.translation("z", 75)
	#dog.periodic_tran("z", 1.5)
	#time.sleep(0.2)
	#dog.leg(1, [0, 0, 75])
	
	time.sleep(0.4)
	dog.leg(3, [-35, 0, 75])
	dog.leg(4, [-35, 0, 75])
	time.sleep(2)
	#time.sleep(4)
	for _ in range(5):
		
		# DESCER
		time.sleep(0.2)
		dog.leg(1, [0, 0, 75])
		dog.leg(2, [0, 0, 75])  
		time.sleep(0.4)

		#SUBIR
		dog.leg(1, [0, 0, 100])
		dog.leg(2, [0, 0, 100])
		time.sleep(0.4)

	dog.reset()
	
	
	#robotAPI.body_translation("f", 35)
	#time.sleep(1)
	#for _ in range(5):
	#	dog.arm(140,20)
	#	time.sleep(0.5)
	#	dog.arm(140,50)
	#	time.sleep(0.5)
	
	#dog.reset()	


asyncio.run(main())





#dog.reset()
#edu.lcd_clear()

#dog.attitude("p",15)
#dog.attitude("y",10)

#dog.claw(0)
#time.sleep(4)
#dog.arm_mode(1)
#dog.arm(120,-70)
#time.sleep(2)
#dog.arm_mode(0)
#dog.arm(-79, -94)
#dog.claw(255)

#dog.move('x', 18)
#time.sleep(5)
#dog.stop()

#dog.reset()
#time.sleep(3)

#time.sleep(4)
#dog.arm_mode(1)
#dog.arm(120,-70)
#time.sleep(2)
#dog.arm_mode(0)
#dog.arm(-79, -94)
#dog.claw(0)

#dog.reset()

#edu.lcd_text(40,40,'Hello, World!', (255,255,255), fontsize=24)
#time.sleep(1)
