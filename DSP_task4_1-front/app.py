from flask import Flask, jsonify, render_template, request ,redirect
import cv2
import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import ifft2, fft2, fftshift
import cmath
import function as fn 

app = Flask(__name__, template_folder="templates")

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method=="POST":
        image1= request.files["profile_pic"]
        path_1 ="DSP_task4_1-front/static/images/image1.png"
        image1.save(path_1)
        image2= request.files["profile_pic2"]
        path_2 ="DSP_task4_1-front/static/images/image2.png"
        image2.save(path_2)

        photo1=cv2.imread("DSP_task4_1-front/static/images/image1.png")
        photo2=cv2.imread("DSP_task4_1-front/static/images/image2.png")

        img1_gray = cv2.cvtColor(photo1,cv2.COLOR_BGR2GRAY)
        img2_gray = cv2.cvtColor(photo2, cv2.COLOR_BGR2GRAY)
        img1,img2 = fn.resize_images(img1_gray,img2_gray)

        img1_fft = np.fft.fftshift(np.fft.fft2(img1))
        img2_fft = np.fft.fftshift(np.fft.fft2(img2))

        fig, ax = plt.subplots()
        ax.imshow (np.log(np.abs(img1_fft)), cmap='gray')
        ax.axis("off")
        fig.savefig("DSP_task4_1-front/static/images/image1_mag.png",bbox_inches="tight",pad_inches=0, dpi=100)

        fig1, ax1 = plt.subplots()
        ax1.imshow (np.angle(img1_fft), cmap='gray')
        ax1.axis("off")
        fig1.savefig("DSP_task4_1-front/static/images/image1_phase.png",bbox_inches="tight",pad_inches=0, dpi=100)

        fig2, ax2 = plt.subplots()
        ax2.imshow (np.log(np.abs(img2_fft)), cmap='gray')
        ax2.axis("off")
        fig2.savefig("DSP_task4_1-front/static/images/image2_mag.png",bbox_inches="tight",pad_inches=0, dpi=100)

        fig3, ax3= plt.subplots()
        ax3.imshow (np.angle(img2_fft), cmap='gray')
        ax3.axis("off")
        fig3.savefig("DSP_task4_1-front/static/images/image2_phase.png",bbox_inches="tight",pad_inches=0, dpi=100)


        imageMixes = [["image_mixed_mag1_p2",[0,1]],["image_mixed_mag2_p1",[1,0]],["image_mixed_mag2_mag1",[0,0]],["image_mixed_p1_p2",[1,1]]]
        for i in range(len(imageMixes)):
            imgCombined = fn.Process_images(img1,img2,imageMixes[i][1])
            fig4, ax4= plt.subplots()
            ax4.imshow (imgCombined, cmap='gray')
            ax4.axis("off")
            fig4.savefig(f"DSP_task4_1-front/static/images/{imageMixes[i][0]}.png",bbox_inches="tight",pad_inches=0, dpi=100)

        return redirect(request.url)

    return render_template('index.html')
    
if __name__ == '__main__':
    app.run(debug=True , port=10000)