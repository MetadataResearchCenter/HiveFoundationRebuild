from whoosh.fields import Schema
from whoosh.fields import ID, TEXT
from whoosh.index import open_dir, create_in
from whoosh.analysis import StopFilter
from whoosh.analysis import RegexTokenizer
from whoosh.analysis import LowercaseFilter
from collections import Counter


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
tokenList = [t.text for t in tokenizer(io.open('sample/material1.txt', encoding='utf-8'))]



print Counter(tokenList)
