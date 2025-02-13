import numpy as np
import cv2

img = np.random.randint(255, size=(600,600,3),dtype=np.uint8)
# cv2.imshow('RGB',img)
cv2.waitKey(0)

cv2.imwrite("test.jpg", img)