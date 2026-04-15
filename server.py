import subprocess
#matar este sempre primeiro
subprocess.run(["sudo","pkill","-f","main.py"])

import os,time,sys,serial,websocket,json,asyncio,websockets,socket
from xgolib import XGO
from robotAPI import edu
import sys, socket, robotAPI
sys.path.append("..")
sys.path.append(".")

os.system('sudo chmod 777 /dev/ttyAMA0')
dog = XGO(port='/dev/ttyAMA0', version='xgolite')
#edu= XGOEDU()

version = dog.read_firmware()
dog_type = 'L'



print("*****************************************")
print("*************XGO-LITE-SERVER*************")
print("*****************************************")

async def display_battery():
    
	while True:
		try:
			print("Clearing LCD")
			edu.lcd_clear()

			ip = os.popen("hostname -I").read().strip().split()[0]
			edu.lcd_rectangle(0, 25, 320, 200, fill=(0, 0, 0), outline=(0, 0, 0))  
			edu.lcd_text(90, 60, "XGOBOT", color=(0, 155, 255), fontsize=35)
   
			ip_x = int((320 - len(ip) * 12) / 2)
			edu.lcd_text(ip_x, 180, ip, color=(255,255,255), fontsize = 24)
			
			
			battery = dog.read_battery()
			print(battery)
			if str(battery) == '0':
				print('uart error')
			else:
				# limpa a área
				edu.lcd_rectangle(255, 2, 318, 20, fill=(0, 0, 0), outline=(0, 0, 0))
                
				# retangulo da borda da bateria e polo
				edu.lcd_rectangle(257, 2, 312, 20, fill=None, outline=(255, 255, 255), width=2)
				edu.lcd_rectangle(312, 7, 317, 15, fill=(255, 255, 255), outline=(255, 255, 255))
                
                # preenchimento verde/vermelho
				fill_width = int(49 * battery / 100)
				bar_color = (0, 180, 0) if battery > 20 else (255, 0, 0)
				edu.lcd_rectangle(259, 4, 259 + fill_width, 18, fill=bar_color, outline=bar_color)
                
                # percentagem da bateria
				edu.lcd_text(265, 3, f"{battery}%", color=(255, 255, 255), fontsize=12)
                
		except Exception as e:
			print(e)
               
		await asyncio.sleep(180)
        
    
def display_info():
    ip = os.popen("hostname -I").read().strip().split()[0]
    
    edu.lcd_rectangle(0, 25, 320, 200, fill=(0, 0, 0), outline=(0, 0, 0))  
    edu.lcd_text(90, 60, "XGOBOT", color=(0, 155, 255), fontsize=35)
   
    ip_x = int((320 - len(ip) * 12) / 2)
    edu.lcd_text(ip_x, 180, ip, color=(255,255,255), fontsize = 24)

    
    
    
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
	#display_info()
	asyncio.create_task(display_battery())
	
	await asyncio.Future()


asyncio.run(main())
