from library.txt_striphtml.html_stripper import getStrippedHtml



def removeNoiseCharacters(content):
	content = content.replace(',','')
	return content


	
def NGramsGenerator(inputData, numberOfGramsToProduce):
    inputData = inputData.split(' ')
    OutputGramsAppender = []
    for NumberOfGrams in range(len(inputData) - numberOfGramsToProduce + 1):
        FinalGram = inputData[NumberOfGrams:NumberOfGrams + numberOfGramsToProduce]
        OutputGramsAppender.append(FinalGram)
    return OutputGramsAppender



def generateNGram(numberOfGrams, htmlContent):
	strippedHtmlContent = getStrippedHtml(htmlContent)
	strippedHtmlContent = removeNoiseCharacters(strippedHtmlContent)
	ngramList = []
	for Grams in NGramsGenerator(strippedHtmlContent,numberOfGrams):
		if numberOfGrams>1:
		    RowGram = '_'.join(map(str, Grams))
		    RowGram = RowGram.strip(r'\"|\'|\,\#|\&|\.|\-|\*')
		else:
		    RowGram = ''.join(map(str, Grams))
		    RowGram = RowGram.strip(r'\"|\'|\,\#|\&|\.|\-|\*')
		if RowGram:
		    ngramList.append(RowGram)
	return ngramList