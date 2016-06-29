import re
import sqlite3
import os
from nltk.corpus import stopwords

"""
TODO
1. fix the OperationalError of sql command
2. look into the implementation of nltk's word counti, see if it's a faster option
3. still need stopword and punctuation filters ?
"""

# connect to UAT database
def db_connect():
    global db
    try:
        dbname = 'concepts.sqlite'
        if os.path.exists(dbname):
            db = sqlite3.connect(dbname)
        else:
            print('Error:', dbname, 'does not exist')
    except sqlite3.IntegrityError as err:
        print('Integrity Error on connect:', err)
    except sqlite3.OperationalError as err:
        print('Operational Error on connect:', err)
    except sqlite3.Error as err:
        print('Error on connect:', err)

# looking for match in UAT
def findConceptsLike(term):
    # SQL query to find all concepts where PrefLabel contains the pattern 'term'
    sql = 'SELECT PrefLabel FROM CONCEPT WHERE lower(PrefLabel) = ' + "'" + term + "'"
    try:
        cursor = db.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        if len(rows) > 0:
           return True
        return False
    except sqlite3.IntegrityError as err:
        print('Integrity Error in getPrefLabelFor:', err)
    except sqlite3.OperationalError as err:
        print('Operational Error in getPrefLabelFor:', err)
    except sqlite3.Error as err:
        print('Error in getPrefLabelFor:', err)

# getting the words in the doc
def get_content(file):
    words = []
    with open(file) as f:
        for line in f:
            for w in line.split():
                words.append(w.lower())
    return words

# counting the frequency of words
def counting(words):
    word_count = {}
    for w in words:
        if findConceptsLike(w):
           if w not in word_count:
              word_count[w] = 1
           else:
              word_count[w] += 1
    return word_count

def main():
    words = get_content("./sample/astronomyArticle.txt")
    db_connect()
    word_count = counting(words)
    print (word_count)

if __name__ == "__main__":
    main()


