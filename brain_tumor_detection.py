# -*- coding: utf-8 -*-
"""Brain Tumor  Detection SIP.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1HAgAXd_nQeHTHWdgGNQeYOJs0z3tM0i3
"""

!pip install -q git+https://github.com/THU-MIG/yolov10.git

!wget -P -q https://github.com/jameslahm/yolov10/releases/download/v1.0/yolov10n.pt

!pip install -q roboflow

from roboflow import Roboflow
rf = Roboflow(api_key= "pZEBEeL3bfGXXSQHCJHH")
project = rf.workspace("brain-mri/").project("mri-rskcu")
version = project.version(3)
dataset = version.download("yolov8")

!yolo  task=detect mode=train epochs =260 batch = 32 plots= True\
model = '/content/-q/yolov10n.pt'\
data = '/content/MRI-3/data.yaml'

from ultralytics import YOLOv10
model_path = "/content/runs/detect/train/weights/best.pt"
model = YOLOv10(model_path)
result = model(source = "/content/MRI-3/valid/images", conf = 0.25, save =True)

import glob
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
images = glob.glob("/content/runs/detect/predict/*.jpg")

images_to_display = images[:10]
fig, axes =plt.subplots(2,5, figsize =(20,10))

for i , ax in enumerate(axes.flat):
  if i < len(images_to_display):
    img = mpimg.imread(images_to_display[i])
    ax.imshow(img)
    ax.axis('off')
  else:
    ax.axis('off')
plt.tight_layout()
plt.show()

result =model.predict(source = '/content/MRI-3/valid/images/Tr-gl_0119_jpg.rf.0768b25ee8d4e0aa20df53673dce853e.jpg',imgsz = 640, conf = 0.25)
annotated_img =result[0].plot()
annotated_img[:, :, ::-1]

!pip install gradio

import gradio as gr
import cv2
import numpy as np

def predict(image):
  result =model.predict(source =image,imgsz = 640, conf = 0.25)
  annotated_image =result[0].plot()
  annotated_image[:, :, ::-1]
  return annotated_image

app = gr.Interface(
    fn = predict,
    inputs = gr.Image(type = "numpy", label ="Upload an Image"),
    outputs = gr.Image(type = "numpy", label ="Detect a Brain Tumor"),
    title = "Brain Tumor Detection Using YOLO V10 made for SIP",
    description = "Upload an Image ant eh YOLO V10 model will detect and Annotate the Brain Tumor"
)
app.launch()

from google.colab import drive
drive.mount('/content/drive')

