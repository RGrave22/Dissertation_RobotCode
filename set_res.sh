#!/bin/bash

xrandr --newmode "1920x1080_60.00" 173.00 1920 2048 2248 2576 1080 1083 1088 1120 -hsync +vsync 2>/dev/null
xrandr --addmode HDMI-1 "1920x1080_60.00" 2>/dev/null
xrandr --output HDMI-1 --mode "1920x1080_60.00"

echo "Resolução definida para 1920x1080!"
