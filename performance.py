import timeit
import os

start = timeit.default_timer()

os.system("python whoosh_example.py")

stop = timeit.default_timer()

print stop - start
