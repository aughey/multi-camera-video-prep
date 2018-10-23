import sys
import os
sys.path.insert(0, 'cvcalib')
from audiosync.app import SyncVideoApp
import thinksplat
import json

project = thinksplat.Project(sys.argv[1])


for camera in project.all_cameras():


    accumulated_offset = 0
    for video in camera.all_videos():
        print("Video: " + video.file + " Offset: " + str((video.begin_offset(),video.middle_offset(),video.end_offset())))

        video_time_to_reference_time = []

        for o in (video.begin_offset(),video.middle_offset(),video.end_offset()):
            offset0 = o - accumulated_offset
            offset1 = o - video.begin_offset()

            if offset0 < 0:
                offset1 -= offset0
                offset0 = 0

            print((o,offset0,offset1))

            args = {
              "calculate_offset_only": True,
              "videos": [
                project.audio_file(),
                video.audio_file(),
              ],
              "folder": "",
              "audio_delay": [0,0],
              "video_delay": [
                offset0,
                offset1
              ]
              }
            app = SyncVideoApp(thinksplat.dotdict(args))
            try:
                calculated_offset = app.calc_offset(verbose=False)
            except IndexError:
                print("Got an exeception in calc_offset:  Likely out of bounds")
                print(sys.exc_info())
                continue
            print("Calculated Offset: " + str(calculated_offset))
            print("Accumulated_offset: " + str(accumulated_offset))
            video_time_to_reference_time.append([offset1,offset0 - calculated_offset])
            accumulated_offset += calculated_offset
        video_time_to_reference_time.sort(key=lambda x: x[0])
        with open(video.file + ".json","w") as f:
            f.write(json.dumps({"video_time_to_reference_time": video_time_to_reference_time}))
        print(video_time_to_reference_time)
        #sys.exit(0)
