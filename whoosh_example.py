from whoosh.fields import Schema
from whoosh.fields import ID, TEXT
from whoosh.index import open_dir, create_in
from whoosh.analysis import StopFilter
from whoosh.analysis import RegexTokenizer
from collections import Counter
from nltk.corpus import stopwords


#=============Input===========
# location = input('Enter the file name: ')
# print location

#=============UATIndex===========
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
writer.add_document(id = u'material1',
                    path = u'sample/astronomy\ article',
                    source = u'material1.txt',
                    title = u'Voltage Scaling of Graphene Device on SrTiO3 Epitaxial Thin Film',
                    text = io.open('sample/astronomyArticle.txt', encoding='utf-8').read())
writer.commit()

#=============UATSearcher===========
UATSearcher = index.searcher()




#=============StopWord===========

#=============Analyzer===========

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

print Counter(tokenList)





