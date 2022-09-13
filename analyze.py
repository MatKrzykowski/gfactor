#!/usr/bin/env python3
from setup import sims
import gtensor
from output import copy_wkr

# For all considered simulations
for sim in sims:
    # Copy files for safekeeping
    copy_wkr(sim)
    if sim.options.write_default:
        # wkr_new.dat
        sim.write_to_file()
        # wkr_unsorted.dat
        sim.write_to_file_unsorted_sim()
        # Minima
        sim.write_minimum_info()
        # Ranges
        sim.write_ranges_info()
        # g-factors
        sim.write_gfactor_info()
        # piezo
        sim.write_piezo_info()

    if sim.options.write_fit_data:
        # lol
        sim.write_fitting_points()

for sim in gtensor.sims:
    # Data for g-tensor calculations
    if sim.options.write_gtensor:
        sim.write_gtensor()
