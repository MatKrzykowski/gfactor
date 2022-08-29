#!/usr/bin/env python3.6

from os import system

# Import from my modules
from options import Options
from simulation import Simulation
from common import psi_release
from lists import B_list_gtensor, B_list_gtensor_xy, B_list_gtensor_xz, B_list_gtensor_yz, B_list_gtensor_x, B_list_gtensor_y

from common import make_psi, echo, sqrt2
from counter import Counter
from clear_files import clear_files

if Options().Polaron:
    psi_release()


sims = [
    # Symmetric
    Simulation(Options(gtensor_E=-4.100765144, eps=1e-7),
               projectname="test_E_field",
               n_list=[1],
               output_filename="gtensor/sym/wkr_new.dat",
               in_plane_E_list=[(0., 0.)],
               B_list=B_list_gtensor),
    # [110]
    Simulation(Options(gtensor_E=-3.973930182, eps=1e-7),
               projectname="test_shift110",
               n_list=[2],
               output_filename="gtensor/110/2/wkr_new.dat",
               in_plane_E_list=[(0., 0.)],
               B_list=B_list_gtensor),
    Simulation(Options(gtensor_E=-3.901344324, eps=1e-7),
               projectname="test_shift110",
               n_list=[24],
               output_filename="gtensor/110/2.5/wkr_new.dat",
               in_plane_E_list=[(0., 0.)],
               B_list=B_list_gtensor),
    Simulation(Options(gtensor_E=-3.773402021, eps=1e-7),
               projectname="test_shift110",
               n_list=[3],
               output_filename="gtensor/110/3/wkr_new.dat",
               in_plane_E_list=[(0., 0.)],
               B_list=B_list_gtensor),
    Simulation(Options(gtensor_E=-3.497840484, eps=1e-7),
               projectname="test_shift110",
               n_list=[4],
               output_filename="gtensor/110/4/wkr_new.dat",
               in_plane_E_list=[(0., 0.)],
               B_list=B_list_gtensor),
    Simulation(Options(gtensor_E=-1.182390712, eps=1e-7),
               projectname="test_shift110",
               n_list=[10],
               output_filename="gtensor/110/high/wkr_new.dat",
               in_plane_E_list=[(0., 0.)],
               B_list=B_list_gtensor),
    # [110] compensation
    Simulation(Options(gtensor_E=-4.024947309, eps=1e-7),
               projectname="test_shift110",
               n_list=[2],
               output_filename="gtensor/110_comp/wkr_new.dat",
               in_plane_E_list=[(-3.761e-1, -3.761e-1)],
               B_list=B_list_gtensor),
    # [100]
    Simulation(Options(gtensor_E=-3.803338546, eps=1e-7),
               projectname="test_shift100",
               n_list=[5],
               output_filename="gtensor/100/top/wkr_new.dat",
               in_plane_E_list=[(0., 0.)],
               B_list=B_list_gtensor),
    Simulation(Options(gtensor_E=-3.2429031155, eps=1e-7),
               projectname="test_shift100",
               n_list=[10],
               output_filename="gtensor/100/before/wkr_new.dat",
               in_plane_E_list=[(0., 0.)],
               B_list=B_list_gtensor),
    Simulation(Options(gtensor_E=-2.689203644, eps=1e-7),
               projectname="test_shift100",
               n_list=[14],
               output_filename="gtensor/100/after/wkr_new.dat",
               in_plane_E_list=[(0., 0.)],
               B_list=B_list_gtensor),
    # E-field [110] half of the minimum
    Simulation(Options(gtensor_E=-3.993856652, eps=1e-7),
               projectname="test_E_field",
               n_list=[1],
               output_filename="gtensor/E[110]/0.5Emin/wkr_new.dat",
               in_plane_E_list=[(0.384, 0.384)],
               B_list=B_list_gtensor),
    # E-field [110] at minimum
    Simulation(Options(gtensor_E=-3.736216804, eps=1e-7),
               projectname="test_E_field",
               n_list=[1],
               output_filename="gtensor/E[110]/Emin/wkr_new.dat",
               in_plane_E_list=[(0.768, 0.768)],
               B_list=B_list_gtensor),
    # E-field [110] 3/2 of the minimum
    Simulation(Options(gtensor_E=-3.399747778, eps=1e-7),
               projectname="test_E_field",
               n_list=[1],
               output_filename="gtensor/E[110]/1.5Emin/wkr_new.dat",
               in_plane_E_list=[(1.152, 1.152)],
               B_list=B_list_gtensor),
    Simulation(Options(gtensor_E=-2.410520818, eps=1e-7),
               projectname="test_E_field",
               n_list=[1],
               output_filename="gtensor/E[110]/3/wkr_new.dat",
               in_plane_E_list=[(2.1213203435596, 2.1213203435596)],
               B_list=B_list_gtensor),
    Simulation(Options(gtensor_E=1.70579287, eps=1e-7),
               projectname="test_E_field",
               n_list=[1],
               output_filename="gtensor/E[110]/8/wkr_new.dat",
               in_plane_E_list=[(5.6568542494924, 5.6568542494924)],
               B_list=B_list_gtensor),
    # E-field [100] 1.5 (top)
    Simulation(Options(gtensor_E=-3.851844329, eps=1e-7),
               projectname="test_E_field",
               n_list=[1],
               output_filename="gtensor/E[100]/1.25/wkr_new.dat",
               in_plane_E_list=[(1.25, 0.0)],
               B_list=B_list_gtensor),
    # E-field [100] 3.2 (before jump)
    Simulation(Options(gtensor_E=-3.021373838, eps=1e-7),
               projectname="test_E_field",
               n_list=[1],
               output_filename="gtensor/E[100]/3.2/wkr_new.dat",
               in_plane_E_list=[(3.2, 0.0)],
               B_list=B_list_gtensor),
    # E-field [100] 3.7 (after jump)
    Simulation(Options(gtensor_E=-2.732452771, eps=1e-7),
               projectname="test_E_field",
               n_list=[1],
               output_filename="gtensor/E[100]/3.7/wkr_new.dat",
               in_plane_E_list=[(3.7, 0.0)],
               B_list=B_list_gtensor),
    # Lines
    Simulation(Options(gtensor_E=-3.736216804, eps=1e-7),
               projectname="test_E_field",
               n_list=[1],
               output_filename="gtensor/lines/xy/wkr_new.dat",
               in_plane_E_list=[(0.768, 0.768)],
               B_list=B_list_gtensor_xy),
    Simulation(Options(gtensor_E=-3.736216804, eps=1e-7),
               projectname="test_E_field",
               n_list=[1],
               output_filename="gtensor/lines/xz/wkr_new.dat",
               in_plane_E_list=[(0.768, 0.768)],
               B_list=B_list_gtensor_xz),
    Simulation(Options(gtensor_E=-3.736216804, eps=1e-7),
               projectname="test_E_field",
               n_list=[1],
               output_filename="gtensor/lines/x/wkr_new.dat",
               in_plane_E_list=[(0.768, 0.768)],
               B_list=B_list_gtensor_x),
    Simulation(Options(gtensor_E=-3.736216804, eps=1e-7),
               projectname="test_E_field",
               n_list=[1],
               output_filename="gtensor/lines/y/wkr_new.dat",
               in_plane_E_list=[(0.768, 0.768)],
               B_list=B_list_gtensor_y),
    Simulation(Options(gtensor_E=-3.736216804, eps=1e-10),
               projectname="test_shift100",
               n_list=[1],
               output_filename="gtensor/lines/xz_low/wkr_new.dat",
               in_plane_E_list=[(0.768, 0.768)],
               B_list=B_list_gtensor_xz*1e-3),
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
