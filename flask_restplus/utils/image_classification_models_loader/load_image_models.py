from keras.applications import ResNet50
from keras.applications import InceptionV3
from keras.applications import VGG16
from keras.applications import VGG19

vgg16Model = VGG16(weights="imagenet")
vgg19Model = VGG19(weights="imagenet")
inceptionModel = InceptionV3(weights="imagenet")
resnetModel = ResNet50(weights="imagenet")