
import os
import random
import imutils
import cv2
import numpy
import numpy as np
from keras.preprocessing.image import img_to_array
from keras.models import load_model

def deeplearning_4models(model,Image_name):


    imagePaths=[]
    labels=[]
    seed = 2
    numpy.random.seed(seed)
    random.shuffle(imagePaths)

    print("[INFO] loading network...")

    model=load_model(model)
    count=0

    image = cv2.imread(Image_name)
    image = cv2.resize(image, (28, 28))
    #image = img_to_array(image)
    image=numpy.array(image, dtype="float") / 255.0
    image = img_to_array(image)
    #image = image / 255
    x = np.expand_dims(image, axis=0)
    preds = model.predict(x)
    pred0 = preds[0]
    notSanta = pred0[0]
    santa = pred0[1]
    
    label = "Matched" if santa > notSanta else "UnMatched"
    proba = santa if santa > notSanta else notSanta
    label = "{},{:.2f}%".format(label, proba * 100)
    return label


if __name__ == "__main__":
    model = 'train1_full_model.h5'
    Image_Name = 'merged.jpg'
    deeplearning_4models(model ,Image_Name)

	
	
	










