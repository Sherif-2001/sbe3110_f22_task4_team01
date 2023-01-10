from flask import Flask, render_template, request
import cv2
import images as fn
import PIL.Image as ImageSave
import io

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
    imageMixed = imageProcess.mixCroppedImages()
    cv2.imwrite(fn.imageMixPath,imageMixed)
    return "Image Mixed Processed"

@app.route("/image/<id>", methods = ["GET", "POST"])
def uploadImage(id):
    if(request.method == "POST"):
        file = request.data
        img = ImageSave.open(io.BytesIO(file))
        if (id == "1"):
            img.save(fn.image1Path)
            photo1 = fn.Image(path=fn.image1Path)
            photo1.saveMagnitudePhaseImages(1)
        elif(id == "2"):
            img.save(fn.image2Path)
            photo2 = fn.Image(path=fn.image2Path)
            photo2.saveMagnitudePhaseImages(2)
    return "image processed"


if __name__ == '__main__':
    app.run(debug=True,port=10000)