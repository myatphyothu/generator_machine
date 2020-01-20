from random import choice
from time import time
from functools import reduce
import os,sys, pickle
from py_utils import *
from py_utils.algorithms import py_algorithm as pal
from py_utils.graphs import py_markov_chain

NUMBERS_DAT="generator_machine/sequences.txt"
PICKLED_MARKOV_CHAIN="generator_machine/markov_chain.pickle"
SEQ_LEN = 6
markov_chain = None
fn_generate = lambda begin,end: [x for x in range(begin,end+1)]
#----------------------------------------------------------------------------------------------------------------
def pick_a_number(nth_pick, pool, selected_list):
    if nth_pick == 0:
        return
    else:
        selected = choice(pool)
        pool.remove(selected)
        selected_list.append(selected)
        pick_a_number(nth_pick-1, pool,selected_list)

#----------------------------------------------------------------------------------------------------------------
def secondsToStr(t):
    return "%d:%02d:%02d.%03d" % \
        reduce(lambda ll,b : divmod(ll[0],b) + ll[1:],
            [(t*1000,),1000,60,60])
#----------------------------------------------------------------------------------------------------------------
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
    print("Generation completed. Please checkout %s" % NUMBERS_DAT)
#----------------------------------------------------------------------------------------------------------------
def compare(compare_file):
    def get_compare_data(compare_file):
        data_list = []
        if os.path.exists(compare_file):
            with open(compare_file, "r") as f:
                lines = f.readlines()
                for line in lines:
                    splited_by_comma = line.strip().split(",")
                    if len(splited_by_comma) == 8:
                        data =  splited_by_comma[1:7]
                        data_list.append(data)
        return data_list

    def get_generated_data(generated_file):
        data_list = []
        if os.path.exists(generated_file):
            with open(generated_file, "r") as f:
                lines = f.readlines()
                for line in lines:
                    splited_by_comma = line.strip().split(",")
                    if len(splited_by_comma) == 6:
                        data_list.append(splited_by_comma)
        return data_list

    def search(compare_data, generated_list):
        for generated_seq in generated_list:
            if set(compare_data) == set(generated_seq):
                return True
        return False
    
    compare_data_list = get_compare_data(compare_file)
    T1 = len(compare_data_list)
    generated_data_list = get_generated_data(NUMBERS_DAT)
    matched = []
    T2 = len(matched)

    for i,data in enumerate(compare_data_list):
        found = search(data, generated_data_list)
        if found:
            matched.append(data)
            T2 = len(matched)
        sys.stdout.write ("comparing %d/%d. match found = %d ...\r" % (i+1,T1,T2))
    sys.stdout.write("\n")

    print("...the following sequences matchd.")
    for i,data in enumerate(matched):
        print("%d. %s" % (i+1, ",".join(data)))
#----------------------------------------------------------------------------------------------------------------
def create_markov_chain(datafile):
    global markov_chain
    markov_chain_raw_data = []

    
    if os.path.exists(datafile):
        with open(datafile, "r") as f:
            lines = f.readlines()
            T=len(lines)
            for i,line in enumerate(lines):
                sequence = line.strip().split(",")
                new_sequence = [int(x) for x in sequence]
                markov_chain_raw_data.append(new_sequence)
                sys.stdout.write("extracting raw data %d/%d ...\r" % (i+1,T))

    sys.stdout.write("\n")
    if len(markov_chain_raw_data) > 0:
        print("creating markov chain... ", end="")
        markov_chain = py_markov_chain(markov_chain_raw_data)
        print("COMPLETED")

    print(markov_chain.matrix())

    #pickle the markov data
    pickle_file = open(PICKLED_MARKOV_CHAIN, "ab")
    pickle.dump(markov_chain,pickle_file)
    pickle_file.close()
#----------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    script, args = sys.argv[0], sys.argv[1:]
    if args[0] == "generate":
        if len(args) > 1:
            Nseconds = int(args[1])
            keep_generating_for(Nseconds)
    elif args[0] == "compare":
        if len(args) > 1:
            compare_file = args[1]
            compare(compare_file)
    elif args[0] == "create" and args[1] == "markov":
        if len(args) == 2:
            create_markov_chain(NUMBERS_DAT)

        

