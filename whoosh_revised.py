import os
import sqlite3
import binascii
from whoosh.qparser import QueryParser
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
    content = fileobj.read()
    fileobj.close()
    writer.add_document(title=u"Astronomy Article", path=doc_loc, content=str(content))
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
def get_word_list(index):
    try:
        searcher = index.searcher()
        return list(searcher.lexicon("content"))
    finally:
        searcher.close()

def hitting(word_list):
    result = {}
    for w in word_list:
        if findConceptsLike(w):
            if w in result:
                result[w] += 1
            else:
                result[w] = 1
    return result

def stop_word_filter(word_list, stop_word_list):
    filtered_list = filter(lambda x: x not in stop_word_list, word_list)
    return filtered_list

if __name__ == "__main__":
    index = create_index(my_schema)
    add_doc(index, "./sample/astronomyArticle.txt")
    stop_word_list = get_stop_word()
    word_list = get_word_list(index)
    filtered_content = stop_word_filter(word_list, stop_word_list)
    dbConnect()
    print (hitting(filtered_content))
