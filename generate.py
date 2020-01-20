from random import choice
from time import time
from functools import reduce
import os,sys
from .py_utils import *

NUMBERS_DAT="numbers.dat"
SEQ_LEN = 6

fn_generate = lambda begin,end: [x for x in range(begin,end+1)]

def pick_a_number(nth_pick, pool, selected_list):
    if nth_pick == 0:
        return
    else:
        selected = choice(pool)
        pool.remove(selected)
        selected_list.append(selected)
        pick_a_number(nth_pick-1, pool,selected_list)



def secondsToStr(t):
    return "%d:%02d:%02d.%03d" % \
        reduce(lambda ll,b : divmod(ll[0],b) + ll[1:],
            [(t*1000,),1000,60,60])

def keep_generating_for(termination_seconds):
    counter = 0
    start_time=time()
    termination_seconds_str = secondsToStr(termination_seconds)
    with open(NUMBERS_DAT, "w") as file:
        while True:
            pool = fn_generate(1,49)
            sequence = []
            pick_a_number(SEQ_LEN,pool,sequence)
            sequence = sorted(sequence)
            file.write(",".join([str(x) for x in sequence]) + "\n")
            end_time = time()
            counter += 1

            sys.stdout.write ("%s | %s: %d sequences generated...\r" % (secondsToStr(end_time-start_time),termination_seconds_str,counter))
            
            if end_time - start_time >= termination_seconds:
                break
    sys.stdout.write("\n")
    print("Generation completed. Please checkout numbers.dat")

if __name__ == "__main__":
    script, Nseconds = sys.argv
    Nseconds = int(Nseconds)
    keep_generating_for(Nseconds)

        

