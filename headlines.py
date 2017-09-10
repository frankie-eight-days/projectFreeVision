from xml.etree import ElementTree
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

def main():
    conservativeCol = 1
    liberalCol = 3

    headlines = []

    conservativeNewsUrls = ['http://feeds.foxnews.com/foxnews/politics',
                            'http://feeds.feedburner.com/breitbart',
                            'https://www.infowars.com/feed/custom_feed_rss']

    liberalNewsUrls = ['https://www.buzzfeed.com/politics.xml',
                       'http://rss.nytimes.com/services/xml/rss/nyt/Politics.xml',
                       'http://www.huffingtonpost.com/section/politics/feed',
                       'http://rss.cnn.com/rss/edition_us.rss',
                       'https://rss.msn.com/en-ca/']

    for i in range(len(conservativeNewsUrls)):
        headlines = []
        getNews(conservativeNewsUrls[i], headlines)
        keyWords = findKeyWords(headlines)
        sheetAddKeyWords(keyWords, conservativeCol)

    for i in range(len(liberalNewsUrls)):
        headlines = []
        getNews(liberalNewsUrls[i], headlines)
        keyWords = findKeyWords(headlines)
        sheetAddKeyWords(keyWords, liberalCol)

def sheetAddKeyWords(keyWords, colNumber):
    sheet = client.open('googleSearchTerms').sheet1
    allDataCells = sheet.col_values(colNumber)
    rowCount = 0
    for i in range(len(allDataCells)):
        if not allDataCells[i] == '':
            rowCount += 1

    for words in range(len(keyWords)):
        sheet.update_cell(words+1+rowCount, colNumber, keyWords[words])

def findKeyWords(newsHeadlines):
    keyWords = []
    keyWordStrings = []
    numberOfHeadlines = 0

    for i in range(len(newsHeadlines)):
        words = newsHeadlines[i].split()
        for word in range(len(words)):
            if len(words[word]) > 5:
                keyWords.append(words[word])
        keyWords.append('.')
        numberOfHeadlines += 1

        currentHeadline = ''

    for i in range(len(keyWords)):
         if not keyWords[i] == '.':
            currentHeadline += keyWords[i]
            currentHeadline += ' '
         else:
            keyWordStrings.append(currentHeadline)
            currentHeadline = ''

    return keyWordStrings


def getNews(url, arrayOfNews):
    response = requests.get(url)
    stringData = response.text
    tree = ElementTree.fromstring(stringData)

    for child in tree:
        for doubleChild in child:
            if doubleChild.tag == 'item':
                for tripleChild in doubleChild:
                    if tripleChild.tag == 'title':
                        arrayOfNews.append(tripleChild.text)

main()