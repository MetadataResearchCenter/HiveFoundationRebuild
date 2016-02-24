from whoosh.fields import Schema
from whoosh.fields import ID, TEXT
from whoosh.index import open_dir, create_in
from whoosh.analysis import StopFilter
from whoosh.analysis import RegexTokenizer
from collections import Counter
import pprint


#=============Input===========
# location = input('Enter the file name: ')
# print location

#=============Index===========
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
                    path = u'sample/material1.txt',
                    source = u'material1.txt',
                    title = u'Voltage Scaling of Graphene Device on SrTiO3 Epitaxial Thin Film',
                    text = io.open('sample/material1.txt', encoding='utf-8').read())
writer.commit()

#=============Analyzer===========

tokenizer = RegexTokenizer()
tokenList = []
stopper = StopFilter()

for token in tokenizer(io.open('sample/material1.txt', encoding='utf-8').read()):

    tokenList.append(token.text)

for word in tokenList:
    print (word)
    print tokenList[]




