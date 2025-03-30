import cv2
from PIL import Image
import os

from .picture import Picture


class Video:
    """
    # Video Class

    The `Video`class represent images.
    """

    def __init__(self, video):
        self.video = video


    @property
    def frames(self) -> int:
        """
        The total number of frames of the video.

        Returns:
            int: total number of frames
        """
        frame_count = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        return frame_count
    
    @property
    def fps(self) -> int:
        """
        Frame per second of the video

        Returns:
            int: fps of the video.
        """
        fps = self.video.get(cv2.CAP_PROP_FPS)
        return fps
    
    @property
    def duration(self) -> float:
        """
        Duration in seconds of the video.

        Returns:
            float: duration in seconds of the video
        """
        frame_count = self.frames
        fps = self.fps
        duration = frame_count / fps  # Duration in seconds
        return duration


    def from_file_path(file_path):
        """
        Initialize a video object from the an .mp4 file.

        Arg:
            file_path (str): file path of the .mp4 video.

        Returns:
            Video: a video object.

        Examples:
            >>> video = Video.from_file_path('video_file.mp4')

        """
        video = cv2.VideoCapture(file_path)
        return Video(video)
    


    


    def extract_frames(self, frame_interval=1) -> Picture:
        """
        Extracts frames from the video at a specified interval.

        This method reads frames from the video file and converts them into `Picture` objects.
        Frames are extracted at every `frame_interval` number of frames.

        Args:
            frame_interval (int): The interval at which frames should be extracted.
                                (e.g., `1` extracts every frame, `5` extracts every 5th frame).

        Returns:
            list[Picture]: A list of `Picture` objects containing the extracted frames.

        Example:
            >>> video = Video("example.mp4")
            >>> frames = video.extract_frames(frame_interval=10)
            >>> print(len(frames))  # Outputs the number of frames extracted        
        """
        
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

