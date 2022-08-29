#!/usr/bin/env python3.6

from os import system

from common import make_psi, echo
from counter import Counter
from clear_files import clear_files
from options import Options
from setup import sims

# File maintainance
system("cp psi_piezo.F08 psi.F08")
make_psi()  # Compile newest psi version
clear_files()  # Clear unnecessary files

counter = Counter(sims, Options().enable_counter)

# Generate required minimum
for sim in sims:
    sim.counter = counter

# Generate additional data if requested
for sim in sims:
    sim.gen_various()

echo("Additional information generated for all structures")

system("cp psi_proper.F08 psi.F08")
make_psi()  # Compile newest psi version
system("calc/run.py")
