
import cv2
import imutils
import numpy as np
from skimage.filters import threshold_local
class Image:
    def __init__(self):
        self.initial_image = None
        self.image = None
        self.contours = None
        self.gray = None
        self.edges = None
        self.threshold = None
        self.points = []
        

    def load(self, width = None, image_name = None):
        print('Loading image...')
        print('Image name: ', image_name)
        self.initial_image = cv2.imread(image_name)

        T = threshold_local(self.initial_image, 15, offset = 10, method = "gaussian")
        
        self.initial_image = (self.initial_image > T).astype("uint8") * 255
        _, self.initial_image= cv2.threshold(self.initial_image, 0, 255, cv2.THRESH_BINARY)
       
        if self.initial_image is None:
            raise Exception('Image not found')

        if width:
            self.initial_image = imutils.resize(self.initial_image, width)
        

        colors = [ (0, 0, 0)]


        # all other colors
        mask = np.zeros(self.initial_image.shape[:2], dtype=bool)

        for color in colors:   
            mask |= (self.initial_image == color).all(-1)

        self.initial_image[~mask] = (255,255,255)
        kernel = np.ones((1,1), np.uint8)
        #self.initial_image = cv2.erode(self.initial_image, kernel, 2)
        self.initial_image = cv2.resize(self.initial_image, (1500,900), interpolation = cv2.INTER_AREA)
        cv2.imshow('show2',self.initial_image)
    
    def process_image(self, image):

        print("Processing image...")

        self.gray = cv2.cvtColor(self.initial_image, cv2.COLOR_BGR2GRAY)
  
        _,self.gray  = cv2.threshold(self.gray, 0, 255, cv2.THRESH_BINARY)

        dilate = cv2.erode(self.gray, np.ones((5,5), np.uint8), iterations = 1)

        self.blur = cv2.GaussianBlur(dilate, (9,9), 0)
        self.edges = cv2.Canny(dilate, 75, 200)

        cv2.imshow('edges', self.edges)
        self.contours = cv2.findContours(self.edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.contours = imutils.grab_contours(self.contours)
        cv2.drawContours(self.initial_image, self.contours, -1, (255,255,255), 1)

        print('Contours finded: ', len(self.contours))
        _, self.threshold = cv2.threshold(self.gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

        self.threshold = cv2.erode(self.threshold, np.ones((3,3), np.uint8), iterations = 1)
        self.threshold = cv2.dilate(self.threshold, np.ones((5,5), np.uint8), iterations = 1)


        self.contours = cv2.findContours(self.threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.contours = imutils.grab_contours(self.contours)
        print("Image processed")


    def display_all(self):
        cv2.imshow('image', self.image)
        cv2.imshow('edges', self.edges)
        cv2.imshow('threshold', self.threshold)



