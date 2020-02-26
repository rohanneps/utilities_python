import os
from library.txt_striphtml.html_stripper import getSourceCode
import datetime

def createFolder(path):
	if not os.path.exists(path):
		os.makedirs(path)



def downloadImage(url, outputDir):
	imageName = url.split('/')[-1]
	if imageName=='':
		imageName = 'temp.jpg'

	# appending time to image name
	now = datetime.datetime.now()
	currentDateTime = '{}{}{}{}{}{}'.format(now.year,now.month,now.day,now.hour,now.minute,now.second)

	imageName = '{}_{}.{}'.format(imageName.split('.')[0],currentDateTime,imageName.split('.')[1])
	imagePath = os.path.join(outputDir,imageName)
	f = open(imagePath,'wb')
	imageContent = getSourceCode(url).content
	f.write(imageContent)
	f.close()
	return imagePath