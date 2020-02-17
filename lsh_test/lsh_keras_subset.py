from imutils import paths
import random
import os
from keras.applications import VGG16, imagenet_utils
from keras.applications.inception_v3 import preprocess_input
from keras.preprocessing.image import img_to_array, load_img
from lshash.lshash import LSHash
import numpy as np
import pickle

dataset = './subset'
image_path_list = sorted(list(paths.list_images(dataset)))
print(len(image_path_list))

random.seed(42)
random.shuffle(image_path_list)

inputShape = (224, 224)

# image_path_list = []

model = VGG16(weights='imagenet', include_top=False)
preprocess = imagenet_utils.preprocess_input

## LSHash Params

k = 10 # hash size
L = 5  # number of tables
d = 25088 # Dimension of Feature vector	from VGG16 bottleneck

lsh = LSHash(hash_size=k, input_dim=d, num_hashtables=L)

for cnt,image_path in enumerate(image_path_list):
	print(cnt)
	print(image_path)
	continue
	image = load_img(image_path)
	image = image.resize(inputShape)
	image = img_to_array(image)
	image = preprocess(image)
	image = np.expand_dims(image, axis=0)
	image_pred_features = model.predict(image)[0]
	lsh.index(image_pred_features.flatten(), extra_data=image_path)

pickle.dump(lsh, open('pick_keras/lsh.p', "wb"))

lsh = pickle.load(open('pick_keras/lsh.p','rb'))

def getVgg16Features(image_path):
	image = load_img(image_path)
	image = image.resize(inputShape)
	image = img_to_array(image)
	image = preprocess(image)
	image = np.expand_dims(image, axis=0)
	image_pred_features = model.predict(image)[0]
	return image_pred_features


# search images
input_path = '101_ObjectCategories/car_side/image_0085.jpg'
q_features = getVgg16Features(input_path)
n_items=5
response = lsh.query(q_features.flatten(),num_results=n_items+1, distance_func='hamming')

for i in range(len(response)):
	img_path = response[i][0][1]
	print(img_path)