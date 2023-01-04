from flask import Flask, jsonify, render_template, request ,redirect
import cv2
import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import ifft2, fft2, fftshift
import cmath
import images as fn
from images import Image
import PIL.Image as ImageSave
import io

image1Path = "DSP_task4_1-front/static/images/image1.png"
image1MagPath = "DSP_task4_1-front/static/images/image1_mag.png"
image1PhasePath = "DSP_task4_1-front/static/images/image1_phase.png"
image2Path = "DSP_task4_1-front/static/images/image2.png"
image2MagPath = "DSP_task4_1-front/static/images/image2_mag.png"
image2PhasePath = "DSP_task4_1-front/static/images/image2_phase.png"

app = Flask(__name__, template_folder="templates")

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route("/dimensions", methods = ["GET","POST"])
def dimensions():
    data = request.data
    dimensionsStr = data.decode("utf-8").split(",")
    dimensionNum = [eval(i) for i in dimensionsStr]
    dimensions = [dimensionNum[:4],dimensionNum[4:8]]
    choices = dimensionNum[8:10]
    checkBoxes = dimensionNum[-1]
    imageProcess = fn.ImageProcessing(choices,dimensions,checkBoxes)
    imageMixed = imageProcess.ProcessImages()
    cv2.imwrite("DSP_task4_1-front/static/images/image_mix.png",imageMixed)
    return "Image Mixed Processed"

@app.route("/image1", methods = ["GET", "POST"])
def uploadImage1():
    if(request.method == "POST"):
        file = request.data
        img = ImageSave.open(io.BytesIO(file))
        img.save(image1Path)
        photo1 = Image(image1Path)
        photo1.saveMagnitudePhaseImages(1)
    return "image 1 processed"

@app.route("/image2", methods = ["GET", "POST"])
def uploadImage2():
    if(request.method == "POST"):
        file = request.data
        img = ImageSave.open(io.BytesIO(file))
        img.save(image2Path)
        photo2 = Image(image2Path)
        photo2.saveMagnitudePhaseImages(2)
    return "image 2 processed"

if __name__ == '__main__':
    app.run(debug=True , port=10000)