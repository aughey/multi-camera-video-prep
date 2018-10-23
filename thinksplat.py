import yaml
import sys
import json
import os

os.environ["PATH"] += os.pathsep + "./ffmpeg-4.0.2-win64-static/bin"
os.environ["PATH"] += os.pathsep + "./sox-14.4.2"

class dotdict(dict):
  __getattr__ = dict.get

class Video:
    def __init__(self, camera, index, video_path, probe):
        self.camera = camera
        self.video_path = video_path
        self.file = video_path
        self.index = index
        self.probe = probe
    def rough_offset(self):
        return self.camera.rough_offset(self.index)
    def duration(self):
        return float(self.probe['format']['duration'])
    def begin_offset(self):
        return self.rough_offset();
    def middle_offset(self):
        return self.rough_offset() + self.duration()/2.0 - 65.0;
    def end_offset(self):
        return self.rough_offset() + self.duration() - 130.0;
    def audio_file(self):
        return self.file + ".audio.wav"

class Camera:
    def __init__(self, project, cam,index):
        self.project = project
        self.camera = cam
        self.index = index
        self.offset = int(cam['offset'])
        self.path = os.path.join(project.path,cam["directory"])
        try:
            with open(self.file("probe.json")) as f:
                self.probes = json.loads(f.read())
                self.probes = self.probes['probes']
        except:
            None
    def first_video(self):
        return self.video_files()[0]
    def rough_offset(self,index):
        offset = self.offset
        for i in range(index):
            offset += float(self.probes[i]['format']['duration'])
        return offset
    def ffmpeg_concat(self):
        tmp="concat.txt"
        with open(tmp,"w") as f:
            for file in camera.video_files():
                f.write("file " + file.replace('\\','/') + "\n")
        yield tmp
        os.remove(tmp)
    def file(self,name):
        return os.path.join(self.path,name)
    def all_videos(self):
        return [ Video(self,i,v,probe = self.probes[i]) for i,v in enumerate(self.video_files()) ]
    def video_files(self):
        extensions = ['.mts','.mp4','.avi','.mpg']
        files = [os.path.join(self.path,f) for f in os.listdir(self.path) if os.path.splitext(f)[1].lower() in extensions]
        files.sort()
        return files

class Project:
    def __init__(self, path):
        self.path = path;
        with open(self.file("project.yaml")) as s:
            config = yaml.safe_load(s)
            config["path"] = sys.argv[1]
        self.config = config
    def audio_file(self):
        return os.path.join(self.path,self.config["audio_track"])
    def file(self, name):
        return os.path.join(self.path,name)
    def camera(self,index):
        return Camera(self,self.config["cameras"][index],index)
    def num_cameras(self):
        return len(self.config["cameras"])
    def all_cameras(self):
        return [self.camera(i) for i in range(self.num_cameras())]
