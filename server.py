import subprocess
#matar este sempre primeiro
subprocess.run(["sudo","pkill","-f","main.py"])

import os,time,sys,serial,websocket,json,asyncio,websockets,socket
import multiprocessing as mp
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

MAIN_SCREEN_REFRESH_TIME = 240

connected_clients = set()
current_execution = None #Processo unico de execução do codigo recebido

PROGRAMS_PATH = "/home/pi/Desktop/Dissertation/programs"
showing_programs = False
selected_program = 0
deleting_program = False


print("*****************************************")
print("*************XGO-LITE-SERVER*************")
print("*****************************************")

def draw_main_info():
	print("Clearing LCD")
	edu.lcd_clear()
	#Hostname do robo e IP tambem
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

async def display_main_info():
    
	while True:
		try:
			draw_main_info()                
		except Exception as e:
			print(e)
               
		await asyncio.sleep(MAIN_SCREEN_REFRESH_TIME)


def get_programs():
	files = [f for f in os.listdir(PROGRAMS_PATH) if f.endswith('.py') and f not in ('robotAPI.py',)]
    
	return sorted(files)
	
	
def show_programs():
	programs = get_programs()
	edu.lcd_clear()

    # Header
	edu.lcd_rectangle(0, 0, 320, 28, fill=(0, 50, 100), outline=(0, 50, 100))
	edu.lcd_text(10, 0, "Programs", color=(255, 255, 255), fontsize=20)

	# Lista dos programas
	start = max(0, selected_program - 2)
	visible = programs[start:start + 6]

	for i, filename in enumerate(visible):
		y = 35 + i * 30
		real_idx = start + i
		is_selected = real_idx == selected_program
		name = filename.replace('.py', '')

		if is_selected:
			edu.lcd_rectangle(0, y, 320, y + 28, fill=(0, 100, 200), outline=(0, 100, 200))

		color = (255, 255, 255) if is_selected else (180, 180, 180)
		edu.lcd_text(12, y + 6, name, color=color, fontsize=16)
		
	if not deleting_program:
		# Info dos botoes (controls)
		edu.lcd_rectangle(0, 215, 320, 240, fill=(0, 30, 60), outline=(0, 30, 60))
		edu.lcd_text(5, 221, "B: UP   D: DOWN   C: Execute   A: Back", color=(150, 150, 150), fontsize=12)
	else:
		edu.lcd_rectangle(0, 215, 320, 240, fill=(0, 30, 60), outline=(0, 30, 60))
		edu.lcd_text(5, 221, "B: UP   D: DOWN   C: Delete   A: Back", color=(150, 150, 150), fontsize=12)

async def buttons_actions():    
	global selected_program, showing_programs, current_execution, deleting_program
	confirming_delete = False
	
	while True:
		is_running = current_execution is not None and current_execution.is_alive()
		
		if (edu.xgoButton("a") and not is_running):
			showing_programs = not showing_programs
			deleting_program = False
			confirming_delete = False
			
			if(showing_programs):
				selected_program = 0
				show_programs()
			else:
				showing_programs = False
				draw_main_info()
			await asyncio.sleep(0.5)
			
		if (edu.xgoButton("c") and not is_running and not showing_programs):
			showing_programs = not showing_programs
			deleting_program = True
			
			if(showing_programs):
				selected_program = 0
				show_programs()
			else:
				showing_programs = False
				draw_main_info()
			await asyncio.sleep(0.5)
		
		if(showing_programs and not is_running):
			programs = get_programs()
			
			if(edu.xgoButton("b") and not confirming_delete):
					selected_program = max(0, selected_program - 1)
					show_programs()
					await asyncio.sleep(0.5)
				
				
			elif(edu.xgoButton("d") and not confirming_delete):
				selected_program = min(len(programs) - 1, selected_program + 1)
				show_programs()
				await asyncio.sleep(0.25)
			
			if not deleting_program:
				
				if(edu.xgoButton("c")):
					path = os.path.join(PROGRAMS_PATH, programs[selected_program])
					
					edu.lcd_clear()	
					
					with open(path, 'r') as f:
						codigo = f.read()
					
					exec(codigo)
					showing_programs = False
					draw_main_info()
			else:
				
				if not confirming_delete:
					if edu.xgoButton("c"):          
						confirming_delete = True
						show_delete_confirm(programs[selected_program])
						await asyncio.sleep(0.5)
				else:
					
					if edu.xgoButton("c"):
						path = os.path.join(PROGRAMS_PATH, programs[selected_program])
						os.remove(path)
						confirming_delete = False
						programs = get_programs()
						selected_program = max(0, min(selected_program, len(programs) - 1))
                        
						if programs:
							show_programs()
						else:
							showing_programs = False
							deleting_program = False
							draw_main_info()
                        
						await asyncio.sleep(0.5)
                    
					elif edu.xgoButton("b") or edu.xgoButton("d"):
						confirming_delete = False
						show_programs()
						await asyncio.sleep(0.5)
				
				
		await asyncio.sleep(0.1)	

def show_delete_confirm(program_name):
    edu.lcd_clear()
    name = program_name.replace('.py', '')
    if len(name) > 18:
        name = name[:15] + "..."
    
    edu.lcd_rectangle(0, 0, 320, 28, fill=(120, 0, 0), outline=(120, 0, 0))
    edu.lcd_text(10, 4, "Delete program?", color=(255, 255, 255), fontsize=18)
    edu.lcd_text(10, 45, name, color=(255, 220, 0), fontsize=16)
    edu.lcd_rectangle(0, 215, 320, 240, fill=(0, 30, 60), outline=(0, 30, 60))
    edu.lcd_text(5, 221, "C: Confirm         B/D: Cancel", color=(150, 150, 150), fontsize=12)

def kill_current_execution():
	global current_execution
	
	if current_execution != None and current_execution.is_alive():
		current_execution.terminate()
		
	current_execution = None
	
#executa o codigo recebido
def execute_code(code):
	try:
		exec(code)
	except Exception as e:
		print(f"Error executing code: {e}")
		
#monitora a execução do codigo e verifica se foi terminado ou se houve algum tipo de erro
async def execution_monitor(websocket):
	global current_execution
	
	while current_execution is not None and current_execution.is_alive():
		await asyncio.sleep(0.3)
	
	if current_execution is not None and current_execution.exitcode == 0:
		print("execucao feita")
		try:
			await websocket.send(json.dumps({
				"type": "execution_finished"
			}))
		except:
			pass
	current_execution = None


	
#guarda o ficheiro na pasta do robô
def save_file(code, filename):
	path = os.path.join(PROGRAMS_PATH, filename)
	name, py = os.path.splitext(filename)
	
	if os.path.exists(path):
		counter = 1
		while os.path.exists(os.path.join(PROGRAMS_PATH, f"{name} ({counter}){py}")):
			counter += 1
		
		path = os.path.join(PROGRAMS_PATH, f"{name} ({counter}){py}")
	
	with open(path, 'w') as f:
		f.write(code)
		
	return os.path.basename(path)


async def handler(websocket):
	global current_execution
	
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
					
				#Cria sempre um processo paralelo, para que possa ser interrompido
				if((data.get("type") == "python_code") and (not showing_programs)):
					code = data["code"]
					
					kill_current_execution()
					current_execution = mp.Process(target = execute_code, args=(code,), daemon=True)
					current_execution.start()
					asyncio.create_task(execution_monitor(websocket))
					
				if((data.get("type") == "cancel_execution") and (not showing_programs)):
					kill_current_execution()
					
				if((data.get("type") == "upload_code")):
					
					try:
					
						code = data["code"]
						filename = f"{data.get('file_name')}.py"
						
						saved_file = save_file(code, filename)
						await websocket.send(json.dumps({
							"type": "upload_success",
							"file_name": saved_file
						}))
						
					except Exception as e:
						await websocket.send(json.dumps({
							"type": "upload_error",
							"message": str(e)
						}))
						
							
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
	
	asyncio.create_task(display_main_info())
	asyncio.create_task(buttons_actions())
	
	await asyncio.Future()


asyncio.run(main())
