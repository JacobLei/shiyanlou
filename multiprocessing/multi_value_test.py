#!/usr/bin/env python3

from multiprocessing import Process, Value, Lock
import os

def f1():
    n = 0 
    while n<10000:
        print(os.getpid(), end=' ')
        n = n + 1

def f2():
    n = 0 
    while n<10000:
        print(os.getpid(), end=' ')
        n = n + 1

if __name__ == '__main__':
    filename = '/home/shiyanlou/out.txt'
    p1 = Process(target=f1)
    p1.start()
    p1.join()
    p2 = Process(target=f2)
    p2.start()
    p2.join()


