import pandas as pd
import pandas_profiling
import numpy as np
import os
import datetime
from utils.global_variables import DATAPROFILERFOLDER,DOWNLOADFOLDER,DATAPROFILEFILE


def generateDataProfile(filename):

	try:
		sourceDF = pd.read_csv(filename, encoding='UTF-8')
	except Exception as e:
		return {'error_msg': 'File not found.'}


	dataProfile = pandas_profiling.ProfileReport(sourceDF)

	now = datetime.datetime.now()
	currentDateTime = '{}{}{}{}{}{}'.format(now.year,now.month,now.day,now.hour,now.minute,now.second)

	outputFileName = '{}_{}.html'.format(DATAPROFILEFILE,currentDateTime)
	outputFilePath = os.path.join(DOWNLOADFOLDER,DATAPROFILERFOLDER,outputFileName)
	dataProfile.to_file(outputFilePath)

	return {'ProfileDataOutputFilePath': outputFilePath}