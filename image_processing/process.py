import numpy as np
import cv2
import base64
from scipy.spatial.distance import cdist

class ProcessImage():
    def __init__(self, image):
        self.image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        
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
    # ảnh đầu vào phải là dạng BGR
    def __init__(self, image, k_centroids=2, theta=1000, types='RGB'):
        
        # lấy kích cỡ của ảnh
        self.rows, self.cols, self.channels = image.shape
        
        # chuyển ảnh về dạng RGB hoặc GRAYSCALE tuỳ chọn
        if types == 'GRAY':
            self.channels = 1
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
        self.image = image.copy()
        self.k_centroids = k_centroids
        self.theta = theta
        
        # chuyển ma trận ảnh số về 1 vector gồm các điểm dữ liệu
        # với RGB thì mỗi phần tử trong vector gồm 3 đặc trưng
        # với GRAYSCALE thì mỗi phần tử trong vector gồm 1 đặc trưng
        self.data = self.image.copy()
        self.data = self.data.reshape((self.rows * self.cols, self.channels))
        
        # tạo nhãn cho từng điểm dữ liệu
        self.labels = np.full(len(self.data), 0)
        # tạo k điểm trung tâm bất kì
        self.centroids = self.data[ np.random.choice(len(self.data), self.k_centroids, replace=False) ]
        
        # đưa ra kết quả
        self.data = self.fit()

    
    def fit(self):
        Error = 9999999999999
        error = 0
        while abs(Error - error) >= self.theta:
            # print(abs(Error - error))
            Error = error
            error = 0
            
            # tính toán nhãn cho từng điểm dữ liệu với k điểm trung tâm bằng euclidean và tính toán lỗi
            # - tính khoảng cách từ k điểm trung tâm đến từng điểm dữ liệu
            # - tính arg_min và min với axis=1 là tính theo hàng ngang
            # d = [[1, 3, 2],
            #      [4, 6, 2]] 
            #      [9, 9, 1]]   -> arg_min = [0, 2, 2], min = [1, 2, 1]
            distances = cdist(self.data, self.centroids)
            self.labels = np.argmin(distances, axis= 1)
            error += np.sum(np.min(distances, axis= 1))
            
            
            # cập nhật lại trung tâm bằng trung bình cộng các điểm dữ liệu
            for centroid_i in range(self.k_centroids):
                temp = self.data[self.labels == centroid_i]
                new_v = np.sum(temp, axis= 0) / len(temp)
                self.centroids[centroid_i] = new_v
        # thay thế từng điểm dữ liệu với nhãn của chúng
        for centroid_i in range(self.k_centroids):
            self.data[self.labels == centroid_i] = self.centroids[centroid_i]
            
        # chuyển ảnh về dạng ban đầu
        if self.channels == 1:
            return self.data.reshape((self.rows, self.cols))
        return self.data.reshape((self.rows, self.cols, self.channels))
    
    def changeBGR2frameb64(self):
        # chuyển về base64 để có thể hiển thị trên website
        if self.channels == 1:
            self.data = cv2.cvtColor(self.data, cv2.COLOR_GRAY2BGR)
        else:
            self.data = cv2.cvtColor(self.data, cv2.COLOR_RGB2BGR)
        ret, frame_buff = cv2.imencode('.jpg', self.data)
        frame_b64 = base64.b64encode(frame_buff).decode('utf-8')
        return frame_b64
        
    
class Edges():
    # ảnh đầu vào phải là dạng BGR
    def __init__(self, 
                 image,  
                 type_of_kernel='sobel'):
        self.image = image
        
        self.gx = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
        self.gy = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])

    
    def auto_threshold(self, origin: np.ndarray, 
                    active: tuple= (True, None)):
        """
            công thức tìm ngưỡng tự động
            I    : kích thước ảnh m x n
            G    : số mức xám số mức xám của ảnh
            t[g] : số điểm ảnh có mức xám <= g
            
            m[g] = 1/t[g] * sum(i * h[i])   --> mô men quán tính TB có mức xám <= g
            
            f[g] = t[g] / (m*n - t[g]) * ( m[g] - m[G - 1] )^2
            
            f(theta) = max{f(g)}
            
            
            ví dụ:
            
            image = np.array([[0, 1, 2, 3, 4, 5],
                              [0, 0, 1, 2, 3, 4],
                              [0, 0, 0, 1, 2, 3],
                              [0, 0, 0, 0, 1, 2],
                              [0, 0, 0, 0, 0, 1]])
            
            g   h[g]    t[g]    g.h[g]  sum_(i.h[i])    m[g]    f[g]
            0    15      15       0         0              0    1.35   
            1     5      20       5         5           0.25    1.66
            2     4      24       8        13           0.54    1.54
            3     3      27       9        22           0.81    1.10
            4     2      29       8        30           1.03    0.49
            5     1      30       5        35           1.16      oo
            
            Ngưỡng cần tách là theta=1 ~ f[theta] = 1.66
        """
        active, theta = active
        if not active:
            image = origin.copy()
            image[image <= theta] = 0
            image[image > theta] = 255
            return image
        image = origin.copy()
        rows, cols = image.shape
        element, occur = np.unique(image, return_counts= True)
        histogram = dict(zip(element, occur))
        keys_histogram = list(histogram.keys())
        
        table = np.zeros((len(keys_histogram), 7), dtype= np.float64)
        table[:, 0] = np.array(list(keys_histogram))
        table[:, 1] = np.array([histogram[value] for value in table[:, 0].copy()])
        table[:, 2] = table[:, 1].copy()
        for i in range(1, len(keys_histogram)):
            table[i, 2] += table[i-1, 2]
        # table[:, 3] = table[:, 0].copy() * table[:, 1].copy()
        table[:, 4] = table[:, 0].copy() * table[:, 1].copy()
        for i in range(1, len(keys_histogram)):
            table[i, 4] += table[i-1, 4]
        table[:, 5] = table[:, 4].copy() / table[:, 2].copy()
        table[:-1, -1] = (table[:-1, 2].copy()*((table[:-1, 5].copy()-table[-1, 5]) ** 2))
        table[:-1, -1] /= (rows * cols - table[:-1, 2].copy())
        result = table[:, -1].copy()
        theta = np.argmax(result)
        image[image <= theta] = 0
        image[image > theta] = 255
        return image
        
        
    def conv2D(self,
            image,
            kernel= np.array([[1, 1, 1],
                                [1, 1, 1],
                                [1, 1, 1]]) / 9.0,
            p= 0,
            s= 1):
        """
        image: hình ảnh [Dạng grayscale]
        kernel: bộ lọc, ma trận vuông
        p: [padding] số pixel được thêm xung quanh ảnh
        s: [strides]số pixel di chuyển mỗi lần trượt nhân tích chập
        --> output:
        ảnh có kích cỡ:
        
        (image_size - kernel_size + 2 * padding)
        ---------------------------------------- + 1
                    strides

        """
        rows, cols = image.shape
        krow, kcol = kernel.shape
        row_output = (rows - krow + 2 * p) // s + 1
        col_output = (cols - kcol + 2 * p) // s + 1
        output = np.zeros((row_output, col_output))
        temp = np.zeros((rows + 2 * p, cols + 2 * p))
        if p == 0:
            temp = image.copy()
        else:
            temp[p:-p, p:-p] = image.copy()
        for row in range(0, row_output, s):
            for col in range(0, col_output, s):
                slicing = temp[row: row + krow, col: col + kcol].copy()
                value = np.sum(slicing * kernel, axis=(0, 1))
                output[row//s, col//s] = value
        return output
    
    
    def changeBGR2frameb64(self, data):
        # chuyển về base64 để có thể hiển thị trên website
        data = np.float32(data)
        data = cv2.cvtColor(data, cv2.COLOR_GRAY2BGR)
        # print("SHAPE", data.shape)
        # cv2.imshow('a', data)
        # cv2.waitKey(0)
        ret, frame_buff = cv2.imencode('.jpg', data)
        frame_b64 = base64.b64encode(frame_buff).decode('utf-8')
        return frame_b64
    
    
    def process(self):
        # chuyển ảnh về grayscale
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        # tìm ngưỡng cho ảnh
        auto_threshold_image = self.auto_threshold(gray)
        # tính nhân tích chập với gx
        output_gx = self.conv2D(auto_threshold_image, self.gx, 1)
        # tính nhân tích chập với gy
        output_gy = self.conv2D(auto_threshold_image, self.gy, 1)
        # tính kết quả = sqrt(gx^2 + gy^2)
        output = np.sqrt(np.square(output_gx) + np.square(output_gy))
        # làm cho các giá trị chỉ nhỏ hơn hoặc bằng 255
        output = output / np.max(output) * 255
        # print("SHAPE", output.shape)
        result = self.changeBGR2frameb64(output)
        return result