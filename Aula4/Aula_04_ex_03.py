import cv2

lena = cv2.imread( "Lena_Ruido.png", cv2.IMREAD_GRAYSCALE )
deti = cv2.imread( "DETI_Ruido.png", cv2.IMREAD_GRAYSCALE )




lena = cv2.medianBlur(lena,3)
cv2.imshow('lena 2', lena)
lena = cv2.medianBlur(lena,5)
cv2.imshow('lena 5', lena)
lena = cv2.medianBlur(lena,7)
cv2.imshow('lena 7', lena)

lena = cv2.medianBlur(deti,3)
cv2.imshow('deti 2', deti)
lena = cv2.medianBlur(deti,5)
cv2.imshow('deti 5', deti)
lena = cv2.medianBlur(deti,7)
cv2.imshow('deti 7', deti)


cv2.waitKey(0)