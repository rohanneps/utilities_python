from utils.image_classification_models_loader.load_image_models import *
from utils.global_variables import IMAGE_DOWNLOAD_DIR
from keras.applications import imagenet_utils
from keras.applications.inception_v3 import preprocess_input
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img
import numpy as np
import argparse
import cv2
import requests
from utils.weblogger.weblogger import *
from utils.helpers.helpers import downloadImage

MODELS = {
	"vgg16": vgg16Model,
	"vgg19": vgg19Model,
	"inception": inceptionModel,
	"resnet": resnetModel
}

def classifyImage(imageUrl, modelName):
	imagePath = downloadImage(imageUrl,IMAGE_DOWNLOAD_DIR)

	# initialize the input image shape (224x224 pixels) along with
	# the pre-processing function (this might need to be changed
	# based on which model we use to classify our image)
	inputShape = (224, 224)
	preprocess = imagenet_utils.preprocess_input
	
	predictionJsonResponse = {}
	# if we are using the InceptionV3 or Xception networks, then we
	# need to set the input shape to (299x299) [rather than (224x224)]
	# and use a different image processing function
	if modelName in ("inception"):
		inputShape = (299, 299)
		preprocess = preprocess_input
	# load our the network weights from disk (NOTE: if this is the
	# first time you are running this script for a given network, the
	# weights will need to be downloaded first -- depending on which
	# network you are using, the weights can be 90-575MB, so be
	# patient; the weights will be cached and subsequent runs of this
	# script will be *much* faster)
	model = MODELS[modelName]
	#model = Network(weights="imagenet")

	#getting required model object
	try:
		image = load_img(imagePath, target_size=inputShape)
	except:
		predictionJsonResponse['error_msg'] = 'Not a Valid Image'
		logger.info('Image Classification Failed: Not a valid image for url {}'.format(imageUrl))

	# Incase there is no error
	if (predictionJsonResponse.get('error_msg',None)) == None:
		image = img_to_array(image)

		 
		# our input image is now represented as a NumPy array of shape
		# (inputShape[0], inputShape[1], 3) however we need to expand the
		# dimension by making the shape (1, inputShape[0], inputShape[1], 3)
		# so we can pass it through thenetwork
		image = np.expand_dims(image, axis=0)
		 
		# pre-process the image using the appropriate function based on the
		# model that has been loaded (i.e., mean subtraction, scaling, etc.)
		image = preprocess(image)


		# classify the image
		preds = model.predict(image)
		prediction = imagenet_utils.decode_predictions(preds)

		resultProbabilityList = []
		for (i, (imagenetID, label, prob)) in enumerate(prediction[0]):
			resultProbilityJson={
			'label':label,
			'probability':'{:.2f}%'.format(prob * 100)
			}
			resultProbabilityList.append(resultProbilityJson)

		predictionJsonResponse['prediction'] = resultProbabilityList
	return predictionJsonResponse