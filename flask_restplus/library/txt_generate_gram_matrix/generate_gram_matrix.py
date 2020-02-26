import pandas as PythonPandas
from library.txt_generate_gram_matrix.gram_generator import *
import os
from utils.gram_generator_variables import *
from  utils.global_variables import GRAMMATRICESZIPPEDFOLDER,DOWNLOADFOLDER
from library.txt_generate_gram_matrix.DictionaryGeneratorPatternCompare import *
from utils.helpers.zip_file import zip_folder


def CleanFile(Uploadpath, DownloadPath, DataFileName):
    DataFrameToClean = PythonPandas.read_csv(DataFileName+'.csv')
    DataFrameToClean = PythonPandas.DataFrame(DataFrameToClean.astype(str))
    DataFrameToClean.to_csv(FOLDER_TO_PROCESS + '/1.2.1 Stage File BreakDown per Columns/'+str(DataFileName).split('.')[0]+'.csv',index=False)
    CleanedDataFrame = DataFrameStripper(DownloadPath,DataFrameToClean,DataFileName)
    return CleanedDataFrame


def RemoveNoise(InputDF):
    InputDF = InputDF.replace('  ',' ')
    return InputDF

def DataFrameStripper(DownloadPath,PandasDataFrame,DataFileName):
    CharToClean = PythonPandas.read_csv(CHARACTERSTOCLEANFILE,sep='\n',delimiter='\n')
    WordsToRemove = CharToClean['Data_To_Clean']
    PandasDataFrame[PandasDataFrame.columns[1]].replace('[\\!"#\'()*+,-.|/:;<=>?@\[\]^_`{|}~’”“′‘]', '', regex=True, inplace=True)
    for Indx,RMVWords in WordsToRemove.iteritems():
        PandasDataFrame[PandasDataFrame.columns[1]]=PandasDataFrame[PandasDataFrame.columns[1]].apply(lambda x: re.sub( '\s'+RMVWords+'\s',' ',x))
        PandasDataFrame[PandasDataFrame.columns[1]] = PandasDataFrame[PandasDataFrame.columns[1]].apply(lambda x: re.sub(r'\b' + RMVWords + r'\b', ' ', x))
        PandasDataFrame[PandasDataFrame.columns[1]] = PandasDataFrame[PandasDataFrame.columns[1]].apply(lambda x: re.sub(r'\b' + '\w{1}' + r'\b', ' ', x))
        PandasDataFrame[PandasDataFrame.columns[1]] = PandasDataFrame[PandasDataFrame.columns[1]].apply(lambda x: re.sub(r'\b' + '\s{2}' + r'\b', ' ', x))

    # Removing Noise Characters
    PandasDataFrame = RemoveNoise(PandasDataFrame)
    PandasDataFrame.to_csv(DownloadPath+'/'+str(DataFileName).split('.')[0]+'_Cleaned'+'.csv',index=False)
    return PandasDataFrame



def generateGramMatrix(filename,keyField,valField):

    createFolders()
    DataFileName = filename
    SelectedKeys = keyField
    SelectedTexts = valField
    DataFileName = str(DataFileName).split(".")[0]
    UploadPath = FOLDER_TO_PROCESS+'/1 InputDataSet/'
    DownloadPath = FOLDER_TO_PROCESS + '/1.1 Dataset After StopWords Removal/'

    # remove stop words
    FileCleaned = CleanFile(UploadPath, DownloadPath, DataFileName)

    UploadPath = FOLDER_TO_PROCESS + '/1.1 Dataset After StopWords Removal/'
    DownloadPath = FOLDER_TO_PROCESS + '/1.1.1.1 Stage Gram per Description/'
    
    # generate gram file
    GramsGenerated = GenerateGrams(UploadPath, DownloadPath, DataFileName, SelectedKeys,
                                               SelectedTexts)

    UploadPath = FOLDER_TO_PROCESS + '/1.1.1.1 Stage Gram per Description/'
    DownloadPath = FOLDER_TO_PROCESS + '/1.1.1.2 Description Gram With Patterns/'
    
    # generate gram pattern file
    PatternsGenerated = PatternGenerator(UploadPath, DownloadPath, DataFileName, SelectedTexts)

    UploadPath = FOLDER_TO_PROCESS + '/1.2.1 Stage File BreakDown per Columns/'
    DownloadPath = FOLDER_TO_PROCESS + '/1.2.1.1 Stage Gram per Description/'
    
    GramsGenerated = GenerateDirtyGrams(UploadPath, DownloadPath, DataFileName, SelectedKeys,
                                               SelectedTexts)
    UploadPath = FOLDER_TO_PROCESS + '/1.2.1.1 Stage Gram per Description/'
    DownloadPath = FOLDER_TO_PROCESS + '/1.2.1.2 Description Gram With Patterns/'
    
    PatternsGenerated = PatternGenerator(UploadPath, DownloadPath, DataFileName, SelectedTexts)
    
    # Generation of Gram Matrices
    Stage2Files()
    zippedFileOPPath= os.path.join(os.getcwd(),DOWNLOADFOLDER,GRAMMATRICESZIPPEDFOLDER,'{}.zip'.format(DataFileName))
    zip_folder(GRAMMATRIXOPFOLDER,zippedFileOPPath)
    return zippedFileOPPath