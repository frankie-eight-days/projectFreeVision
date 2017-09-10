import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google import google

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

def main():
    conservativeSearchKey = []
    liberalSearchKey = []
    matchingIndicesList = []

    conservativeSearchKey = fillSearchTerms('right')
    liberalSearchKey = fillSearchTerms('left')

    matchingIndicesList = matchSearches(conservativeSearchKey, liberalSearchKey)

    doSearches(conservativeSearchKey, liberalSearchKey, matchingIndicesList)

def doSearches(conservativeSearch, liberalSearch, indicesList):
    worksheet = client.open_by_key('1DTDmpP9dlUfZhfm8Bb4AL7-PfqlbjoCEI0FxUFGfjA0')
    wks = worksheet.worksheet('Sheet3')
    rowNumber = 382 - 4

    for i in range(75, len(indicesList)):

        wks.update_cell(i + 1 + rowNumber, 1, conservativeSearch[indicesList[i][0]])
        wks.update_cell(i + 1 + rowNumber, 4, liberalSearch[indicesList[i][1]])

        cSearchResults = google.search(conservativeSearch[indicesList[i][0]])
        lSearchResults = google.search(liberalSearch[indicesList[i][1]])

        for result in range(4):
            wks.update_cell(i+1+rowNumber, 2, cSearchResults[result].name)
            wks.update_cell(i + 1 + rowNumber, 5, lSearchResults[result].name)
            rowNumber += 1
        print(i)


def matchSearches(conservativeKeyList, liberalKeyList):
    keyWordsC = []
    keyWordsL = []

    matchingIndices = []

    for i in range(len(conservativeKeyList)):
        keyWordsC.append(conservativeKeyList[i].split())
    for i in range(len(liberalKeyList)):
        keyWordsL.append(liberalKeyList[i].split())

    for cHeadIndex in range(len(keyWordsC)):
        for cWordIndex in range(len(keyWordsC[cHeadIndex])):
            for lHeadIndex in range(len(keyWordsL)):
                for lWordIndex in range(len(keyWordsL[lHeadIndex])):
                    if keyWordsC[cHeadIndex][cWordIndex] == keyWordsL[lHeadIndex][lWordIndex]:
                        matchingIndices.append([cHeadIndex, lHeadIndex])
    return matchingIndices

def fillSearchTerms(wing):
    sheet = client.open('googleSearchTerms').sheet1
    if wing == 'right':
        return sheet.col_values(1)
    else:
        return sheet.col_values(3)

main()