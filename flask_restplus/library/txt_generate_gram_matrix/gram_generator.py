import csv
import re
import pandas as PythonPandas
import os
from utils.gram_generator_variables import *

def ReadGramPatternFilePaths(DataFileName, TextsToAppend):
    ChosenColumn = TextsToAppend
    CleanedDataGrams = FOLDER_TO_PROCESS + '/1.1.1.1 Stage Gram per Description/'
    CleanedGramPatterns = FOLDER_TO_PROCESS + '/1.1.1.2 Description Gram With Patterns/'
    GramWithStopWords = FOLDER_TO_PROCESS + '/1.2.1.1 Stage Gram per Description/'
    GramPatternsWithStopWords = FOLDER_TO_PROCESS + '/1.2.1.2 Description Gram With Patterns/'
    GramLists = [GramWithStopWords]
    PatternLists = [GramPatternsWithStopWords]
    for FileNumber in range(1, 7):
        GramFiles = ChosenColumn + '_' + DataFileName + '_Grams_' + str(FileNumber)
        GramLists.append(GramFiles)
        PatternFiles = ChosenColumn + '_' + DataFileName + '_Patterns_' + str(FileNumber)
        PatternLists.append(PatternFiles)
    CleanedGramsList = [CleanedDataGrams]
    CleanedPatternsList = [CleanedGramPatterns]
    for FileNumber in range(1, 7):
        GramFiles = ChosenColumn + '_' + DataFileName + '_Grams_' + str(FileNumber)
        CleanedGramsList.append(GramFiles)
        PatternFiles = ChosenColumn + '_' + DataFileName + '_Patterns_' + str(FileNumber)
        CleanedPatternsList.append(PatternFiles)
    PathToDictionary = DICT_FOLDER
    PathToCorrelationData = CORREL_FOLDER
    DictionaryList = [PathToDictionary]
    CorrelationDataList = [PathToCorrelationData]
    for root, dirs, files in os.walk(PathToDictionary):
        for name in files:
            if (name.endswith('.' + 'csv')):
                if name not in DictionaryList:
                    DictionaryList.append(name)
    for root, dirs, files in os.walk(PathToCorrelationData):
        for name in files:
            if (name.endswith('.' + 'csv')):
                if name not in CorrelationDataList:
                    CorrelationDataList.append(name)

    FinalList = [CleanedGramsList, CleanedPatternsList, GramLists, PatternLists,DictionaryList,CorrelationDataList]
    return FinalList

def GeneratePatternsFromGrams(InputFilePath, OutputFilePath):
    OpenCSVInputFile = open(InputFilePath, 'r')
    ReadCSVInputFile = csv.reader(OpenCSVInputFile, delimiter=',')
    OpenCSVOutputFile = open(OutputFilePath, 'w', newline='\n')
    CreateCSVWriter = csv.writer(OpenCSVOutputFile, delimiter=',', lineterminator='\n')
    CreateCSVWriter.writerow(['Grams', 'Patterns'])
    next(ReadCSVInputFile, None)
    for EveryRowData in ReadCSVInputFile:
        if len(EveryRowData) > 0:
            if not EveryRowData: continue
            MyRow=str(EveryRowData[1]).strip(' ')
            #MyRow=MyRow.strip(r'[\s\/\W+\D+\w{1}\w{2}\w{3}\_\-]')
            Numbers = re.sub(r'[0-9]', r'9', MyRow)
            Lowercase = re.sub(r'[a-z]', r'x', Numbers)
            UpperCase = re.sub(r'[A-Z]', r'X', Lowercase)
            Symbols=re.sub('[^9xX ]', '#', UpperCase)
            #Spaces = re.sub('[9xX ]'+' '+'[9xX ]', '[9xX ]'+'_'+'[9xX ]', Symbols)
            Spaces = re.sub(' ',  '_' , Symbols)
            RegularExpression = Spaces
            #if RegularExpression.startswith(r'[^_]'):
                #break
            #else:
                #pass
            GramData=str(EveryRowData[1])
            if GramData.__contains__('%'):
                RegularExpression=''.join(RegularExpression).replace('#', '%', 1)
                JoinKeyValuePairs = [GramData, RegularExpression]

                CreateCSVWriter.writerow(JoinKeyValuePairs)
            else:
                JoinKeyValuePairs = [GramData, RegularExpression]
                CreateCSVWriter.writerow(JoinKeyValuePairs)




    OpenCSVInputFile.close()
    OpenCSVOutputFile.close()

def PatternGenerator(Uploadpath, DownloadPath, DataFileName, TextsToAppend):
    for PatternCount in range(1, 7):
        InputFile = Uploadpath + TextsToAppend + '_' + DataFileName + '_Grams_' + str(PatternCount) + '.' + 'csv'
        OutputFile = DownloadPath + TextsToAppend + '_' + DataFileName + '_Patterns_' + str(PatternCount) + '.' + 'csv'
        GeneratePatternsFromGrams(InputFile, OutputFile)

def NGramsGenerator(InputData, NumberPfGramsToProduce):
    InputData = InputData.split(' ')
    OutputGramsAppender = []
    for NumberOfGrams in range(len(InputData) - NumberPfGramsToProduce + 1):
        FinalGram = InputData[NumberOfGrams:NumberOfGrams + NumberPfGramsToProduce]
        OutputGramsAppender.append(FinalGram)
    return OutputGramsAppender

def GramFarmGenerator(InputFilePath, OutputFilePath, NumberOfGrams, KeysToAppend):

    OpenCSVInput = open(InputFilePath, 'r')
    ReadCSVInput = csv.reader(OpenCSVInput, delimiter=',')

    Headers = next(ReadCSVInput, None)
    OutputFilePath = OutputFilePath.replace('_Grams', '_Grams_' + str(NumberOfGrams))
    OpenCSVOutput = open(OutputFilePath, 'w', newline='\n')
    CreateCSVWriter = csv.writer(OpenCSVOutput, delimiter=',', lineterminator='\n')
    CreateCSVWriter.writerow([KeysToAppend, 'Grams'])
    for DataRow in ReadCSVInput:
        for Grams in NGramsGenerator(DataRow[1], NumberOfGrams):

            if NumberOfGrams>1:
                RowGram = '_'.join(map(str, Grams))
                RowGram = RowGram.strip(r'\"|\'|\,\#|\&|\.|\-|\*')
            else:
                RowGram = ''.join(map(str, Grams))
                RowGram = RowGram.strip(r'\"|\'|\,\#|\&|\.|\-|\*')
            if RowGram:
                AppendKeyValuePairs = [DataRow[0], RowGram]
                CreateCSVWriter.writerow(AppendKeyValuePairs)
    OpenCSVInput.close()
    OpenCSVOutput.close()

def GenerateGrams(Uploadpath, DownloadPath, DataFileName, Keys, TextsToAppend):
    for GramsNumbers in range(1, 7):
        csvOutputFile = DownloadPath + TextsToAppend + '_' + DataFileName + '_Grams' + '.' + 'csv'
        GramFarmGenerator(Uploadpath + DataFileName + '_Cleaned.csv', csvOutputFile, GramsNumbers, Keys)

def GenerateDirtyGrams(Uploadpath, DownloadPath, DataFileName, Keys, TextsToAppend):
    for GramsNumbers in range(1, 7):
        csvOutputFile = DownloadPath + TextsToAppend + '_' + DataFileName + '_Grams' + '.' + 'csv'
        GramFarmGenerator(DataFileName + '.csv', csvOutputFile, GramsNumbers, Keys)

def KeysColumnsBreaker(Uploadpath, DownloadPath, DataFileName, Keys, TextsToAppend):


    DataToSplit = PythonPandas.DataFrame(PythonPandas.read_excel(Uploadpath + DataFileName + '.' + 'csv'))
    print(DataToSplit)
    DataToSplit = PythonPandas.DataFrame(DataToSplit.astype(str))
    DataToSplit = PythonPandas.DataFrame(BreakColumns(DownloadPath, DataFileName, DataToSplit, Keys, TextsToAppend))
    return DataToSplit

def BreakColumns(DownloadPath, DataFileName, PandasDataFrame, KeyNumbers, TextsToAppend):
    SplittedDataFrame = PythonPandas.DataFrame(PandasDataFrame[[KeyNumbers, TextsToAppend]].copy())
    SplittedDataFrame.replace('nan', value='', inplace=True)
    SplittedDataFrame.to_excel(DownloadPath + TextsToAppend + '_' + DataFileName + '.' + '.xlsx')
    return PandasDataFrame





