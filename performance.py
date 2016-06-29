import timeit
import os

start = timeit.default_timer()

os.system("python nltk_version.py")

stop = timeit.default_timer()

print (stop - start)
