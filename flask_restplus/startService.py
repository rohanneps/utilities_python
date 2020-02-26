from utils.global_variables import *
from utils.helpers.helpers import createFolder
from utils.weblogger.weblogger import *
from web_service.txt_striphtml.html_strip_router import *
from web_service.txt_get_attrval_from_attr.get_attr_val_from_attr_router import *
from web_service.txt_get_attr_from_cat.get_attr_from_cat_router import *
from web_service.txt_get_cat_from_attr.get_cat_from_attr_router import *
from web_service.txt_infer_google_category.infer_google_cat_router import *
from web_service.txt_generate_gram.generate_ngram_router import *
from web_service.txt_infer_attribute_value_category.infer_attribute_value_category_router import *
from web_service.txt_get_platform_cat.get_platform_cat_router import *
from web_service.txt_profile_data.profile_data_router import *
from web_service.txt_generate_gram_matrix.generate_gram_matrix_router import *
from web_service.txt_get_one_gram_word_errors.get_one_gram_word_error_router import *

from web_service.match_get_models.get_models_router import *
from web_service.match_get_image_similarity.get_image_similarity_router import *
from web_service.img_classify_image.image_classifier_router import *
# from web_service.img_deeplearning.deep_learning_router import *
# from web_service.img_comparealgos.IMG_Opencv_Numpy_GrayScale_Vectors_COMPARE_router import *

class APIServices():
	def __init__(self):
		self.counter = 0
		self.services = []

	def create(self, data):
		service = data
		service['service_id'] = self.counter = self.counter + 1
		self.services.append(service)

apiServices = APIServices()
apiServices.create({'task': 'Get Attribute from Category','Input':'Category Name','Endpoint':getAttributeFromCategoryEndpoint})
apiServices.create({'task': 'Get Attribute Value from Attribute Name','Input':'Attribute Name','Endpoint':getAttributeValueFromAttributeNameEndpoint})
apiServices.create({'task': 'Get Category from Attribute','Input':'Attribute Name','Endpoint':getCategoryNameFromAttributeNameEndpoint})
apiServices.create({'task': 'Get Stripped Html Content from URL','Input':'Web Page Source Code','Endpoint':getStrippedHtmlTextFromUrlEnpoint})
apiServices.create({'task': 'Generate Word Gra,e','Input':['Number of Gram (1,2,..,10)','Web Page Source Code'],'Endpoint':generateNGramFromHtmlEnpoint})
apiServices.create({'task': 'Google Shopping Category Detection','Input':'Web Page Url','Endpoint':detectGoogleCategoryFromUrlEndpoint})

# Loading Image Classfication Models
# logger.info('Loading Image Classification Models')
# from utils.image_classification_models_loader.load_image_models import *


# Generating File for Gram Matrices
from utils.gram_generator_variables import createFolders
createFolders()

createFolder(os.path.join(PROJECT_ROOT_PATH,DOWNLOADFOLDER))
createFolder(os.path.join(PROJECT_ROOT_PATH,DOWNLOADFOLDER,GRAMMATRICESZIPPEDFOLDER))
createFolder(os.path.join(PROJECT_ROOT_PATH,DOWNLOADFOLDER,PATTERNFOLDER))
createFolder(os.path.join(PROJECT_ROOT_PATH,DOWNLOADFOLDER,DATAPROFILERFOLDER))
createFolder(os.path.join(PROJECT_ROOT_PATH,DOWNLOADFOLDER,ONEGRAMWORDERRORDIR))

createFolder(os.path.join(PROJECT_ROOT_PATH,IMAGE_DOWNLOAD_DIR))

# initialize database and get initial platform dataframes
from utils.db_initializer.initialize_db import * 

@txt.route('/')
class APIServicesListing(Resource):
	@txt.doc('list_services')
	def get(self):
		return apiServices.services


if __name__ =='__main__':
	logger.info('Application Started')


	app.run(debug=True,host='0.0.0.0',port=5001)

