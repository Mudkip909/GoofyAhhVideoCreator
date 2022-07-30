import ffmpeg
import os
import cv2
import math

#Get info on this video... if it exists.
try:
    probe = ffmpeg.probe('input.mp4')
    video = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    fps = int(video['r_frame_rate'].split('/')[0]) 
    frames = int(video['nb_frames'].split('/')[0]) 
    width = int(video['width'])
    height = int(video['height'])
except:
    print("input.mp4 could not be found. is it an mp4 file and is it spelled correctly?")
    sys.exit(1)
#Make the list used for ffmpeg concat
with open('temp/list.txt', 'w') as f:
    for c in range (0,frames):       
    
        f.write("file '" + str(c + 1) +".webm'" + '\n')        
    f.close()


vc = cv2.VideoCapture('input.mp4')
c=1

if vc.isOpened():
    rval , frame = vc.read()
else:
    rval = False

while rval:
    rval, frame = vc.read()
    if (rval):
        
        #Convert to jpg
        cv2.imwrite("temp/" + str(c) + '.jpg',frame)
        #Then convert those jpgs to webm, this can probably be done in 1 step
        (
        ffmpeg
        .input('temp/' + str(c) +'.jpg', pattern_type='none', framerate=fps)
        #Modify this line to change the wavy-ness of the video.
        .filter('scale', w=(24 + abs(math.cos(c/3)*800)), h=(24 + abs(math.sin(c/3)*500)))
        .output('temp/' + str(c) + '.webm')
        .overwrite_output()
        #zzzzzz
        .run(quiet=True)
        )
        print('Frame: ' + str(c) + ' of ' + str(frames))
        c = c + 1
        cv2.waitKey(1)
vc.release()
  
os.startfile("export.bat")
