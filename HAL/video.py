import cv2
from PIL import Image
import os

from HAL import picture
from HAL.picture import Picture


class Video:

    def __init__(self, video):
        self.video = video


    @property
    def frames(self):
        frame_count = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        return frame_count
    
    @property
    def fps(self):
        fps = self.video.get(cv2.CAP_PROP_FPS)
        return fps
    
    @property
    def duration(self):
        frame_count = self.frames
        fps = self.fps
        duration = frame_count / fps  # Duration in seconds
        return duration


    def from_file_path(file_path):
        video = cv2.VideoCapture(file_path)
        return Video(video)
    


    


    def extract_frames(self, frame_interval=1):
        
        pictures = []

        frame_count = 0
        
        while self.video.isOpened():
            success, frame = self.video.read()
            if not success:
                break  # Stop if the video has ended
            
            if frame_count % frame_interval == 0:
                # Convert frame from OpenCV format (BGR) to PIL format (RGB)
                pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                pictures.append(Picture.from_PIL_image(pil_image))  

            frame_count += 1
        
        self.video.release()

        return pictures

