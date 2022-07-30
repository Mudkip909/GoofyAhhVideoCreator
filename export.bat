@echo off
ffmpeg -f concat -safe 0 -i temp/list.txt -y -c copy temp/exporttemp.webm
ffmpeg -i temp/exporttemp.webm -i input.mp4 -y -map 0 -map 1:a -c:v copy -shortest export.webm
del temp /Q
del temp2 /Q