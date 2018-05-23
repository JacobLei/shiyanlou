#!/usr/bin/env python3

from multiprocessing import Process, Queue, Lock

queue = Queue()

def f1():
    for i in range(10):
        queue.put(i)

def f2():
    for i in range(10):
        print(queue.get())

def main():
    Process(target=f1).start()
    Process(target=f2).start()

if __name__ == '__main__':
    main()
