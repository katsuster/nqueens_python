#!/usr/bin/python

import threading

__author__ = 'Katsuhiro Suzuki'


class Solver(threading.Thread):
    def __init__(self, row, left, right, n, y, answer):
        threading.Thread.__init__(self)
        self.row = row
        self.left = left
        self.right = right
        self.n = n
        self.y = y
        self.answer = answer
        self.new_answer = 0

    def get_new_answer(self):
        return self.new_answer

    def run(self):
        self.new_answer = self.solve_inner(self.row, self.left, self.right,
                                           self.n, self.y, self.answer)

    def solve_inner(self, row, left, right, n, y, answer):
        if y == n:
            #found the answer
            return answer + 1

        field = ((1 << n) - 1) & ~(left | row | right)
        while field != 0:
            xb = -field & field
            field &= ~xb

            n_row = row | xb
            n_left = (left | xb) << 1
            n_right = (right | xb) >> 1

            #find the next line
            answer = self.solve_inner(n_row, n_left, n_right, n, y + 1, answer)

        return answer
