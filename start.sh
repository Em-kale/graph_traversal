#!/bin/bash

rm -r images
rm my_animation.mp4 

manim -g main.py MyScene -s

ffmpeg -framerate 30 -i images/main/MyScene%04d.png -c:v libx264 -vf "fps=30,format=yuv420p" -movflags +faststart my_animation.mp4
