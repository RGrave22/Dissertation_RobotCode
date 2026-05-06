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
	#dog.pace("slow")
	robotAPI.arm_position(120,0)
	dog.arm_mode(1)
	#robotAPI.body_attitude("pb",12)
	
	robotAPI.body_translation("f",12)
	robotAPI.body_translation("b",12)
	robotAPI.body_translation("b",18)
	
	
	
	robotAPI.reset_arm()
	
	#dog.mark_time(35 )
	time.sleep(1)
	#dog.mark_time(0)
	
	print(dog.read_battery())
	


	


asyncio.run(main())






