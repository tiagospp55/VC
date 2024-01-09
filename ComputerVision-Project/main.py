from Image import *
from Geometrical import *
from perspective_functions import *
import numpy as np
import matplotlib.pyplot as plt
from translate import *

def main():
    
    
    loaded_image = Image()
    image_name = 'braille4.png'
    warped_name = 'warped.png'

    #belongs to prespective
    img, ratio, orig = load(image_name)
    img, screen = contours(edge(img), img)
   
    warped = perspective(orig, screen.reshape(4, 2) * ratio)
    
    save(warped, warped_name, 900, 900)

    #belongs to image 
    loaded_image.load(image_name = warped_name)    
    #cv2.imshow('warped', loaded_image.initial_image)
    cv2.waitKey(0)
    loaded_image.process_image(warped)


    # geo
    geo = Geometrical(loaded_image.initial_image, loaded_image.contours)
    geo.get_diameter()
    geo.get_circles()
    geo.sort_contours()
    geo.draw_contours()
   
    geo.get_spacing()
    # geo.display_contours()
    geo.get_letters()
    letters = translate(geo.letters)
    

    for i in range(0, len(letters)):
        
        print( str(letters[i]) , end = '')
        
            

    

    cv2.imshow('im2', geo.img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    

if __name__ == '__main__':
    main()