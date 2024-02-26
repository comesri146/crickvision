from threading import Thread
import cv2, time


class ThreadedCamera(object):
    def __init__(self, src):
        self.capture = cv2.VideoCapture(video_path)
        
        # Read the first frame to get the original resolution
        self.ret, self.frame = self.capture.read()
        self.height, self.width, _ = self.frame.shape

        # Define the desired scale factors
        self.scale_x = 0.3 #Scale factor for width
        self.scale_y = 0.3 #Scale factor for height

        # Calculate the new dimensions based on the scale factors
        self.new_width = int(self.width * self.scale_x)
        self.new_height = int(self.height * self.scale_y)
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        # FPS = 1/X
        # X = desired FPS
        self.FPS = 1 / 20
        self.FPS_MS = int(self.FPS * 1000)

        # Start frame retrieval thread
        self.thread = Thread(target=self.update, args=())
        self.frame = None
        self.thread.daemon = True
        self.thread.start()
        print("ThreadedCamera object created")

    def update(self):
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()
            time.sleep(self.FPS)

    
    def show_frame(self):
        # Rescale the frame without changing the resolution
        rescaled_frame = cv2.resize(self.frame, (self.new_width, self.new_height))

        return self.FPS_MS, rescaled_frame

# For getting input of prerecorded video
video_path = "D:\Cricvision\Crickvision Dataset\Different Batting shots in cricket #shorts.mp4"
threaded_camera = ThreadedCamera(video_path)
print("ThreadedCamera instance created")
