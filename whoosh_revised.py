import os
import sqlite3
from nltk.corpus import stopwords
from whoosh import scoring
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

#=============getting all the stop words (unused, customized stop_word needed?)===========
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

#=============getting UAT keywords from database===========
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

#=============searching and filtering stop words===========
def searcher(index, thesaurus):
    try:
        searcher = index.searcher()
        word_list = list(searcher.lexicon("content"))
        return word_list
    finally:
        searcher.close()

def stop_word_filter(word_list):
    filtered_list = filter(lambda x: x not in stopwords.words('english'), word_list)
    return filtered_list


if __name__ == "__main__":
    index = create_index(my_schema)
    add_doc(index, "/Users/Robert/Desktop/HiveFoundationRebuild/sample/astronomyArticle.txt")
    word_list = searcher(index)
    filtered_content = stop_word_filter(word_list)
    dbConnect()
    UAT_words = unicode(findConceptsLike())















