#!/usr/bin/env python3.6

from common import make_psi, echo
from counter import Counter
from clear_files import clear_files
from options import Options
from setup import sims

# File maintainance
make_psi()  # Compile newest psi version
clear_files()  # Clear unnecessary files

counter = Counter(sims, Options().enable_counter)

# Generate required minimum
for sim in sims:
    sim.counter = counter

# Generate required minimum
for sim in sims:
    sim.counter = counter
    sim.gen_required()
    sim.gen_required()

# Keep generating data given time
counter.enable = False
while Options().continue_calculations:
    for sim in sims:
        sim.continue_generating()
        sim.options.increase_threshold()
    echo("Increasing threshold of calculations")
