import thinksplat
import os
import sys
from subprocess import Popen, PIPE
os.environ["PATH"] += os.pathsep + "./ffmpeg-4.0.2-win64-static/bin"

project = thinksplat.Project(sys.argv[1])

for camera in project.all_cameras():
    for file in camera.video_files():
    #with camera.ffmpeg_concat as concat:
        args = ["ffmpeg","-i",file, "-y", "-vn", "-f", "wav", file + ".audio.wav"]

        process = Popen(args) #, stdout=PIPE, stderr=PIPE)
        #output, err = process.communicate()
        exit_code = process.wait()
