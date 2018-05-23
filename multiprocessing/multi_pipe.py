from multiprocessing import Process, Pipe

conn1, conn2 = Pipe()

def f1():
    for i in range(100):    
        conn1.send(i)

def f2():
    for i in range(100):
        print(conn2.recv())

def main():
    Process(target=f1).start()
    Process(target=f2).start()

if __name__ == '__main__':
    main()
