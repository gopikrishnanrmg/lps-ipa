#!/usr/bin/env python
import codecs, time, resource, sys
from pympler import asizeof
from random import choice as rchoice
from comparer import comparer

K = 3
COEFFICIENT = 1.5
data = {} #Main dictionary 


def main(argv):
    if len(argv)==2:
        global K = int(argv[0])
        global COEFFICIENT = float(argv[1])

    result_f = codecs.open('data/result.txt', 'w+','utf-8')
    start = time.clock()
    i = 1
    with codecs.open('data/queries.txt', 'r','utf-8') as f:
        for line in f:
            res = line.split('\t')
            category = res[6]
            user = res[1]
            query = res[2]+ '\t'+ res[3]+ '\t'+ res[4]+ '\t'+ res[5]
            
            if not category in data:
                data[category] = [K, [], []] # [MAX_QUERIES, USERS, QUERIES]
            curcat = data[category]
            curcat[1].append(user)
            curcat[2].append(query)           

            if len(curcat[1])>=curcat[0]:	#Category full
                query_choice = rchoice(curcat[2])
                if curcat[1].count(query_choice[0]) >= curcat[0]: # All users are the same
                    curcat[0] = curcat[0]*COEFFICIENT
                else:
                    user_choice = rchoice(curcat[1])
                    while user_choice==query_choice[0]:		# Find a different user    
                        user_choice = rchoice(curcat[1])
                    result_f.write(query_choice[2] + '\t'+user_choice+'\t'+query_choice[1]+'\n')
                    curcat[1].remove(user_choice)
                    curcat[2].remove(query_choice)
                    i+=1
    mem = asizeof.asizeof(data)
    total=time.clock()-start

    result_f.close()

if __name__ == "__main__":
    main(sys.argv[1:])
