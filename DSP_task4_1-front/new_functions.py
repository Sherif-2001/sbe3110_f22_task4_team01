import numpy as np
import cv2
import matplotlib.pylab as plt

image1Path = "DSP_task4_1-front/static/images/image1.png"
image1MagPath = "DSP_task4_1-front/static/images/image1_mag.png"
image1PhasePath = "DSP_task4_1-front/static/images/image1_phase.png"
image2Path = "DSP_task4_1-front/static/images/image2.png"
image2MagPath = "DSP_task4_1-front/static/images/image2_mag.png"
image2PhasePath = "DSP_task4_1-front/static/images/image2_phase.png"

def resize_images(img1,img2):

    img1_resized = cv2.resize(img1, (500, 500))
    img2_resized = cv2.resize(img2, (500, 500))
    cv2.imwrite("./static/images/re_image1.png", img1_resized)
    cv2.imwrite("./static/images/re_image2.png", img2_resized)
    return img1_resized,img2_resized

def cropping_fourier (Fouri_img1,choice_img1,Fouri_img2,choice_img2,cropping_indecies,checkBoxesValue):

    F1_2d=Fouri_img1
    F2_2d=Fouri_img2

    left1    =cropping_indecies[0][0]
    top1     =int(cropping_indecies[0][1]*500/300)
    width1   =cropping_indecies[0][2]
    height1  =int(cropping_indecies[0][3]*500/300)
    left2    =cropping_indecies[1][0]
    top2     =int(cropping_indecies[1][1]*500/300)
    width2   =cropping_indecies[1][2]
    height2  =int(cropping_indecies[1][3]*500/300)

    inside_part1  =F1_2d[top1:top1+height1, left1:left1+width1]
    outside_part1 =F1_2d
    inside_part2  =F2_2d[top2:top2+height2, left2:left2+width2]
    outside_part2 =F2_2d    

    if(checkBoxesValue == [0,0]):
        chosen_part1 = inside_part1
        chosen_part2 = inside_part2    
        if(choice_img1==1):
            rejected_part1 = outside_part1*0
            rejected_part1 =np.exp(1j*rejected_part1)
        elif (choice_img1==0):
                    rejected_part1 =np.ones((500,500))

        if(choice_img2==1):
                    rejected_part2 = outside_part2*0
                    rejected_part2 =np.exp(1j*rejected_part2)

        elif (choice_img2==0):
                    rejected_part2=np.ones((500,500))

        result1 = rejected_part1.copy()
        result2 = rejected_part2.copy()

        result1[top1:top1+height1, left1:left1+width1] = chosen_part1
        result2[top2:top2+height2, left2:left2+width2] = chosen_part2

    elif (checkBoxesValue == [1,1]):
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

def mixCroppedImages(img1,img2,choices,dim,checkBoxesValue):
    
    f  = np.fft.fftshift(np.fft.fft2(img1))
    f2 = np.fft.fftshift(np.fft.fft2(img2))

    if  (choices[0]==1 and choices[1] ==1 ):
        print("choice1 phase choice2 phase")

        f, f2 = cropping_fourier(
                np.exp(1j*np.angle(f)), 1, np.exp(1j*np.angle(f2)), 1, dim,checkBoxesValue)
        combined_img1 = np.multiply(f, f2)
        
    elif (choices[0]==0 and choices[1]==1 ):
       f, f2 =cropping_fourier(np.abs(f), 0, np.exp(1j*np.angle(f2)), 1, dim,checkBoxesValue)
        combined_img1 = np.multiply(f, f2)
          
    

    elif (choices[0]==1 and choices[1]==0 ):
        f, f2 = cropping_fourier(
                np.exp(1j*np.angle(f)), 1, np.abs(f2), 0, dim,checkBoxesValue)
        combined_img1 = np.multiply(f, f2)
       

    elif (choices[0]==0 and choices[1]==0 ):
        f, f2 = cropping_fourier(np.abs(f), 0, np.abs(f2), 0, dim,checkBoxesValue)
        combined_img1 = np.multiply(f, f2)
   
    imgCombined = np.real(np.fft.ifft2(np.fft.fftshift(combined_img1)))
 
    cv2.imwrite("/static/images/output_image1.png", imgCombined)

    return imgCombined

def saveMagnitudePhaseImages(image_path,index):
    imageRead = cv2.imread(image_path)

    img_gray = cv2.cvtColor(imageRead,cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img_gray, (500, 500))

    dft = cv2.dft(np.float32(img),flags = cv2.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)

    magnitude_spectrum = 20*np.log(cv2.magnitude(dft_shift[:,:,0],dft_shift[:,:,1]))
    mag, ang = cv2.cartToPolar(dft_shift[:,:,0],dft_shift[:,:,1])

    fig, ax = plt.subplots()
    ax.imshow(magnitude_spectrum, cmap = 'gray')
    ax.axis("off")
    fig.savefig(f"D:\Github Projects\DSP_task4_1\DSP_task4_1-front\static\images\image{index}_mag.png",bbox_inches="tight",pad_inches=0, dpi=100)

    fig1, ax1 = plt.subplots()
    ax1.imshow(ang, cmap = 'gray')
    ax1.axis("off")
    fig1.savefig(f"D:\Github Projects\DSP_task4_1\DSP_task4_1-front\static\images\image{index}_phase.png",bbox_inches="tight",pad_inches=0, dpi=100)

def mixImages(mixtype):

    image1 = cv2.imread(image1Path)
    image2 = cv2.imread(image2Path)

    img1_gray = cv2.cvtColor(image1,cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    img1 = cv2.resize(img1_gray, (500, 500))
    img2 = cv2.resize(img2_gray, (500, 500))

    image1Fourier = np.fft.fftshift(np.fft.fft2(img1))
    image2Fourier = np.fft.fftshift(np.fft.fft2(img2))

    # Magnitude - Magnitude mix
    if (mixtype == [0,0]):
        mixedImg = np.multiply(np.abs(image1Fourier), np.abs(image2Fourier))

    # Magnitude - Phase mix
    elif (mixtype == [0,1]):
        mixedImg = np.multiply(np.abs(image1Fourier), np.exp(1j*np.angle(image2Fourier)))

    # Phase - Magnitude mix
    elif (mixtype == [1,0]):
        mixedImg = np.multiply(np.abs(image2Fourier), np.exp(1j*np.angle(image1Fourier)))

    # Phase - Phase mix
    elif(mixtype == [1,1]):
        mixedImg = np.multiply(np.exp(1j*np.angle(image1Fourier)), np.exp(1j*np.angle(image2Fourier)))

    mixedImg = np.real(np.fft.ifft2(np.fft.fftshift(mixedImg)))
    return mixedImg

def saveMixedImage():
    imageMixes = [["image_mixed_mag1_p2",[0,1]],["image_mixed_mag2_p1",[1,0]],["image_mixed_mag2_mag1",[0,0]],["image_mixed_p1_p2",[1,1]]]
    for i in range(len(imageMixes)):
        mixedImage = mixImages(imageMixes[i][1])
        fig, ax= plt.subplots()
        ax.imshow (mixedImage, cmap='gray')
        ax.axis("off")
        fig.savefig(f"DSP_task4_1-front/static/images/{imageMixes[i][0]}.png",bbox_inches="tight",pad_inches=0, dpi=100)
