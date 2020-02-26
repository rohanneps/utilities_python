from utils.global_variables import *
from utils.weblogger.weblogger import *
from library.img_deeplearning.All_Deep_Learning import deeplearning_4models
from library.img_deeplearning.ImageDeepLearningClass import ImageDeepLearningClass

imgParams = api.model('deeplearning', {
'model': fields.String(required=True, description='Which Model to USE, Choose One: vgg16, vgg19, resnet50, or inceptionv3'),
'train_path': fields.String(required=True, description='Training images folder path'),
'test_path': fields.String(required=True, description='Test images folder Path'),
'model_path': fields.String(required=True, description='Path to Save Each Model'),
'num_classes': fields.Integer(required=True, description='Number of Classes Folders with Images')

})


def beginProcess():
	DAO = TodoDAO()
	DAO.create({'model': 'vgg16'})
	DAO.create({'model': 'vgg19'})
	DAO.create({'model': 'resnet50'})
	DAO.create({'model': 'inceptionv3'})
	DAO.create({'train_path':'D:/Multiple_Classifier/Learning/1_training/images/'})
	DAO.create({'test_path': 'D:/Multiple_Classifier/Learning/3_test/images/'})
	DAO.create({'model_path': 'D:/Multiple_Classifier/Learning_Output/'})
	DAO.create({'train_path':'D:/Multiple_Classifier/Learning/1_training/images/'})
	DAO.create({'test_path': 'D:/Multiple_Classifier/Learning/3_test/images/'})
	DAO.create({'model_path': 'D:/Multiple_Classifier/Learning_Output/'})
	DAO.create({'train_path':'D:/Multiple_Classifier/Learning/1_training/images/'})
	DAO.create({'test_path': 'D:/Multiple_Classifier/Learning/3_test/images/'})
	DAO.create({'model_path': 'D:/Multiple_Classifier/Learning_Output/'})
	DAO.create({'train_path':'D:/Multiple_Classifier/Learning/1_training/images/'})
	DAO.create({'test_path': 'D:/Multiple_Classifier/Learning/3_test/images/'})
	DAO.create({'model_path': 'D:/Multiple_Classifier/Learning_Output/'})
	DAO.create({'num_classes': '29'})
	DAO.create({'num_classes': '29'})
	DAO.create({'num_classes': '29'})
	DAO.create({'num_classes': '29'})
	return DAO

@img.route('/deeplearning')
class DeepLearning(Resource):
	@img.doc('image_deep_learning')
	@img.expect(imgParams)
	@img.marshal_with(imgParams, code=201)
	def post(self):
		# DAO = ImageDeepLearningClass()
		# output=DAO.create(api.payload)
		output=api.payload
		model=output['model']
		train_path=output['train_path']
		test_path=output['test_path']
		model_path=output['model_path']
		num_classes=output['num_classes']
		final=deeplearning_4models(model,train_path,test_path,model_path,num_classes)
		return final