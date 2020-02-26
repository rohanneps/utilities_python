from flask import Flask, request
from flask_restplus import Api, Resource, fields
import os


PROJECT_ROOT_PATH = '/home/rohan/Desktop/rohan_backup/Research/Python/Flask_Restplus/RestAPI/Core'

#App Initializer
app = Flask(__name__)
api = Api(app, version='1.0', title='API Services',
    description='API Services Listings',
)

# Api Namespace
txt = api.namespace('txt', description='RestAPI Services')
img = api.namespace('img', description='RestAPI Services')
match = api.namespace('match', description='RestAPI Services')


# Downloadable Folder
DOWNLOADFOLDER = os.path.join(PROJECT_ROOT_PATH,'Downloadables')
PATTERNFOLDER = os.path.join(DOWNLOADFOLDER,'PatternInfered')
DATAPROFILERFOLDER = os.path.join(DOWNLOADFOLDER,'DataProfile')
GRAMMATRICESZIPPEDFOLDER = os.path.join(DOWNLOADFOLDER,'GramMatricesZipped')
IMAGE_DOWNLOAD_DIR = os.path.join(PROJECT_ROOT_PATH,'DownloadedImages')
ONEGRAMWORDERRORDIR = os.path.join(DOWNLOADFOLDER,'OneGramWordError')

# Text Endpoints
getAttributeFromCategoryEndpoint = '/get_category_attributes'
getAttributeValueFromAttributeNameEndpoint = '/get_category_attribute_values'
getCategoryNameFromAttributeNameEndpoint = '/get_attribute_categories'
getStrippedHtmlTextFromUrlEnpoint = '/get_text_from_url'
getTextFromHtmlEnpoint = '/get_text_from_html'
generateNGramFromHtmlEnpoint = '/get_ngram_from_text'
getPlatfromCategoriesEndpoint = '/get_platform_categories'
getOneGramWordErrors = '/get_one_gram_word_errors'

# Data Profiling Endpoint
profileDataEndpoint = '/profile_data'

# Generate Gram Matrix Enpoint
generateGramMatrixEndpoint = '/get_gram_matrix'

# Text Inference Endpoints
detectGoogleCategoryFromUrlEndpoint = '/get_google_taxonomy'
detectAttributeValueCategoryFromTextEndpoint = '/infer_attribute_value_category_from_text'
detectAttributeValueCategoryPatternFromTextEndpoint = '/infer_pattern_attribute_value_category_from_text'


# Image Endpoint
getImageClassification = '/get_image_classification'

# Match Endpoints
getModelsEndpoint = '/get_models'
getImageSimilarityEndpoint = '/get_image_similarity'

# Model folder 
All_MODELS_PATH = os.path.join(PROJECT_ROOT_PATH,'models')

# Log files
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGFOLDER = 'log'
LOGFILE = os.path.join(ROOT_DIR,'..',LOGFOLDER,'api.log')
MICROSERVICELOGFILE = os.path.join(ROOT_DIR,'..',LOGFOLDER,'microService.log')

# File Names
PATTERNINFEREDCATATTRVAL = 'PatternInferedCatAttrVal'
DATAPROFILEFILE = 'DataProfile'



