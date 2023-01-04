import pandas as pd
import numpy as np
import cv2
import matplotlib.pylab as plt

class Image:
    def __init__(self,image=None, path= None):

        self.image = image
        self.image_path = path
        if path is not None:
            self.read()

    def resize(self, height=500, width=500):
    
        self.image = cv2.resize( self.image, (height, width))
        

    def getFourier(self):
        fourier = np.fft.fft2(self.image)
        fourier = np.fft.fftshift(fourier)
        return fourier
        
    def gray_scale(self):
        # truning colored image to gray
        self.image=cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)


    def save(self ,save_path):
        # saving image to given path
        cv2.imwrite(save_path, self.image)

    def read(self):
        #reading the image
        self.image = cv2.imread(self.image_path)
        
    def saveMagnitudePhaseImages(self, index=0):
    
        self.read()
        self.gray_scale()
        self.resize()

        magnitude1 ,phase1=self.MagnitudePhaseImages()


        magnitude1= Image(image=magnitude1)
        magnitude1.save(f"DSP_task4_1-front\static\images\image{index}_mag.png")

        phase1= Image(image=phase1)
        phase1.save(f"DSP_task4_1-front\static\images\image{index}_phase.png")

    def MagnitudePhaseImages(self):
        dft = cv2.dft(np.float32(self.image),flags = cv2.DFT_COMPLEX_OUTPUT)
        dft_shift = np.fft.fftshift(dft)

        magnitude_spectrum = 20*np.log(cv2.magnitude(dft_shift[:,:,0],dft_shift[:,:,1]))
        mag, ang = cv2.cartToPolar(dft_shift[:,:,0],dft_shift[:,:,1])
        return magnitude_spectrum ,ang
    


class ImageProcessing:
    
    def __init__(self,choices, cropping_indecies,checkBoxesValue):
        self.choices = choices
        self.cropping_indecies = cropping_indecies
        self.checkBoxValue = checkBoxesValue
    
    def read_images(self):

        image_file1="DSP_task4_1-front\static\images\image1.png"
        image_file2="DSP_task4_1-front\static\images\image2.png"

        # creating objects

        image1 =Image(path=image_file1)
        image2 =Image(path=image_file2)

        image1.gray_scale()
        image2.gray_scale()

        image1.resize()
        image2.resize()

        return image1,image2


    def ProcessImages(self):
        
        image1,image2=self.read_images()

        f=image1.getFourier()
        f2=image2.getFourier()
            
        if (self.choices[0]==0 and self.choices[1]==1 ):
            #-------------------choice1 mag choice2 phase--------------------- 
            # combined_img1 = np.multiply(np.abs(f), np.exp(1j*np.angle(f2)))
            f, f2 =self.cropping_fourier(np.abs(f),  np.exp(1j*np.angle(f2)))
            combined_img1 = np.multiply(f, f2)


        elif (self.choices[0]==1 and self.choices[1]==0 ):
            #-------------------choice1 phase choice2 mag----------------------
            # combined_img1 = np.multiply(np.abs(f2), np.exp(1j*np.angle(f)))
            f, f2 = self.cropping_fourier(np.exp(1j*np.angle(f)), np.abs(f2))
            combined_img1 = np.multiply(f, f2)


        imgCombined = np.real(np.fft.ifft2(np.fft.fftshift(combined_img1 )))
        img= Image(image=imgCombined)
        img.save("DSP_task4_1-front\static\images\image_mix.png")

        return imgCombined

    def cropping_fourier(self, Fourier_img1, Fourier_img2):

        choice_img1=self.choices[0]
        choice_img2=self.choices[1]

        F1_2d = Fourier_img1
        F2_2d = Fourier_img2

        #  indecies extraction and manipulation

        left1    =self.cropping_indecies[0][0]
        top1     =int(self.cropping_indecies[0][1]*500/300)
        width1   =self.cropping_indecies[0][2]
        height1  =int(self.cropping_indecies[0][3]*500/300)
        left2    =self.cropping_indecies[1][0]
        top2     =int(self.cropping_indecies[1][1]*500/300)
        width2   =self.cropping_indecies[1][2]
        height2  =int(self.cropping_indecies[1][3]*500/300)

        # using indecies to show inside and outside part

        inside_part1 = F1_2d[top1:top1+height1, left1:left1+width1]
        outside_part1 = F1_2d
        inside_part2 = F2_2d[top2:top2+height2, left2:left2+width2]
        outside_part2 = F2_2d
        
        if(self.checkBoxValue == 0):

            chosen_part1 = inside_part1
            chosen_part2 = inside_part2

            if(choice_img1 == 1):
                rejected_part1 = outside_part1*0
                rejected_part1 = np.exp(1j*rejected_part1)
            elif (choice_img1 == 0):
                rejected_part1 = np.ones((500, 500))

            if(choice_img2 == 1):
                rejected_part2 = outside_part2*0
                rejected_part2 = np.exp(1j*rejected_part2)

            elif (choice_img2 == 0):
                rejected_part2 = np.ones((500, 500))

            result1 = rejected_part1.copy()
            result2 = rejected_part2.copy()

            result1[top1:top1+height1, left1:left1+width1] = chosen_part1
            result2[top2:top2+height2, left2:left2+width2] = chosen_part2
            
        elif (self.checkBoxValue == 1):
            chosen_part1 = outside_part1
            chosen_part2 = outside_part2    

            if(choice_img1 == 1):
                rejected_part1 = inside_part1*0
                rejected_part1 = np.exp(1j*rejected_part1)

            elif (choice_img1 == 0):
                rejected_part1 = np.ones((height1, width1))

            if(choice_img2 == 1):
                rejected_part2 = inside_part2*0
                rejected_part2 = np.exp(1j*rejected_part2)
            elif (choice_img2 == 0):
                rejected_part2 = np.ones((height2, width2))

            result1 = chosen_part1.copy()
            result2 = chosen_part2.copy()

            result1[top1:top1+height1, left1:left1+width1] = rejected_part1
            result2[top2:top2+height2, left2:left2+width2] = rejected_part2

        return result1, result2

