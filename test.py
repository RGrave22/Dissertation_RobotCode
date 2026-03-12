import os,time,sys,serial,subprocess,websocket,json,asyncio,websockets
from xgolib import XGO
from xgoedu import XGOEDU
import sys, socket
sys.path.append("..")

os.system('sudo chmod 777 /dev/ttyAMA0')
dog = XGO(port='/dev/ttyAMA0', version='xgolite')
version = dog.read_firmware()
dog_type = 'L'

subprocess.run(["sudo","pkill","-f","main.py"]) #Se nao for feito, nao funciona

#subprocess.run(["sudo", "systemctl", "restart", "NetworkManager"])

edu= XGOEDU()

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
	
async def main():
	server = await websockets.serve(handler, "0.0.0.0", 8765)
	print("Creating websocket server...")
	await asyncio.Future()


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
