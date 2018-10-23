import thinksplat
import os
import sys
import stat

project = thinksplat.Project(sys.argv[1])

for camera in project.all_cameras():
    for file in camera.video_files():
        os.chmod(file, stat.S_IREAD)
