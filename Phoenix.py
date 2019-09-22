import sys
import os
import time
from multiprocessing import Process
import subprocess
import numpy as np

def __terminator(tbl):
    for i in list(tbl.keys()):
        os.remove(i)

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
    while True:
        tbl = __load()
        for f in list(tbl.keys()):
            chcksm = (__md5(f),__sha256(f))
            if chcksm != tbl[f]:
                return True
        time.sleep(3600)

def __load():
    try:
        t = dict(np.ndarray.tolist(np.load('core.npy')))
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
        __terminator(__load())

def main():
    # print(sys.argv)
    ctrl = sys.argv[1]
    if ctrl.lower() =='run':
        run()
    elif ctrl.lower() == 'secure':
        secure()    

if __name__ == "__main__":
    main()
