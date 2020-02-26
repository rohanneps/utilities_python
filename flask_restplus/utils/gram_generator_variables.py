import os
from utils.helpers.helpers import createFolder

# Stopwords list file
CHARACTERSTOCLEANFILE = os.path.join('utils','CharsToClean','Characters_To_Clean.csv')


# FOLDER_TO_PROCESS = os.path.join(os.getcwd(),'testrohan')
FOLDER_TO_PROCESS = '/tmp/testrohan'

STAGE2_METADATA = os.path.join(FOLDER_TO_PROCESS,'2. Metadata Stage')
REINFORCE_FOLDER = os.path.join(STAGE2_METADATA,'Reinforcement Data For Analysis')
DICT_FOLDER = os.path.join(REINFORCE_FOLDER,'OneGram_Dictionary_Annotation')

CORREL_FOLDER=REINFORCE_FOLDER+'Comparing_Grams_Correlation/'


GRAMMATRIXOPFOLDER = os.path.join(STAGE2_METADATA,'Reinforcement Data For AnalysisComparing_Grams_Correlation')

def createFolders():

    createFolder(os.path.join(FOLDER_TO_PROCESS,'1.1 Dataset After StopWords Removal'))
    createFolder(os.path.join(FOLDER_TO_PROCESS,'1.2.1 Stage File BreakDown per Columns'))
    createFolder(os.path.join(FOLDER_TO_PROCESS,'1.1.1.1 Stage Gram per Description'))
    createFolder(os.path.join(FOLDER_TO_PROCESS,'1.1.1.2 Description Gram With Patterns'))
    createFolder(os.path.join(FOLDER_TO_PROCESS,'1.2.1.1 Stage Gram per Description'))
    createFolder(os.path.join(FOLDER_TO_PROCESS,'1.2.1.2 Description Gram With Patterns'))