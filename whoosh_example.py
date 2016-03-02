from whoosh.fields import Schema
from whoosh.fields import ID, TEXT
from whoosh.index import open_dir, create_in
from whoosh.analysis import StopFilter
from whoosh.analysis import RegexTokenizer
from whoosh.qparser import QueryParser
from collections import Counter
# from nltk.corpus import stopwords


#=============Input===========


#=============Input Indexing===========
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
                    path = u'sample/uat_voc.txt',
                    source = u'uat_voc.txt',
                    title = u'uat_voc',
                    text = io.open('uat_voc.txt', encoding='utf-8').read())
writer.commit()

#=============Input Searcher===========

inputSearcher = index.searcher()

phrases = list(inputSearcher.lexicon("text"))

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
    searchReuslt = inputSearcher.search(query)
    print searchReuslt
    if len(searchReuslt) == 0:
        tokenList.remove(token)

print Counter(tokenList)





