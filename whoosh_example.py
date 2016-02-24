from whoosh.fields import Schema
from whoosh.fields import ID, TEXT
from whoosh.index import open_dir, create_in
from whoosh.qparser import QueryParser
from whoosh import scoring
from whoosh.query import Term, And
from whoosh.analysis import RegexTokenizer
from whoosh import reading

#=============Index===========
my_schema = Schema(id = ID(unique=True, stored=True), 
                   path = ID(stored=True), 
                   source = ID(stored=True),
                   # author = TEXT(stored=True),
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

writer.add_document(id = u'material2',
                    path = u'sample/material2.txt',
                    source = u'material2.txt',
                    title = u'Eutectic Growth in Two-Phase Multicomponent Alloys',
                    text = io.open('sample/material2.txt', encoding='utf-8').read())

writer.add_document(id = u'material3',
                    path = u'sample/material3.txt',
                    source = u'material3.txt',
                    title = u'Short-range phase coherence and origin of the 1T-TiSe2 charge density wave',
                    text = io.open('sample/material3.txt', encoding='utf-8').read())
writer.commit()



#=============Query===========
# index = open_dir("index")
# reader = index.reader()
# print index
# searcher = index.searcher()
# query = And([Term("text", "particular"), Term("text", "multicomponent"), Term("text", "hypotheses")])
#
# results = searcher.search(query)
# print('# of hits:', len(results))
# print('Best Match:', results[0])

searcher = index.searcher(weighting=scoring.TF_IDF())

print list(searcher.lexicon("text"))

qp = QueryParser("text", schema = my_schema)
q = qp.parse(u"In addition, the substantial shift")

with index.searcher() as s:
    results = s.search(q)

found = results.scored_length()

if results.has_exact_length():
    print("Scored", found, "of exactly", len(results), "documents")
else:
    low = results.estimated_min_length()
    high = results.estimated_length()

    print("Scored", found, "of between", low, "and", high, "documents")