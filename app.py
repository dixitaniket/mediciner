import flask
import cv2
import numpy as np
import base64
from flask import Flask,Response
from flask import request
from scripts import preprocessing_image,get_text_predictions

from flask import jsonify
app=Flask(__name__)

@app.route("/")
def index():
    return "Welcome"

@app.route("/process",methods=["POST"])
def preprocess_image():
    try:
        file=request.files["file"]

        file_string=file.read()
        bytes_as_array=np.frombuffer(file_string,dtype=np.uint8)
        image=cv2.imdecode(bytes_as_array,flags=1)
        images=preprocessing_image(path=None,image=image)
        final_data=get_text_predictions(images)
        return {"filename":file.filename,"shape":image.shape,"text":final_data}
    except Exception as e:
        print(e)
        return {"error":"some error occured please select correct filenames"},500


