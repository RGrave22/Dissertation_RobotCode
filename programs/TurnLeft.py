import time, robotAPI
from xgolib import XGO
from robotAPI import edu
dog = XGO(port="/dev/ttyAMA0",version="xgolite")

robotAPI.rotateWithYaw("l", 90)