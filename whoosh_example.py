from whoosh.fields import Schema
from whoosh.fields import ID, TEXT
from whoosh.index import open_dir, create_in
from whoosh.analysis import StopFilter
from whoosh.analysis import RegexTokenizer
from whoosh.qparser import QueryParser
from collections import Counter
import sqlite3
import os

#=============Database Connection===========
db = None

def dbConnect():
    global db
    try:
        dbName = "concepts.sqlite"
        if os.path.exists(dbName):
            db = sqlite3.connect(dbName)
            print "database connected"
        else:
            print ("Error:", dbName, "does not exits" )

    except sqlite3.IntegrityError as err:
        print('Integrity Error on connect:', err)
    except sqlite3.OperationalError as err:
        print('Operational Error in connect:', err)
    except sqlite3.Error as err:
        print('Error in connect:', err)

dbConnect()

#=============Retrieving Data from DB===========

def findConceptsLike():
    prefLabels = []

    sql = 'SELECT PrefLabel FROM CONCEPT'
    try:
        cursor = db.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        if len(rows) > 0:
            for r in rows:
                prefLabels.append(r[0])
        return prefLabels
    except sqlite3.IntegrityError as err:
        print('Integrity Error in getPrefLabelFor:', err)
    except sqlite3.OperationalError as err:
        print('Operational Error in getPrefLabelFor:', err)
    except sqlite3.Error as err:
        print('Error in getPrefLabelFor:', err)

UAT_words = unicode(findConceptsLike())

#=============UAT Indexing===========
my_schema = Schema(id = ID(unique=True, stored=True),
                   path = ID(stored=True),
                   source = ID(stored=True),
                   author = TEXT(stored=True),
                   title = TEXT(stored=True),
                   text = TEXT)


ix = create_in("index", my_schema)
index = open_dir("index")
writer = index.writer()

import io
writer.add_document(id = u'uat_voc',
                    path = u'HiveFoundationRebuild/concepts.sqlite',
                    source = u'concepts.sqlite',
                    title = u'uat_voc',
                    text = UAT_words)

writer.commit()
#=============UATSearcher===========

UATSearcher = index.searcher()

qp = QueryParser("text", schema=index.schema)

#=============StopWord===========

tokenizer = RegexTokenizer()
tokenList = []

stopWordsFile1 = open("stopwords (1).txt", "r")
stopWordsFile2 = open("stopwords_en.txt", "r")

stopwords1 = stopWordsFile1.read().splitlines()
stopwords2 = stopWordsFile2.read().splitlines()
stopwords = stopwords1 + stopwords2

stopper = StopFilter(stoplist = stopwords)

# try to make lowercasefilter works
for token in stopper(tokenizer(io.open('sample/astronomyArticle.txt', encoding='utf-8').read().lower())):
    tokenList.append(token.text)

#=============KeywordsMatch===========

for token in tokenList:
    query = qp.parse(token)
    searchReuslt = UATSearcher.search(query)
    if len(searchReuslt) == 0:
        tokenList = filter(lambda a: a != token, tokenList)

def counting(token):
    print Counter(token)

counting(tokenList)




