import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google import google

# Setting up and authorizing the backend with Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

def main():
    # Gets the string of buzzwords from Google Sheets
    conservativeSearchKey = fillSearchTerms('right')
    liberalSearchKey = fillSearchTerms('left')

    # Creates list of indices where topics of headlines match
    matchingIndicesList = matchSearches(conservativeSearchKey, liberalSearchKey)

    # Then does the searches and updates the second sheet of the workbook
    doSearches(conservativeSearchKey, liberalSearchKey, matchingIndicesList)

def doSearches(conservativeSearch, liberalSearch, indicesList):
    # Open workbook and create worksheet (wks) object
    worksheet = client.open_by_key('1DTDmpP9dlUfZhfm8Bb4AL7-PfqlbjoCEI0FxUFGfjA0')
    wks = worksheet.worksheet('Sheet3')

    # Starts from one since there is no 0 cell or column in sheets
    rowNumber = 1

    for i in range(len(indicesList)):
        # Creates cells containing buzzwords that will be searched
        wks.update_cell(i + 1 + rowNumber, 1, conservativeSearch[indicesList[i][0]])
        wks.update_cell(i + 1 + rowNumber, 4, liberalSearch[indicesList[i][1]])

        # Searches google for the buzzwords
        # CAUTION: if more than 45 searches are conducted, your IP will be temp banned from Google
        cSearchResults = google.search(conservativeSearch[indicesList[i][0]])
        lSearchResults = google.search(liberalSearch[indicesList[i][1]])

        # Prints results from each search into it's appropriate cell
        for result in range(4):
            wks.update_cell(i+1+rowNumber, 2, cSearchResults[result].name)
            wks.update_cell(i + 1 + rowNumber, 5, lSearchResults[result].name)
            rowNumber += 1
        print(i)


def matchSearches(conservativeKeyList, liberalKeyList):
    # Lists where key words and matching indices will be held
    keyWordsC = []
    keyWordsL = []
    matchingIndices = []

    # Buzzword strings are broken back into words
    for i in range(len(conservativeKeyList)):
        keyWordsC.append(conservativeKeyList[i].split())
    for i in range(len(liberalKeyList)):
        keyWordsL.append(liberalKeyList[i].split())

    # Searches through the conservative list looking for words that match in the liberal list
    for cHeadIndex in range(len(keyWordsC)):
        for cWordIndex in range(len(keyWordsC[cHeadIndex])):
            for lHeadIndex in range(len(keyWordsL)):
                for lWordIndex in range(len(keyWordsL[lHeadIndex])):
                    # If one word matches, the string index is matched and stored
                    if keyWordsC[cHeadIndex][cWordIndex] == keyWordsL[lHeadIndex][lWordIndex]:
                        matchingIndices.append([cHeadIndex, lHeadIndex])
    return matchingIndices

# Grabs the buzzwords from the first sheet
def fillSearchTerms(wing):
    sheet = client.open('googleSearchTerms').sheet1
    if wing == 'right':
        return sheet.col_values(1)
    else:
        return sheet.col_values(3)

main()