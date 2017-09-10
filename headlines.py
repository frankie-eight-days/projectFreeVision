from xml.etree import ElementTree
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Setting up and authorizing the backend with Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

def main():
    # Columns where information is stored on sheet one
    conservativeCol = 1
    liberalCol = 3

    conservativeNewsUrls = ['http://feeds.foxnews.com/foxnews/politics',
                            'http://feeds.feedburner.com/breitbart',
                            'https://www.infowars.com/feed/custom_feed_rss']

    liberalNewsUrls = ['https://www.buzzfeed.com/politics.xml',
                       'http://rss.nytimes.com/services/xml/rss/nyt/Politics.xml',
                       'http://www.huffingtonpost.com/section/politics/feed',
                       'http://rss.cnn.com/rss/edition_us.rss',
                       'https://rss.msn.com/en-ca/']

    for i in range(len(conservativeNewsUrls)):
        headlines = []                              # Clears headlines list
        getNews(conservativeNewsUrls[i], headlines) # Gets the headlines from RSS feeds and stores in list
        keyWords = findKeyWords(headlines)          # Extracts the buzzwords from the headlines
        sheetAddKeyWords(keyWords, conservativeCol) # Then adds them on the first sheet column 1

    for i in range(len(liberalNewsUrls)):
        headlines = []                              # Clears headlines list
        getNews(liberalNewsUrls[i], headlines)      # Gets headlines from RSS feeds and stores in list
        keyWords = findKeyWords(headlines)          # Extracts the buzzwords from the headlines
        sheetAddKeyWords(keyWords, liberalCol)      # Then adds them on the first sheet column 3

def sheetAddKeyWords(keyWords, colNumber):
    sheet = client.open('googleSearchTerms').sheet1 # Creates sheet object
    allDataCells = sheet.col_values(colNumber)      # Grabs all the data in the passed in column
    rowCount = 0
    for i in range(len(allDataCells)):     # Loops through all the headlines
        if not allDataCells[i] == '':      # Ignores blank cells
            rowCount += 1                  # Counts upto where the blank cells begin

    for words in range(len(keyWords)):     # Updates the cells after preexisting cells
        sheet.update_cell(words+1+rowCount, colNumber, keyWords[words])

def findKeyWords(newsHeadlines):
    keyWords = []
    keyWordStrings = []
    numberOfHeadlines = 0

    for i in range(len(newsHeadlines)):
        words = newsHeadlines[i].split()        # Each headline gets split into words (now have 2d list)
        for word in range(len(words)):          # Loops through each word in headline
            if len(words[word]) > 5:
                keyWords.append(words[word])    # Word is added to master list of buzzwords
        keyWords.append('.')                    # Period differentiates what keyword belongs to what headline
        numberOfHeadlines += 1

        currentHeadline = ''

    for i in range(len(keyWords)):                  # Loops through all the words now
         if not keyWords[i] == '.':                 # Checks to see if words belong together
            currentHeadline += keyWords[i]          # If they do, they get added to a temporary str
            currentHeadline += ' '
         else:
            keyWordStrings.append(currentHeadline)  # When a period is found, the str gets appended to master list
            currentHeadline = ''

    return keyWordStrings


def getNews(url, arrayOfNews):
    # Gets the raw data from website
    response = requests.get(url)

    # Converts the raw data to string, then ElementTree is used to find the elements
    stringData = response.text
    tree = ElementTree.fromstring(stringData)

    # All RSS feeds follow the same path to get to headlines
    # There are three layers that must be penetrated, the path will always be: 'rss/channel/item'
    # Hence the three nested for loops below
    # First for loop opens the rss element
    for child in tree:
        # Second loop opens the channel element
        for doubleChild in child:
            # Inside channel element there ~10 elements describing the feed
            # If statement is used to filter them (Something more elegant could probably be done with ET)
            if doubleChild.tag == 'item':
                # Third for loop filters through the elements in each article for the headline
                for tripleChild in doubleChild:
                    if tripleChild.tag == 'title':
                        # Finally the headline is appended to it's array
                        arrayOfNews.append(tripleChild.text)

main()