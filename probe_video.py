import thinksplat
import os
import sys
from subprocess import Popen, PIPE
import json

project = thinksplat.Project(sys.argv[1])

for camera in project.all_cameras():
    probes = []
    for file in camera.video_files():
        print("Probing: " + file)
        args = ["ffprobe","-v","quiet","-print_format","json","-show_streams","-show_format", file]

        process = Popen(args, stdout=PIPE, stderr=PIPE)
        output, err = process.communicate()
        exit_code = process.wait()
        data = json.loads(output);
        probes.append(data)

    with open(camera.file("probe.json"),"w") as jsonfile:
        jsonfile.write(json.dumps({"probes" : probes}, sort_keys=True, indent=4, separators=(',',': ')))
