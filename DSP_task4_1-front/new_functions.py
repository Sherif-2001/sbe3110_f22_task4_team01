import pandas as pd
import numpy as np
import cv2
import matplotlib.pylab as plt

def Magnitudephase(img1_fft, img2_fft):
    
    img1_amplitude  = np.sqrt(np.real(img1_fft) * 2 + np.imag(img1_fft) * 2)
    img1_phase      = np.arctan2(np.imag(img1_fft), np.real(img1_fft))
    img2_amplitude  = np.sqrt(np.real(img2_fft) * 2 + np.imag(img2_fft) * 2)
    img2_phase      = np.arctan2(np.imag(img2_fft), np.real(img2_fft))

    return img1_amplitude, img1_phase, img2_amplitude, img2_phase

def draw_requency_domain(img1_fft, img2_fft):
    
    fig, ax = plt.subplots(1,4)

    ax[0].imshow (np.log(np.abs(img1_fft)), cmap='gray')
    ax[1].imshow (np.log(np.abs(img2_fft)),cmap='gray')
    ax[2].imshow (np.angle(img1_fft) , cmap='gray')
    ax[3].imshow (np.angle( img2_fft),cmap='gray')
    fig.savefig('./static/images/all_fig.png')

def resize_images(img1,img2):

    img1_resized = cv2.resize(img1, (500, 500))
    img2_resized = cv2.resize(img2, (500, 500))
    cv2.imwrite("./static/images/re_image1.png", img1_resized)
    cv2.imwrite("./static/images/re_image2.png", img2_resized)
    return img1_resized,img2_resized


def cropping_fourier (Fouri_img1,choice_img1,Fouri_img2,choice_img2,cropping_indecies):

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

    # print("sherif")
    # print("mmm",left1)
    # print(top1)
    # print(width1)
    # print(height1)
    # print(left2)
    # print(top2)
    # print(width2)
    # print(height2)

    inside_part1  =F1_2d[top1:top1+height1, left1:left1+width1]
    outside_part1 =F1_2d
    inside_part2  =F2_2d[top2:top2+height2, left2:left2+width2]
    outside_part2 =F2_2d    

    chosen_part1=inside_part1
    chosen_part2=inside_part2
    
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


    print(rejected_part1)
    print(rejected_part2)

    result1 = rejected_part1.copy()
    result2 = rejected_part2.copy()

    result1[top1:top1+height1, left1:left1+width1] = chosen_part1
    result2[top2:top2+height2, left2:left2+width2] = chosen_part2

    return result1, result2



def Process_images(img1,img2,choices,dim):
    
    f  = np.fft.fft2(img1)
    f  = np.fft.fftshift(f)
    f2 = np.fft.fft2(img2)
    f2 = np.fft.fftshift(f2)

    if  (choices[0]==1 and choices[1] ==1 ):
        print("choice1 phase choice2 phase")

        # combined_img1 = np.multiply(np.exp(1j*np.angle(f)), np.exp(1j*np.angle(f2)))
        f, f2 = cropping_fourier(
                np.exp(1j*np.angle(f)), 1, np.exp(1j*np.angle(f2)), 1, dim)
        combined_img1 = np.multiply(f, f2)
        
    elif (choices[0]==0 and choices[1]==1 ):
             
        # combined_img1 = np.multiply(np.abs(f), np.exp(1j*np.angle(f2)))
        f, f2 =cropping_fourier(np.abs(f), 0, np.exp(1j*np.angle(f2)), 1, dim)
        combined_img1 = np.multiply(f, f2)


    elif (choices[0]==1 and choices[1]==0 ):
        # print("choice1 phase choice2 mag")
        # combined_img1 = np.multiply(np.abs(f2), np.exp(1j*np.angle(f)))
        f, f2 = cropping_fourier(
                np.exp(1j*np.angle(f)), 1, np.abs(f2), 0, dim)
        combined_img1 = np.multiply(f, f2)
       

    elif (choices[0]==0 and choices[1]==0 ):
        # print("choice1 mag choice2 mag")
        # combined_img1 = np.multiply(np.abs(f), np.abs(f2))
        f, f2 = cropping_fourier(np.abs(f), 0, np.abs(f2), 0, dim)
        combined_img1 = np.multiply(f, f2)
   

    imgCombined = np.real(np.fft.ifft2(np.fft.fftshift(combined_img1)))
 
    cv2.imwrite("/static/images/output_image1.png", imgCombined)

    return imgCombined

def read_images(cropped_indecies):
    img_file1="/static/images/image1.png"
    img_file2="/static/images/image2.png"
    
    img1_cv2 = cv2.imread(img_file1)
    img2_cv2 = cv2.imread(img_file2)

    # -------- gray scaled
    img2_gray = cv2.cvtColor(img2_cv2, cv2.COLOR_RGB2GRAY)
    img1_gray = cv2.cvtColor(img1_cv2, cv2.COLOR_RGB2GRAY)

    # ---------resize images
    img1,img2=resize_images(img1_gray,img2_gray)
    Process_images(img1,img2,cropped_indecies)