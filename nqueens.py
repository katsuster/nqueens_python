#!/usr/bin/python

import sys
import time
#import threading

import solver

__author__ = 'Katsuhiro Suzuki'


def main(argv):
    """
    Main function.
    :param argv: The arguments from command line.
    :return: 0 is success, non 0 is error.
    """
    if len(argv) < 2:
        print("usage: \n"
              + argv[0] + " queens(1 ... 30) parallel(true or false)")
        return -1

    #get the arguments
    n = int(argv[1])
    if (n < 0) or (30 < n):
        n = 0
    print("queens  : " + str(n))

    parallel = False
    if len(argv) >= 3:
        parallel = argv[2] in ["true", "True"]
    print("parallel: " + str(parallel))

    #start
    start = time.time()

    #solve
    center = n >> 1
    solvers = []

    answer = 0
    for x in range(0, center):
        #left half
        row = 1 << x
        left = row << 1
        right = row >> 1

        s = solver.Solver(row, left, right, n, 1, 0)
        if parallel:
            s.start()
        else:
            s.run()
        solvers.append(s)

    if n % 2 == 1:
        #center(if N is odd)
        row = 1 << center
        left = row << 1
        right = row >> 1

        solver_remain = solver.Solver(row, left, right, n, 1, 0)
        if parallel:
            solver_remain.start()
        else:
            solver_remain.run()

    #join
    for s in solvers:
        if parallel:
            s.join()
        answer += s.get_new_answer()
    answer *= 2

    try:
        if parallel:
            solver_remain.join()
        answer += solver_remain.get_new_answer()
    except NameError:
        pass

    #finished
    elapse = time.time() - start

    #solved
    print("answers : " + str(answer))
    print("time    : " + str(elapse) + "[s]")


if __name__ == "__main__":
    main(sys.argv[0:])
