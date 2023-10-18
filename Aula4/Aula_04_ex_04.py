import cv2

lena = cv2.imread("./lena.jpg", cv2.IMREAD_GRAYSCALE)
deti = cv2.imread("DETI_Ruido.png", cv2.IMREAD_GRAYSCALE)

lena = cv2.GaussianBlur(lena, (3, 3), 0)
cv2.imshow('lena 3', lena)
lena = cv2.GaussianBlur(lena, (5, 5), 0)
cv2.imshow('lena 4', lena)
lena = cv2.GaussianBlur(lena, (7, 7), 0)
cv2.imshow('lena 5', lena)

deti = cv2.GaussianBlur(deti, (3, 3), 1)
cv2.imshow('deti 3', deti)
deti = cv2.GaussianBlur(deti, (3, 3), 0)
cv2.imshow('deti 3 ---', deti)
deti = cv2.GaussianBlur(deti, (5, 5), 1)
cv2.imshow('deti 5', deti)
deti = cv2.GaussianBlur(deti, (7,7), 1)
cv2.imshow('deti 7', deti)

cv2.waitKey(0)