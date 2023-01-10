
import numpy as np
import cv2
import matplotlib.pyplot as plt

image1Path = "DSP_task4_1-front/static/images/image1.png"
image1MagPath = "DSP_task4_1-front/static/images/image1_mag.png"
image1PhasePath = "DSP_task4_1-front/static/images/image1_phase.png"
image2Path = "DSP_task4_1-front/static/images/image2.png"
image2MagPath = "DSP_task4_1-front/static/images/image2_mag.png"
image2PhasePath = "DSP_task4_1-front/static/images/image2_phase.png"
imageMixPath = "DSP_task4_1-front/static/images/image_mix.png"

class Image:
    def __init__(self,image = None,path= None):
        self.image = image
        self.image_path = path
        if path is not None:
            self.prepare()
        
    def prepare(self,height=500, width=500):
        self.image = cv2.imread(self.image_path)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
        self.image = cv2.resize( self.image, (height, width))

    def getFourier(self):
        return np.fft.fftshift(np.fft.fft2(self.image))
        
    def save(self,path):
        fig, ax = plt.subplots()
        ax.imshow(self.image, cmap = 'gray')
        ax.axis("off")
        fig.savefig(path,bbox_inches="tight",pad_inches=0, dpi=100)

    def saveMagnitudePhaseImages(self, index = 0):
        
        dft = cv2.dft(np.float32(self.image),flags = cv2.DFT_COMPLEX_OUTPUT)
        dft_shift = np.fft.fftshift(dft)

        magnitude_spectrum = 20*np.log(cv2.magnitude(dft_shift[:,:,0],dft_shift[:,:,1]))
        mag, phase_spec = cv2.cartToPolar(dft_shift[:,:,0],dft_shift[:,:,1])
        
        magnitude = Image(image = magnitude_spectrum)
        phase = Image(image = phase_spec)

        if (index == 1):
            magnitude.save(image1MagPath)
            phase.save(image1PhasePath)
        elif (index == 2):
            magnitude.save(image2MagPath)
            phase.save(image2PhasePath)        

class ImageProcessing:
    
    def __init__(self,choices, cropping_indecies,checkBoxesValue):
        self.choices = choices
        self.cropping_indecies = cropping_indecies
        self.checkBoxValue = checkBoxesValue

    def mixCroppedImages(self):
        
        image1,image2 = Image(path=image1Path),Image(path=image2Path)

        fourier1,fourier2 = image1.getFourier(),image2.getFourier()
            
        if (self.choices == [0,1]):
            fourier1, fourier2 =self.cropping_fourier(np.abs(fourier1),  np.exp(1j*np.angle(fourier2)))
            image_mixed = np.multiply(fourier1, fourier2)

        elif (self.choices == [1,0]):
            fourier1, fourier2 = self.cropping_fourier(np.exp(1j*np.angle(fourier1)), np.abs(fourier2))
            image_mixed = np.multiply(fourier1, fourier2)

        imgCombined = np.real(np.fft.ifft2(np.fft.fftshift(image_mixed)))
        img= Image(image=imgCombined)
        img.save("DSP_task4_1-front\static\images\image_mix.png")

        return imgCombined

    def getDimensions(self,index):
        dimensions = []
        for i in range(4):
            if i%2 == 0:
                dimensions.append(self.cropping_indecies[index][i])
            else:
                dimensions.append(int(self.cropping_indecies[index][i]*(500/300)))
        return dimensions

    def cropOutside(self,index,inside_part,outside_part):
        dimensions = self.getDimensions(index) 

        if(self.choices[index] == 1):
            rejected_part = outside_part*0
            rejected_part = np.exp(1j*rejected_part)

        elif (self.choices[index] == 0):
            rejected_part = np.ones((500, 500))

        result = rejected_part.copy()
        result[dimensions[1]:dimensions[1]+dimensions[3], dimensions[0]:dimensions[0]+dimensions[2]] = inside_part
        
        return result

    def cropInside(self,index,inside_part,outside_part):

        dimensions = self.getDimensions(index)        

        if(self.choices[index] == 1):
            rejected_part = inside_part*0
            rejected_part = np.exp(1j*rejected_part)

        elif (self.choices[index] == 0):
            rejected_part = np.ones((dimensions[3], dimensions[2]))

        result = outside_part.copy()
        result[dimensions[1]:dimensions[1]+dimensions[3], dimensions[0]:dimensions[0]+dimensions[2]] = rejected_part

        return result

    def cropping_fourier(self, Fourier_img1, Fourier_img2):

        F1_2d,F2_2d = Fourier_img1, Fourier_img2

        dimensions1,dimensions2 = self.getDimensions(0),self.getDimensions(1)

        inside_part1 = F1_2d[dimensions1[1]:dimensions1[1]+dimensions1[3], dimensions1[0]:dimensions1[0]+dimensions1[2]]
        inside_part2 = F2_2d[dimensions2[1]:dimensions2[1]+dimensions2[3], dimensions2[0]:dimensions2[0]+dimensions2[2]]
        outside_part1,outside_part2 = F1_2d, F2_2d
        
        if(self.checkBoxValue == 0):
            result1 = self.cropOutside(0,inside_part1,outside_part1)
            result2 = self.cropOutside(1,inside_part2,outside_part2)
            
        elif (self.checkBoxValue == 1):
            result1 = self.cropInside(0,inside_part1,outside_part1)
            result2 = self.cropInside(1,inside_part2,outside_part2)

        return result1, result2
