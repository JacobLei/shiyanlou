#!/usr/bin/env python3

from multiprocessing import Pool
import os

def f(i):
    print(i, end=' ')
    print(os.getpid())

def main():
    pool = Pool(processes=3)
    for i in range(30):
        pool.apply(f,(i,))
    pool.close()
    pool.join()

if __name__ == '__main__':
    main()
