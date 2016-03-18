import sqlite3
import os

db = None

def main():
    db_connect()
    prefLabels = findConceptsLike("star")
    for p in prefLabels:
        print(p)

    db.close()

# Returns a list of concept PrefLabels in the UAT that contain the pattern 'term'
def findConceptsLike(term):
    prefLabels = []
    # SQL query to find all concepts where PrefLabel contains the pattern 'term'
    sql = 'SELECT PrefLabel FROM CONCEPT WHERE PrefLabel LIKE ' + "'%" + term + "%'"
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

main()
