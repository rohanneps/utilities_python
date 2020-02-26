from keras.applications.vgg16 import decode_predictions
from keras.applications.vgg19 import decode_predictions
from keras.applications.resnet50 import preprocess_input
from keras.applications.inception_v3 import preprocess_input
from keras.preprocessing import image
from keras.models import model_from_json
from keras.models import Model,load_model
import logging
import pandas as pd

from keras.layers import Input
import numpy as np
import os
import json
import pickle
import cv2
#with open('conf/conf.json') as f:config = json.load(f)

# config variables
test_size     = 0.10
weights       = 'imagenet'
include_top    = True

def deeplearning_4models(model_name,train_path,test_path,model_path,num_classes):
    json_file = open(model_path+model_name + '_json_model' + '.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights(model_path+model_name +'_weights.weights')
    base_model=loaded_model
    print("Loaded model from disk")
    if model_name == "vgg16":

        model = Model(inputs=base_model.input, outputs=base_model.outputs)
        model.save(model_path +model_name + '_full_model.h5')
        model.save_weights(model_path +model_name + '_weights.weights')
        model_json = model.to_json()
        with open(model_path +model_name + '_json_model' + '.json', "w") as json_file:
            json_file.write(model_json)
        image_size = (224, 224)
    elif model_name == "vgg19":

        model = Model(input=base_model.input, output=base_model.outputs)
        model.save(model_path + model_name + '_full_model.h5')
        model.save_weights(model_path + model_name + '_weights.weights')
        model_json = model.to_json()
        with open(model_path + model_name + '_json_model' + '.json', "w") as json_file:
            json_file.write(model_json)
        image_size = (224, 224)
    elif model_name == "resnet50":

        model = Model(input=base_model.input, output=base_model.outputs)
        model.save(model_path + model_name + '_full_model.h5')
        model.save_weights(model_path + model_name + '_weights.weights')
        model_json = model.to_json()
        with open(model_path + model_name + '_json_model' + '.json', "w") as json_file:
            json_file.write(model_json)
        image_size = (224, 224)
    elif model_name == "inceptionv3":

        model = Model(input=base_model.input, output=base_model.outputs)
        model.save(model_path + model_name + '_full_model.h5')
        model.save_weights(model_path + model_name + '_weights.weights')
        model_json = model.to_json()
        with open(model_path + model_name + '_json_model' + '.json', "w") as json_file:
            json_file.write(model_json)
        image_size = (299, 299)
    test_images = []
    for (rootDir, dirNames, filenames) in os.walk(test_path):
        for file in filenames:
            test_images.append(rootDir + '/' + file)

    outputs=[]
    for image_path in test_images:
        path = image_path
        print(path)
        img = image.load_img(path, target_size=image_size)
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        feature = model.predict(x)
        r1=decode_predictions(feature, top=1)[0]
        r1,r2,r3=r1[0]
        outputstr=model_name+','+image_path+','+str(r1)+','+str(r2)+','+str(r3)
        print(outputstr)
        outputs.append(outputstr)

    pdout=pd.DataFrame(outputs)
    pdout.to_csv(model_path+'_'+model_name+'.csv',index=False)
    return pdout

if __name__ == "__main__":
    import sys
    model = sys.argv[1]
    train_path = sys.argv[2]
    test_path = sys.argv[3]
    model_path = sys.argv[4]
    num_classes = sys.argv[5]
    logging.basicConfig(filename=model_path+'DeepLearning_images_Screenshots.log', level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logging.info('Started')
    deeplearning_4models(model,train_path,test_path,model_path,num_classes)
    logging.info('End')