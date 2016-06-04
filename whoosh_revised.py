import os, os.path
import sqlite3
from whoosh import index
from whoosh.fields import Schema, TEXT, ID
from whoosh.analysis import StemmingAnalyzer
from whoosh.qparser import QueryParser

#=============design schema===========
my_schema = Schema(path = ID,
                   author = TEXT,
                   date = ID,
                   title = TEXT(stored=True, analyzer=StemmingAnalyzer()),
                   content = TEXT(stored=True, analyzer=StemmingAnalyzer()))

#=============create index and add document===========
def create_index(schema):
    if not os.path.exists("index"):
        os.mkdir("index")
        ix = index.create_in("index", schema=schema)
    else:
        ix = index.open_dir("index")
    return ix

def index_doc(index, doc_loc):
    writer = index.writer()
    fileobj = open(doc_loc, "r")
    content = fileobj.read()
    writer.add_document(title=u"Astronomy Article", path=doc_loc, content=content)
    fileobj.close()
    writer.commit()

#=============getting all the stop words (unused, customized stop_word needed?)===========
def get_stop_word():
    stop_words = []
    with open('stopwords_1.txt','r') as f1:
        for line in f1:
            for word in line.split():
               stop_words.append(word)
    with open('stopwords_2.txt','r') as f2:
        for line in f2:
            for word in line.split():
               stop_words.append(word)
    return stop_words

#=============getting UAT keywords from database===========
db = None

def dbConnect():
    global db
    try:
        dbName = "concepts.sqlite"
        if os.path.exists(dbName):
            db = sqlite3.connect(dbName)
            print ("database connected")
        else:
            print ("Error:", dbName, "does not exits" )

    except sqlite3.IntegrityError as err:
        print('Integrity Error on connect:', err)
    except sqlite3.OperationalError as err:
        print('Operational Error in connect:', err)
    except sqlite3.Error as err:
        print('Error in connect:', err)

def findConceptsLike(term):
    prefLabels = []

    sql = 'SELECT PrefLabel FROM CONCEPT WHERE PrefLabel LIKE' + "'%" + term.decode('utf-8') + "%'"

    try:
        cursor = db.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        if len(rows) > 0:
            for r in rows:
                prefLabels.append(r)
        return prefLabels
    except sqlite3.IntegrityError as err:
        print('Integrity Error in getPrefLabelFor:', err)
    except sqlite3.OperationalError as err:
        print('Operational Error in getPrefLabelFor:', err)
    except sqlite3.Error as err:
        print('Error in getPrefLabelFor:', err)

#=============searching and counting===========
def querying(index, keyword):
    try:
        searcher = index.searcher()
        qp = QueryParser("word", schema=index.schema)
        q = qp.parse("Sarah")
        result = searcher.search(q, limit=10)
        print (result)
    finally:
        searcher.close()

def hits(word_list):
    result = {}
    for w in word_list:
        if findConceptsLike(w):
            if w in result:
                result[w] += 1
            else:
                result[w] = 1
    return result

def stop_word_filter(word_list, stop_word_list):
    filtered_list = filter(lambda x: x.decode("utf-8") not in stop_word_list, word_list)
    return list(filtered_list)


if __name__ == "__main__":
    index = create_index(my_schema)
    index_doc(index, "./sample/astronomyArticle.txt")
    print (index)
    searcher = index.searcher()
    querying(index, u"world")

