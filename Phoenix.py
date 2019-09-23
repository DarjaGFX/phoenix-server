import sys
import os
import time
from multiprocessing import Process
import subprocess
import numpy as np

tbl = {}

def __terminator():
    global tbl
    for i in list(tbl.keys()):
        try:
            os.remove(i)
        except:
            pass

def __start(path):
    """
    Runs python file from path  
    """
    os.system('python {}'.format(path))

def __md5(path):
    return subprocess.getoutput('md5sum {}'.format(path))

def __sha256(path):
    return subprocess.getoutput('sha256sum {}'.format(path))

def secure():
    """
    stores all files to check in future if their changed or not!
    """
    tbl = dict()
    dirs = sys.argv[2:]
    for d in dirs:
        ls = os.listdir(d)
        for f in ls:
            path = '{}/{}'.format(d,f)
            tbl.update({path:(__md5(path), __sha256(path))})
    np.save('core',tbl)

def lookForChange():
    ### look for checksum missmatch to delete files and kill processes :-)
    global tbl
    flag = True
    while flag:
        for f in list(tbl.keys()):
            chcksm = (__md5(f),__sha256(f))
            if chcksm != tbl[f]:
                flag = False            
        time.sleep(1)
    return True

def __load():
    try:
        t = dict(np.ndarray.tolist(np.load('core.npy', allow_pickle=True)))
    except:
        print('npy file not found!')
        t = {}
    return t

def run():
    """
    runs all files in an indpndnt process
    """
    p = []
    for i in range(2,len(sys.argv)):
        p.append(Process(target=__start,args=(sys.argv[i],)))
    for pr in p:
        pr.start()  
    if lookForChange():
        for pr in p:
            pr.terminate()
        __terminator()
        os.kill(os.getppid(),9)

def main():
    # print(sys.argv)
    global tbl
    ctrl = sys.argv[1]
    if ctrl.lower() =='run':
        tbl = __load()
        run()
    elif ctrl.lower() == 'secure':
        secure()    

if __name__ == "__main__":
    main()
