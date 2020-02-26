from utils.global_variables import *
from utils.match_config.match_global_variables import *




@match.route(getModelsEndpoint)
class ImageClassifier(Resource):
    @match.doc('get_models')
    def get(self):
        return match_model_dict