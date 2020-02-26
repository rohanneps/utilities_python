import os,errno
import pandas as PythonPandas
from textblob import TextBlob

from utils.gram_generator_variables import *



def Stage2Files():
    UploadPath = FOLDER_TO_PROCESS + '/1.1.1.2 Description Gram With Patterns/'
    DownloadPath = REINFORCE_FOLDER + 'Comparing_Grams_Correlation/'
    try:
        os.makedirs(DownloadPath)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    CompareGramPatterns = CompareOnegramWithOtherGrams(UploadPath, DownloadPath)
    UploadPath = FOLDER_TO_PROCESS + '/1.1.1.1 Stage Gram per Description/'
    DownloadPath = REINFORCE_FOLDER + 'OneGram_Dictionary_Annotation/'
    try:
        os.makedirs(DownloadPath)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    DictionaryGeneration = GenerateDictionary(UploadPath, DownloadPath)


def CompareOnegramWithOtherGrams(Uploadpath, DownloadPath):
    InputFileFath = Uploadpath
    AnalyzePatternsComparisons(InputFileFath, DownloadPath)


def AnalyzePatternsComparisons(InputFilePath, DownloadPath,
                               RejectionThreshold=20):
    outputFilePath = DownloadPath
    OneGramFile=[]
    TwoGramFile=[]
    ThreeGramFile=[]
    FourGramFile=[]
    for root, dirs, ListofFiles in os.walk(InputFilePath):
        for FileName in ListofFiles:
            if FileName.endswith('_'+'1'+'.'+'csv'):
                if FileName not in OneGramFile:
                    OneGramFile.append(FileName)
            if FileName.endswith('_' + '2'+'.'+'csv'):
                if FileName not in OneGramFile:
                    TwoGramFile.append(FileName)
            if FileName.endswith('_' + '3' +'.'+'csv'):
                if FileName not in OneGramFile:
                    ThreeGramFile.append(FileName)
            if FileName.endswith('_' + '4' +'.'+'csv'):
                if FileName not in OneGramFile:
                    FourGramFile.append(FileName)
    for FileIndex in range(0,len(OneGramFile)):
        OneGram = PythonPandas.read_csv(InputFilePath + OneGramFile[FileIndex], sep=',', engine='python')
        TwoGram = PythonPandas.read_csv(InputFilePath + TwoGramFile[FileIndex], sep=',', engine='python')
        ThreeGram = PythonPandas.read_csv(InputFilePath + ThreeGramFile[FileIndex], sep=',', engine='python')
        FourGram = PythonPandas.read_csv(InputFilePath + FourGramFile[FileIndex], sep=',', engine='python')
        (RowCount, ColumnCount) = OneGram.shape
        if RowCount == 0: return 0
        OneGram = OneGram.groupby(OneGram.columns.tolist()).size().reset_index().rename(
            columns={0: 'Count_OneGram'})
        OneGram = OneGram.sort_values('Count_OneGram', ascending=False)
        OneGram = OneGram.rename(index=str, columns={"Grams": "OneGram", "Patterns": "Pattern_OneGram"})
        OneGram = OneGram[OneGram["Count_OneGram"] > RejectionThreshold]
        (RowCount, ColumnCount) = TwoGram.shape
        if RowCount == 0: return 0
        TwoGram = TwoGram.groupby(TwoGram.columns.tolist()).size().reset_index().rename(
            columns={0: 'Count_TwoGram'})
        TwoGram = TwoGram.sort_values('Count_TwoGram', ascending=False)
        TwoGram = TwoGram.rename(index=str, columns={"Grams": "TwoGram", "Patterns": "Pattern_TwoGram"})
        TwoGram = TwoGram[TwoGram["Count_TwoGram"] > RejectionThreshold]
        rejectedData = TwoGram[TwoGram['TwoGram'].str.count('_') >= 2]
        TwoGram = TwoGram[TwoGram['TwoGram'].str.count('_') == 1]
        TwoGram[['FirstGram', 'SecondGram']] = TwoGram.TwoGram.str.split('_', expand=True)
        TwoGramOnPrefix = PythonPandas.merge(OneGram, TwoGram, left_on='OneGram', right_on='FirstGram')
        TwoGramOnPrefix['GramVariantType'] = 'P_2Gram'
        TwoGramOnSufix = PythonPandas.merge(OneGram, TwoGram, left_on='OneGram', right_on='SecondGram')
        TwoGramOnSufix['GramVariantType'] = 'S_2Gram'
        TwoGramOnSufix = TwoGramOnSufix.sort_values('Count_TwoGram', ascending=False)
        TwoGramOnPrefix = TwoGramOnPrefix.sort_values('Count_TwoGram', ascending=False)
        TwoGramOnPrefix = TwoGramOnPrefix[['OneGram', 'Pattern_OneGram', 'Count_OneGram', 'TwoGram',
                                           'Pattern_TwoGram', 'Count_TwoGram',
                                           'GramVariantType']]
        TwoGramOnSufix = TwoGramOnSufix[['OneGram', 'Pattern_OneGram', 'Count_OneGram', 'TwoGram',
                                         'Pattern_TwoGram', 'Count_TwoGram',
                                         'GramVariantType']]
        TwoGramOnPrefix.to_csv(outputFilePath +str(TwoGramFile[FileIndex]).split(".")[0]+  '_Two_Gram_On_Prefix'+'.'+'csv', index=False)
        TwoGramOnSufix.to_csv(outputFilePath +str(TwoGramFile[FileIndex]).split(".")[0] +'_Two_Gram_On_Sufix'+'.'+'csv', index=False)
        rejectedData.to_csv(outputFilePath + str(TwoGramFile[FileIndex]).split(".")[0]+'_Rejected_2Grams_Data'+'.'+'csv', index=False)
        (RowCount, ColumnCount) = ThreeGram.shape
        if RowCount == 0: return 0
        ThreeGram = ThreeGram.groupby(ThreeGram.columns.tolist()).size().reset_index().rename(
            columns={0: 'Count_ThreeGram'})
        ThreeGram = ThreeGram.sort_values('Count_ThreeGram', ascending=False)
        ThreeGram = ThreeGram.rename(index=str,
                                     columns={"Grams": "ThreeGram", "Patterns": "Pattern_ThreeGram"})
        ThreeGram = ThreeGram[ThreeGram["Count_ThreeGram"] > RejectionThreshold]
        rejectedData = ThreeGram[ThreeGram['ThreeGram'].str.count('_') >= 3]
        ThreeGram = ThreeGram[ThreeGram['ThreeGram'].str.count('_') == 2]
        ThreeGram[['FirstGram', 'SecondGram', 'ThirdGram']] = ThreeGram.ThreeGram.str.split('_',
                                                                                            expand=True)
        ThreeGramOnPrefix = PythonPandas.merge(OneGram, ThreeGram, left_on='OneGram', right_on='FirstGram')
        ThreeGramOnPrefix['GramVariantType'] = 'P_3Gram'
        ThreeGramOnMid = PythonPandas.merge(OneGram, ThreeGram, left_on='OneGram', right_on='SecondGram')
        ThreeGramOnMid['GramVariantType'] = 'M_3Gram'
        ThreeGramOnSufix = PythonPandas.merge(OneGram, ThreeGram, left_on='OneGram', right_on='ThirdGram')
        ThreeGramOnSufix['GramVariantType'] = 'S_3Gram'
        ThreeGramOnSufix = ThreeGramOnSufix.sort_values('Count_ThreeGram', ascending=False)
        ThreeGramOnMid = ThreeGramOnMid.sort_values('Count_ThreeGram', ascending=False)
        ThreeGramOnPrefix = ThreeGramOnPrefix.sort_values('Count_ThreeGram', ascending=False)
        ThreeGramOnPrefix = ThreeGramOnPrefix[
            ['OneGram', 'Pattern_OneGram', 'Count_OneGram', 'ThreeGram',
             'Pattern_ThreeGram', 'Count_ThreeGram',
             'GramVariantType']]
        ThreeGramOnSufix = ThreeGramOnSufix[['OneGram', 'Pattern_OneGram', 'Count_OneGram', 'ThreeGram',
                                             'Pattern_ThreeGram', 'Count_ThreeGram',
                                             'GramVariantType']]
        ThreeGramOnMid = ThreeGramOnMid[['OneGram', 'Pattern_OneGram', 'Count_OneGram', 'ThreeGram',
                                         'Pattern_ThreeGram', 'Count_ThreeGram',
                                         'GramVariantType']]
        ThreeGramOnPrefix.to_csv(outputFilePath +str(ThreeGramFile[FileIndex]).split(".")[0]  +'Three_Gram_On_Prefix'+'.'+'csv', index=False)
        ThreeGramOnMid.to_csv(outputFilePath + str(ThreeGramFile[FileIndex]).split(".")[0] +'Three_Gram_On_Mid'+'.'+'csv', index=False)
        ThreeGramOnSufix.to_csv(outputFilePath +str(ThreeGramFile[FileIndex]).split(".")[0] + 'Three_Gram_On_Sufix'+'.'+'csv', index=False)
        rejectedData.to_csv(outputFilePath +str(ThreeGramFile[FileIndex]).split(".")[0] + 'Rejected_3Grams_Data'+'.'+'csv', index=False)
        (RowCount, ColumnCount) = FourGram.shape
        if RowCount == 0: return 0
        FourGram = FourGram.groupby(FourGram.columns.tolist()).size().reset_index().rename(
            columns={0: 'Count_FourGram'})
        FourGram = FourGram.sort_values('Count_FourGram', ascending=False)
        FourGram = FourGram.rename(index=str,
                                   columns={"Grams": "FourGram", "Patterns": "Pattern_FourGram"})
        FourGram = FourGram[FourGram["Count_FourGram"] > RejectionThreshold]
        # Check Acceptable and rejected Data
        rejectedData = FourGram[FourGram['FourGram'].str.count('_') >= 4]
        FourGram = FourGram[FourGram['FourGram'].str.count('_') == 3]

        FourGram[['FirstGram', 'SecondGram', 'ThirdGram', 'FourthGram']] = FourGram.FourGram.str.split('_', expand=True)
        FourGramOnPrefix = PythonPandas.merge(OneGram, FourGram, left_on='OneGram', right_on='FirstGram')
        FourGramOnPrefix['GramVariantType'] = 'P_4Gram'
        FourGramOnMid1 = PythonPandas.merge(OneGram, FourGram, left_on='OneGram', right_on='SecondGram')
        FourGramOnMid1['GramVariantType'] = 'M1_4Gram'
        FourGramOnMid2 = PythonPandas.merge(OneGram, FourGram, left_on='OneGram', right_on='ThirdGram')
        FourGramOnMid2['GramVariantType'] = 'M2_4Gram'
        FourGramOnSufix = PythonPandas.merge(OneGram, FourGram, left_on='OneGram', right_on='FourthGram')
        FourGramOnSufix['GramVariantType'] = 'S_4Gram'
        FourGramOnSufix = FourGramOnSufix.sort_values('Count_FourGram', ascending=False)
        FourGramOnMid1 = FourGramOnMid1.sort_values('Count_FourGram', ascending=False)
        FourGramOnMid2 = FourGramOnMid2.sort_values('Count_FourGram', ascending=False)
        FourGramOnPrefix = FourGramOnPrefix.sort_values('Count_FourGram', ascending=False)
        FourGramOnPrefix = FourGramOnPrefix[['OneGram', 'Pattern_OneGram', 'Count_OneGram', 'FourGram',
                                             'Pattern_FourGram', 'Count_FourGram',
                                             'GramVariantType']]

        FourGramOnSufix = FourGramOnSufix[['OneGram', 'Pattern_OneGram', 'Count_OneGram', 'FourGram',
                                           'Pattern_FourGram', 'Count_FourGram',
                                           'GramVariantType']]
        FourGramOnMid1 = FourGramOnMid1[['OneGram', 'Pattern_OneGram', 'Count_OneGram', 'FourGram',
                                         'Pattern_FourGram', 'Count_FourGram',
                                         'GramVariantType']]
        FourGramOnMid2 = FourGramOnMid2[['OneGram', 'Pattern_OneGram', 'Count_OneGram', 'FourGram',
                                         'Pattern_FourGram', 'Count_FourGram',
                                         'GramVariantType']]
        FourGramOnPrefix.to_csv(outputFilePath +str(FourGramFile[FileIndex]).split(".")[0]+ '_Four_Gram_On_Prefix'+'.'+'csv', index=False)
        FourGramOnMid1.to_csv(outputFilePath +str(FourGramFile[FileIndex]).split(".")[0]+'_Four_Gram_On_Mid1'+'.'+'csv', index=False)
        FourGramOnMid2.to_csv(outputFilePath +str(FourGramFile[FileIndex]).split(".")[0]+'_Four_Gram_On_Mid2'+'.'+'csv', index=False)
        FourGramOnSufix.to_csv(outputFilePath +str(FourGramFile[FileIndex]).split(".")[0]+ '_Four_Gram_On_Sufix'+'.'+'csv', index=False)
        rejectedData.to_csv(outputFilePath + str(FourGramFile[FileIndex]).split(".")[0]+'_Rejected_4Grams_Data'+'.'+'csv', index=False)


def GetLemmaDefinitions(WordTokens):
    BlobText = TextBlob(WordTokens)
    WordsFromBlobs = BlobText.words
    for Words in WordsFromBlobs:
        DictionaryValue = Words.definitions[:1]
        if len(DictionaryValue) > 0:
            return ' '.join(DictionaryValue)
def GetWordVariations(WordTokens):
    BlobText = TextBlob(WordTokens)
    WordsFromBlobs = BlobText.words
    for Words in WordsFromBlobs:
        try:
            DictionaryValue = [Words.stem(Words.PorterStemmer),Words.synsets[0].lemma_names(),Words.pluralize(),Words.singularize(),Words.pos_tag]
        except:
            DictionaryValue = ''
        if len(DictionaryValue) > 0:
            return DictionaryValue


def GenerateDictionary(Uploadpath, DownloadPath):
    FileNameAppender = []
    for root, dirs, files in os.walk(Uploadpath):
        for name in files:
            for x in range(1, 2):
                if (name.endswith('_' + str(x) +'.'+'csv')):
                    if name not in FileNameAppender:
                        FileNameAppender.append(name)

    for FileNames in FileNameAppender:
        FirstpartOfFile = str(FileNames).split('_',maxsplit=1)[0]
        SecondPartOfFile=str(FileNames).split('_',maxsplit=1)[1]
        GenerateFileName = FirstpartOfFile + '_' + SecondPartOfFile
        OneGram = PythonPandas.DataFrame(PythonPandas.read_csv(Uploadpath + GenerateFileName, sep=',', engine='python'))
        (RowNumber, ColumnNumber) = OneGram.shape
        if RowNumber == 0: return 0
        WordListAppender = []
        for RowNumbers, WordValues in OneGram['Grams'].iteritems():
            CleanedValues = str(WordValues).strip(' ').lstrip('_').rstrip('_').strip('_').strip('-').split(' ')
            for UniqueGrams in CleanedValues:
                UniqueGrams=UniqueGrams.lower()
                if UniqueGrams not in WordListAppender:
                    WordListAppender.append(UniqueGrams)
        GramDataFrame = PythonPandas.DataFrame(PythonPandas.Series(WordListAppender), columns=['Grams'])
        OneGram['Dictionary'] = GramDataFrame['Grams'].apply(GetLemmaDefinitions)
        OneGram = OneGram[PythonPandas.notnull(OneGram['Dictionary'])]
        GramDataFrame = GramDataFrame.join(OneGram['Dictionary'], how='left')
        GramDataFrame = GramDataFrame[PythonPandas.notnull(GramDataFrame['Dictionary'])]
        GramDataFrame['Word_Variations'] = GramDataFrame['Grams'].apply(GetWordVariations)

        GramDataFrame.to_csv(DownloadPath + 'Dictionary_' + GenerateFileName, index=False)