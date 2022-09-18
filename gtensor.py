#!/usr/bin/env python3.6

from os import system

# Import from my modules
from options import Options
from simulation import Simulation
from common import psi_release
from lists import B_list_gtensor

from common import make_psi, echo
from counter import Counter
from clear_files import clear_files

if Options().Polaron:
    psi_release()


sims = [
    # C2v
    Simulation(Options(gtensor_E=-4.3280376706999997), projectname="new_gtensor",
               n_list=[1],
               output_filename="new_gfactor/wkr_new.dat",
               in_plane_E_list=[(0.0, 0.0)],
               B_list=B_list_gtensor),
    # Cs[110] small
    Simulation(Options(gtensor_E=-4.2584691500999998), projectname="new_gtensor",
               n_list=[2],
               output_filename="new_gfactor/wkr_new.dat",
               in_plane_E_list=[(0.0, 0.0)],
               B_list=B_list_gtensor),
    # Cs[110] large
    Simulation(Options(gtensor_E=2.9755692701999998), projectname="new_gtensor",
               n_list=[3],
               output_filename="new_gfactor/wkr_new.dat",
               in_plane_E_list=[(0.0, 0.0)],
               B_list=B_list_gtensor),
    # C1
    Simulation(Options(gtensor_E=-4.0026005500000004), projectname="new_gtensor",
               n_list=[4],
               output_filename="new_gfactor/wkr_new.dat",
               in_plane_E_list=[(0.0, 0.0)],
               B_list=B_list_gtensor),
    # C2 small
    Simulation(Options(gtensor_E=-4.5184076203999997), projectname="new_gtensor",
               n_list=[5],
               output_filename="new_gfactor/wkr_new.dat",
               in_plane_E_list=[(0.0, 0.0)],
               B_list=B_list_gtensor),
    # C2 large
    Simulation(Options(gtensor_E=-3.6550266988000000), projectname="new_gtensor",
               n_list=[6],
               output_filename="new_gfactor/wkr_new.dat",
               in_plane_E_list=[(0.0, 0.0)],
               B_list=B_list_gtensor),
]

if __name__ == "__main__":
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
    # system("calc/run.py")
