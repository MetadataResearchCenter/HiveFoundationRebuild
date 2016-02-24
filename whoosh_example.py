from whoosh.fields import Schema
from whoosh.fields import ID, TEXT
from whoosh.index import open_dir, create_in
from whoosh.qparser import QueryParser
from whoosh.analysis import RegexTokenizer
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

#=============Searcher===========

searcher = index.searcher()

print list(searcher.lexicon("text"))

qp = QueryParser("text", schema = my_schema)
q = qp.parse(u"In addition, the substantial shift")

with index.searcher() as s:
    results = s.search(q, terms = True)

found = results.scored_length()
#
# if results.has_matched_terms():
#     # What terms matched in the results?
#     print(results.matched_terms())
#
#     # What terms matched in each hit?
#     for hit in results:
#         print(hit.matched_terms())
#
# if results.has_exact_length():
#     print("Scored", found, "of exactly", len(results), "documents")
# else:
#     low = results.estimated_min_length()
#     high = results.estimated_length()
#
#     print("Scored", found, "of between", low, "and", high, "documents")

#=============Analyzer===========

tokenizer = RegexTokenizer()
tokenList = []
for token in tokenizer(io.open('sample/material1.txt', encoding='utf-8').read()):
    tokenList.append(token.text)
print Counter(tokenList)
