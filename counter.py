from numpy import sum

import time

from common import echo
from timer import print_time


class Counter():
    def __init__(self, sims, enable=True):
        self.sims = sims
        self.init_n = self.n
        self.init_t = time.time()
        self.enable = enable

    @property
    def n(self):
        return sum([sim.n for sim in self.sims])

    def update(self):
        if not self.enable:
            return None
        x = self.init_n - self.n
        echo("{}/{} done".format(x, self.init_n))
        if x <= 0 or x == self.init_n:
            return None
        print_time(x, self.init_n, self.init_t)
