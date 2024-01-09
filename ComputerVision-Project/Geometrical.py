from Image import *
from collections import Counter
import matplotlib.pyplot as plt

from imutils.perspective import four_point_transform as FPT
from collections import Counter

class Geometrical():

    def __init__(self, image, cntrs):
        self.img = image
        self.diameter = None
        self.boxes = None
        self.circles = []
        self.limist_XY = None
        self.contours = cntrs
        self.color = (0,255,0)
        self.centers = []
        self.l = []
        self.xx = None
        self.xy = None
        self.linesV = []
        self.spacingY = []
        self.spacingX = []
        self.letters = []
        

    

    def get_diameter(self):
        self.boxes = [list(cv2.boundingRect(c)) for c in self.contours]
        print('Getting diameter...')
        c = Counter([i[2] for i in self.boxes])
        print(c)

        mode = c.most_common(1)[0][0]
        if mode > 1:
            self.diameter = mode
        else:
            self.diameter = c.most_common(2)[1][0]

        print('Most common diameter found')
    

    def get_circles(self):
        for c in self.contours:
            (_,_,w,h) = cv2.boundingRect(c)
        
            asp_ratio = w/float(h)
            if self.diameter*0.2<= w <= self.diameter*2 and 0.2<= asp_ratio <= 2:
                self.circles.append(c)

            


    def sort_contours(self):

        self.boxes = [list(cv2.boundingRect(c)) for c in self.contours]
        
        tolerance =  1.5 * self.diameter

        #for i in range(1):
            #S = sorted(self.boxes, key = lambda x: x[i])
            
            #s = [b[i] for b in S]
            

            #m = s[0]
        
            #for b in S:
            #    if m - tolerance < b[i] < m or m < b[i] < m + tolerance:
            #        b[i] = m
            #    elif b[i] > m + self.diameter:
            #        s = sorted(set(s[s.index(m):]))
            #        m = next(e for e in s if e > m + self.diameter)
            #    self.l.append(s)

        S = sorted(self.boxes, key = lambda x: x[0])
        s = [b[0] for b in S]
        m = s[0]

        for b in S:
            if m - tolerance < b[0] < m or m < b[0] < m + tolerance:
                b[0] = m
            elif b[0] > m + self.diameter:
                for e in s[s.index(m):]:
                    if e > m + self.diameter:
                        m = e
                        break
            
        self.xx = sorted(set(s))
        
        S = sorted(self.boxes, key = lambda x: x[1])
        s = [b[1] for b in S]
        m = s[0]

        for b in S:
            if m - tolerance < b[1] < m or m < b[1] < m + tolerance:
                b[1] = m
            elif b[1] > m + self.diameter:
                for e in s[s.index(m):]:
                    if e > m + self.diameter:
                        m = e
                        break
            
        self.xy = sorted(set(s))
            
            #self.limist_XY = (self.l[0], self.l[1])
            
            #self.l[i] = sorted(set(s))
        zipped = zip(*sorted(zip(self.contours, self.boxes), key = lambda b: b[1][1]*len(self.img) + b[1][0]))
        self.contours, self.boxes = zipped

    def draw_contours(self):

        i = 0

        for q in range(len(self.circles)):
            cv2.drawContours(self.img, self.circles[q], -1 , self.color, 3)
            cv2.putText(self.img,str(i), (self.boxes[q][0]+ self.boxes[q][2]//2, self.boxes[q][1] + self.boxes[1][3]//2), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,0.5,(255,0,0), 2)
            i += 1



    def get_spacing(self):

        def spacing(x):
            space = []
            coor = [b[x] for b in self.boxes]
            for i in range(len(coor)-1):
                c = coor[i+1] - coor[i]
                if c > self.diameter//2: space.append(c)
            return sorted(list(set(space)))

        self.spacingX = spacing(0)
        self.spacingY = spacing(1)

        # smallest x-serapation (between two adjacent dots in a letter)
        m = min(self.spacingX)

        c = 0

        d1 = self.spacingX[0]
        d2 = 0
        d3 = 0

    #   for x in range(len(spacingX)):
    #     if spacingX[x+1] > spacingX[x]*1.1:
    #       c += 1
    #       if d2 == 0: d2 = spacingX[x+1]
    #     if c == 2:
    #       d3 = spacingX[x+1]
    #       break
        
        for x in self.spacingX:
            if d2 == 0 and x > d1*1.3:
                d2 = x
            if d2 > 0 and x > d2*1.3:
                d3 = x
                break
            
       
        prev = 0 # outside

        self.linesV.append(min(self.xx) - (d2 - self.diameter)/2)

        for i in range(1, len(self.xx)):
            diff = self.xx[i] - self.xx[i-1]
            if i == 1 and d2*0.9 < diff:
                self.linesV.append(min(self.xx) - d2 - self.diameter/2)
                prev = 1
            if d1*0.8 < diff < d1*1.2:
                self.linesV.append(self.xx[i-1] + self.diameter + (d1 - self.diameter)/2)
                prev = 1
            elif d2*0.8 < diff < d2*1.1:
                self.linesV.append(self.xx[i-1] + self.diameter + (d2 - self.diameter)/2)
                prev = 0
            elif d3*0.9 < diff < d3*1.1:
                if prev == 1:
                    self.linesV.append(self.xx[i-1] + self.diameter + (d2 - self.diameter)/2)
                    self.linesV.append(self.xx[i-1] + d2 + self.diameter + (d1 - self.diameter)/2)
                else:
                    self.linesV.append(self.xx[i-1] + self.diameter + (d1 - self.diameter)/2)
                    self.linesV.append(self.xx[i-1] + d1 + self.diameter + (d2 - self.diameter)/2)
            elif d3*1.1 < diff:
                if prev == 1:
                    self.linesV.append(self.xx[i-1] + self.diameter + (d2 - self.diameter)/2)
                    self.linesV.append(self.xx[i-1] + d2 + self.diameter + (d1 - self.diameter)/2)
                    self.linesV.append(self.xx[i-1] + d3 + self.diameter + (d2 - self.diameter)/2)
    
                    prev = 0
                else:
                    self.linesV.append(self.xx[i-1] + self.diameter + (d1 - self.diameter)/2)
                    self.linesV.append(self.xx[i-1] + d1 + self.diameter + (d2 - self.diameter)/2)
                    self.linesV.append(self.xx[i-1] + d1 + d2 + self.diameter + (d1 - self.diameter)/2)
                    self.linesV.append(self.xx[i-1] + d1 + d3 + self.diameter + (d2 - self.diameter)/2)
            #         if d2 + d3 < diff:
            #           self.linesV.append(self.xx[i-1] + d1 + 2*d3 - (d2 - self.diameter)/2)
                    prev = 1



        self.linesV.append(max(self.xx) + self.diameter*1.5)
        if len(self.linesV)%2 == 0:
            self.linesV.append(max(self.xx) + d2 + self.diameter)    


    def display_contours(self):

        figsize = (15,30)
        fig=plt.figure(figsize = figsize)
        plt.rcParams['axes.grid'] = False
        plt.rcParams['axes.spines.left'] = False
        plt.axis('off')
        
        plt.imshow(self.img)
        
        for x in self.linesV:
           plt.axvline(x)

        plt.show()   

    def get_letters(self):
        
        
        Bxs = list(self.boxes)
        Bxs.append((100000, 0))
        
        dots = [[]]
        for y in sorted(list(set(self.spacingY))):
            if y > 1.5*self.diameter:
                minYD = y*1.5
                break
            
                   
        # get lines of dots
        for b in range(len(Bxs)-1):
            if Bxs[b][0] < Bxs[b+1][0]:
                 dots[-1].append(Bxs[b][0])
            else:
                if abs(Bxs[b+1][1] - Bxs[b][1]) < minYD:
                    dots[-1].append(Bxs[b][0])
                    dots.append([])
                else:
                    dots[-1].append(Bxs[b][0])
                    dots.append([])
                    if len(dots)%3 == 0 and not dots[-1]:
                        dots.append([])

        #   for d in dots: print(d)
            
        

        
        for r in range(len(dots)):

            if not dots[r]:
                self.letters.append([0 for _ in range(len(self.linesV)-1)])
                continue

            else:
                self.letters.append([])
                c = 0
                i = 0
                while i < len(self.linesV)-1:
                    if c < len(dots[r]):
                        if self.linesV[i] < dots[r][c] < self.linesV[i+1]:
                            self.letters[-1].append(1)
                            c += 1
                        else:
                            self.letters[-1].append(0)
                    else:
                        self.letters[-1].append(0)
                    i += 1

        print('---------------------------------------------')
        print(self.letters)
        print('---------------------------------------------')

        for l in range(len(self.letters)):
            if l%3 == 0: print()
            print(self.letters[l])
        print()
    

 
            

  
  
  