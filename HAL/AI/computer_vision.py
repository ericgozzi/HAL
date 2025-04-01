
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
        masks = self.results[0].masks  # Get segmentation masks
        if masks is None:
            raise ValueError("No segmentation masks found.")
        mask_array = masks.data.cpu().numpy()  # Convert to NumPy array
        mask_array = (mask_array * 255).astype(np.uint8)  # Scale to 8-bit

        # If multiple masks exist, merge them
        if len(mask_array.shape) == 3:
            mask_array = np.max(mask_array, axis=0)

        # Create the mask
        pil_image = Image.fromarray(mask_array, mode="L")
        mask = Picture.from_PIL_image(pil_image)
        mask.invert_colors()
        return mask
