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

subprocess.run(["sudo","pkill","-f","main.py"])


print("*****************************************")
print("*************XGO-LITE-SERVER*************")
print("*****************************************")


connected_clients = set()

async def handler(websocket):
	if(len(connected_clients) >= 1):
		print("A different client is already connected, closing connection...")
		await websocket.close()
		return
		
	connected_clients.add(websocket)
	print("Client connected...")
	
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
		connected_clients.remove(websocket)
	except Exception as e:
		print(f"Error on handler: {e}")
	finally:
		print("Client disconnected")
		connected_clients.remove(websocket)
	
		
	
async def main():
	
	print("Starting websocket server...")
	server = await websockets.serve(handler, "0.0.0.0", 8765)
	print("Websocket server ready and listening on port: 8765!")
	await asyncio.Future()


asyncio.run(main())
