
-> set_res.sh - this file changes the resolution of the pi to 1920x1080 in order to solve a bug using RealVNC Viewer.

-> server.py - this file represents the server and main file of the robot code, this file is executed on boot.

-> robotAPI.py - this file contains the API that contains all the functions that abstract the xgoedu and xgolib libraries.


IMPORTANT: 

a change was made in the robot in order to make server.py execute at boot instead of main.py(Luwu Dynamics software). The changes where made in the file: /home/pi/start1.sh. If you want to return to Luwu dynamics software just make:

	>sudo nano start1.sh
	
comment the code after "Dissertation" and uncomment the code before (the one that runs main.py) 
