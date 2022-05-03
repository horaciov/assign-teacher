
from multiprocessing import Process, Queue
import queue


def print_func(qu,continent='Asia'):
    print('The name of continent is : ', continent)
    qu.put(continent)

if __name__ == "__main__":  # confirms that the code is under main function
    names = ['America', 'Europe', 'Africa']
    procs = []
    q = Queue()
    proc = Process(target=print_func,args=(q,'Asia'))  # instantiating without any argument
    procs.append(proc)
    proc.start()

    # instantiating process with arguments
    for name in names:
        # print(name)
        proc = Process(target=print_func, args=(q,name))
        procs.append(proc)
        proc.start()

    # complete the processes
    for proc in procs:
        proc.join()

    while not q.empty():
        print(q.get())
    print("Hola")