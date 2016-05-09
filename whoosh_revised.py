import os.path
import re
from nltk.corpus import stopwords
from whoosh.fields import Schema, TEXT, ID
from whoosh.index import create_in



#=============design schema===========
my_schema = Schema(id = ID(unique=True, stored=True),
                   path = ID(stored=True),
                   author = TEXT,
                   title = TEXT(stored=True),
                   content = TEXT(stored=True))

#=============create index and add document===========
def create_index(schema):
    if not os.path.exists("index"):
        mkdir("index")
    ix = create_in("index", schema=schema)
    return ix

def add_doc(index, doc_loc):
    writer = index.writer()
    fileobj = open(doc_loc, "rb")
    content = unicode(fileobj.read())
    fileobj.close()
    doc_loc = unicode(doc_loc)
    writer.add_document(title=u"Astronomy Article", path=doc_loc, content=content)
    writer.commit()

#=============getting all the stop words (unused)===========
# def get_stop_word():
#     stop_words = []
#
#     with open('stopwords_1.txt','r') as f1:
#         for line in f1:
#             for word in line.split():
#                stop_words.append(word)
#
#     with open('stopwords_2.txt','r') as f2:
#         for line in f2:
#             for word in line.split():
#                stop_words.append(word)
#
#     return stop_words

#=============searching and filtering stop words===========
def searcher(index):
    try:
        searcher = index.searcher()
        word_list = list(searcher.lexicon("content"))
        return word_list
    finally:
        searcher.close()

def filter(word_list):
    filtered_list = filter(lambda x: x not in stopwords.words('english'), word_list)
    return filtered_list


if __name__ == "__main__":
    index = create_index(my_schema)
    add_doc(index, "/Users/Robert/Desktop/HiveFoundationRebuild/sample/astronomyArticle.txt")
    word_list = searcher(index)
    filtered_content = filter(word_list)
    print filtered_content













