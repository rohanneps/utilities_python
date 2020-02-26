import pandas as pd
import os
from textblob import TextBlob
from nltk.corpus import stopwords
import datetime
from utils.global_variables import ONEGRAMWORDERRORDIR
from utils.weblogger.weblogger import *


STOPWORDS = set(stopwords.words("english"))

WordsToRemove = ['the', 'an', 'a', 'up', 'there', 'are', 'at', 'by', 'This','to', 'of', 'that', 'you', 
                'your', 'is', 'are', 'or', 'It', 'will', 'as', 'with', 'on', 'from', 'can', 'be','and',
                's', 'whatever', 'EL','for', 'in', 'up', 'out', 'this', 'just', 'go', 'us', 'not', 'it']


def GetLemmaDefinitions(WordTokens):
    BlobText = TextBlob(WordTokens)
    WordsFromBlobs = BlobText.words
    for Words in WordsFromBlobs:
        DictionaryValue = Words.definitions[:1]
        if len(DictionaryValue) > 0:
            return ' '.join(DictionaryValue)
        elif WordTokens.isdigit():
            return 'Number'
        else:
            return 'Error Word.'


def GenerateDictionary(oneGramFilePath):
    OneGram = pd.read_csv(oneGramFilePath)
    (RowNumber, ColumnNumber) = OneGram.shape
    if RowNumber == 0: return 0
    
    WordListAppender = []
    for RowNumbers, WordValues in OneGram['Grams'].iteritems():
        CleanedValues = str(WordValues).strip('.').strip(',"').strip(',').strip('-').strip(':').split('_')
        for UniqueGrams in CleanedValues:
            if (UniqueGrams.lower() not in WordsToRemove) and (UniqueGrams not in WordListAppender) and(UniqueGrams.lower() not in STOPWORDS):
                WordListAppender.append(UniqueGrams)

    GramDataFrame = pd.DataFrame(pd.Series(WordListAppender), columns=['Grams'])
    sourceOneGrameDF = OneGram.copy()
    OneGram['Dictionary'] = GramDataFrame['Grams'].apply(GetLemmaDefinitions)
    OneGram = OneGram[pd.notnull(OneGram['Dictionary'])]
    GramDataFrame = GramDataFrame.join(OneGram['Dictionary'], how='left')
    GramDataFrame = GramDataFrame[pd.notnull(GramDataFrame['Dictionary'])]
    
    GramDataFrame = GramDataFrame[GramDataFrame['Dictionary'] == 'Error Word.']

    errorGramDF = pd.merge(sourceOneGrameDF, GramDataFrame, how='inner', on =['Grams'])

    # Appending current date time to file
    now = datetime.datetime.now()
    currentDateTime = '{}{}{}{}{}{}'.format(now.year,now.month,now.day,now.hour,now.minute,now.second)
    outputFileName = '{}_{}.csv'.format('OneGramWordError',currentDateTime)
    outputFullPath = os.path.join(ONEGRAMWORDERRORDIR,outputFileName)
    logger.info('file path: {}'.format(outputFullPath))
    errorGramDF = errorGramDF.drop_duplicates(keep='last')
    errorGramDF.to_csv(outputFullPath,index=False)
    return {'OutputFileName':outputFullPath}

