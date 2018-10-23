import thinksplat
import os
import sys
import re
from subprocess import Popen, PIPE
import json

project = thinksplat.Project(sys.argv[1])

for camera in project.all_cameras():
    for file in camera.video_files():
        previewdir = file + "-preview"
        framemapfile = os.path.join(previewdir,"framemap.json")
        print("Keyframing: " + file)
        if os.path.isfile(framemapfile):
            print("   Already keyframed, skipping...")
            continue

        try:
            os.mkdir(previewdir)
        except:
            None
        args = ["ffmpeg","-i", file,"-vf","scale=1920:-1,showinfo","-r",str(5),os.path.join(previewdir,"frame%04d.jpg")]

        process = Popen(args,stdout=PIPE,stderr=PIPE)
        out,err = process.communicate()
        exit_code = process.wait()
        # [Parsed_showinfo_0 @ 000002034c4359c0] n: 298 pts: 888888 pts_time:9.87653 pos: 17982144 fmt:yuv420p sar:1/1 s:1920x1080
        parse = re.compile(".*n:\s*(\d+)\s+pts:\s*(\d+) .*")
        frames = {}
        for line in err.decode("utf-8").split("\n"):
            #print(line)
            if not line.startswith("[Parsed_showinfo"):
                continue
            m = parse.match(line)
            try:
                frame,ptr = [ int(n) for n in m.groups() ]
            except:
                print("Not handling: " + line)
                continue
            frames[frame] = ptr / 90000.0
        with open(framemapfile,"w") as f:
            f.write(json.dumps({"frames": frames}))

    #with open(camera.file("probe.json"),"w") as jsonfile:
    #    jsonfile.write(json.dumps({"probes" : probes}, sort_keys=True, indent=4, separators=(',',': ')))
