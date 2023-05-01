import numpy as np
import cv2
import base64
from scipy.spatial.distance import cdist

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
    
    
class Kmeans():
    # types of image input must be bgr
    def __init__(self, image, k_centroids=2, theta=1000, types='RGB'):
        
        # get shape image
        self.rows, self.cols, self.channels = image.shape
        
        # change image to types gray or rgb
        if types == 'GRAY':
            self.channels = 1
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
        self.image = image.copy()
        self.k_centroids = k_centroids
        self.theta = theta
        
        # reshape image to each point data
        self.data = self.image.copy()
        self.data = self.data.reshape((self.rows * self.cols, self.channels))
        
        # create labels
        self.labels = np.full(len(self.data), 0)
        self.centroids = self.data[ np.random.choice(len(self.data), self.k_centroids, replace=False) ]
        
        
        # process img
        self.data = self.fit()

    
    def fit(self):
        Error = 9999999999999
        error = 0
        while abs(Error - error) >= self.theta:
            # print(abs(Error - error))
            Error = error
            error = 0
            
            # get labels and calculate error
            distances = cdist(self.data, self.centroids)
            self.labels = np.argmin(distances, axis= 1)
            error += np.sum(np.min(distances, axis= 1))
            
            
            # update centroid by mean
            for centroid_i in range(self.k_centroids):
                temp = self.data[self.labels == centroid_i]
                new_v = np.sum(temp, axis= 0) / len(temp)
                self.centroids[centroid_i] = new_v
        # replace each data with to mean of the centroid belong
        for centroid_i in range(self.k_centroids):
            self.data[self.labels == centroid_i] = self.centroids[centroid_i]
            
        # reshape image to origin and return output
        if self.channels == 1:
            return self.data.reshape((self.rows, self.cols))
        return self.data.reshape((self.rows, self.cols, self.channels))
    
    def changeBGR2frameb64(self):
        if self.channels == 1:
            self.data = cv2.cvtColor(self.data, cv2.COLOR_GRAY2BGR)
        else:
            self.data = cv2.cvtColor(self.data, cv2.COLOR_RGB2BGR)
        ret, frame_buff = cv2.imencode('.jpg', self.data)
        frame_b64 = base64.b64encode(frame_buff).decode('utf-8')
        return frame_b64
        
    