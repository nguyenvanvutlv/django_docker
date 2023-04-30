import numpy as np
import cv2

class ProcessImage():
    def __init__(self, image, action):
        self.image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.action = action
        
        
    def brightness(self, alpha=1, C = 30):
        
        temp_image = self.image.copy()
        rows, cols, channels = self.image.shape
        for channel in range(channels):
            temp_image[:,:, channel] = np.asarray(temp_image[:,:, channel] * alpha + C, dtype=np.int16)
        
        print(temp_image.shape)
        temp_image[temp_image > 255] = 255
        temp_image[temp_image < 0] = 0
        temp_image = cv2.cvtColor(temp_image, cv2.COLOR_RGB2BGR)
        return temp_image
    
    
    def process(self):
        return self.brightness()