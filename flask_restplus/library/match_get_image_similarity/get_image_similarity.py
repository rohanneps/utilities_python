import PIL
from PIL import Image
import os, datetime
from utils.helpers.helpers import downloadImage
from utils.global_variables import IMAGE_DOWNLOAD_DIR,All_MODELS_PATH
from .predictSimilarity import *
from utils.match_config.match_global_variables import match_model_name_dict
from utils.weblogger.weblogger import *


def merge_images(image1,image2,img_file,outputDir):
    width1, height1 = image1.size
    width2, height2 = image2.size
    result_width = width1+ width2
    result_height = max(height1, height2)
    result = Image.new("RGB", (result_width, result_height), (255, 255, 255))

    result.paste(im=image1, box=(0, 0))
    result.paste(im=image2, box=(width1, 0))
    mergedImagePath = os.path.join(outputDir,img_file)
    result.save(mergedImagePath)
    return (mergedImagePath)


def get_image_similarity_confidence(model, imageUrl1, imageUrl2):
    imageSimConfJson = {}
    imagePath1 = downloadImage(imageUrl1,IMAGE_DOWNLOAD_DIR)
    imagePath2 = downloadImage(imageUrl2,IMAGE_DOWNLOAD_DIR)

    img1 = Image.open(imagePath1)
    img2 = Image.open(imagePath2)

    # appending time to image name
    now = datetime.datetime.now()
    currentDateTime = '{}{}{}{}{}{}'.format(now.year,now.month,now.day,now.hour,now.minute,now.second)

    mergedImagePath = merge_images(img1,img2,'merged_{}.jpg'.format(currentDateTime),IMAGE_DOWNLOAD_DIR)

    modelPath = os.path.join(All_MODELS_PATH,match_model_name_dict[model])

    logger.info('Model File {} called for urls {} and {} '.format(modelPath,imagePath1, imagePath2))
    resultLabelConf = deeplearning_4models(modelPath ,mergedImagePath)
    label = resultLabelConf.split(',')[0]
    confidence = resultLabelConf.split(',')[1]

    logger.info('Label and confidence {} obtained for urls {} and {}.'.format(resultLabelConf,imageUrl1, imageUrl2))

    return {
        'match': label,
        'confidence': confidence
        }