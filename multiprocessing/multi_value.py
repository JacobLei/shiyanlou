#!/usr/bin/env python3

import time
from multiprocessing import Process, Value, Lock

def func(val):
    for i in range(50):
        time.sleep(0.01)
        with lock:
            val.value += 1

if __name__ == '__main__':
    lock = Lock()
    v = Value('i', 0)

    procs1 = Process(target=func, args=(v,))
    procs2 = Process(target=func, args=(v,))
    procs3 = Process(target=func, args=(v,))

    procs1.start()
    procs1.join()
    print('procs1 = ', v.value)
   
    procs2.start()
    procs2.join()
    print('procs2 = ', v.value)
   
    procs3.start()
    procs3.join()
    print('procs3 = ', v.value)
    
    print('v.value = ', v.value)
