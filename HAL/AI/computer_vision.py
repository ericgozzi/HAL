
import numpy as np

from ultralytics import YOLO
from PIL import Image

from HAL.pixels.picture import Picture



class Detect:

    def __init__(self, picture: Picture):
        self.picture = picture
        self.results = None

    def detect_objects(self, model_name = "yolo11m.pt"):
        # Load a model
        model = YOLO(model_name)  # load an official model

        # Predict with the model
        self.results = model.predict(self.picture.np_array)  # predict on an image
    

    def get_picture(self) -> Picture:
        picture = Picture.from_array(self.results[0].plot())
        return picture
    
    def get_segmentation_mask(self) -> Picture:
        masks = self.results[0].masks  # This will give you the segmentation masks

        print(masks)