import time, robotAPI
from xgolib import XGO
from robotAPI import edu
dog = XGO(port="/dev/ttyAMA0",version="xgolite")

robotAPI.open_claw()
robotAPI.body_attitude("pf", 15)
robotAPI.arm_position(120, -60)
robotAPI.close_claw()
robotAPI.arm_position(0,150)