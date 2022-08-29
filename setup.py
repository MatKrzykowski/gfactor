#!/usr/bin/env python3.6

# Import from my modules
from options import Options
from simulation import Simulation
from common import psi_release, sqrt2
from lists import B_list, B_list_001, B_list_110, B_list_log_z, B_list_log_inplane, B_list_log_inplane_100, B_list_symm_log, B_list_extended
from lists import E_compensation100, E_compensation110, E_compensation110_high
from lists import in_plane_E_110, in_plane_E_100, in_plane_E_m110, in_plane_E_010
from lists import E_elong100_comp_E100_B100, E_elong100_comp_E110_B100
from lists import E_elong100_comp_E100_B110, E_elong100_comp_E110_B110
from lists import E_elong100_comp_E100_B001, E_elong100_comp_E110_B001
from lists import n_list_rotate, n_list_rotate_shift, n_list_elong100, n_list_elong110

if Options().Polaron:
    psi_release()


# g-factor at anticrossing
anti_gfactor = [
    # Anticrossing g-factor in symmetric case
    Simulation(Options(minima_eps=1e-5, bound_limit=0.2, fill_blank=0.8),
               projectname="E_field",
               in_plane_E_list=[(0., 0.)],
               output_filename="anticrossing_gfactor/sym/wkr_new.dat",
               B_list=B_list_001 + B_list_110),
    # Anticrossing g-factor with E-field in [110]
    Simulation(Options(minima_eps=1e-5, bound_limit=0.2, fill_blank=0.8),
               projectname="E_field",
               in_plane_E_list=[(0.7 / sqrt2, 0.7 / sqrt2)],
               output_filename="anticrossing_gfactor/Efield110/wkr_new.dat",
               B_list=B_list_001 + B_list_110),
    # Anticrossing g-factor with E-field in [100]
    Simulation(Options(minima_eps=1e-5, bound_limit=0.2, fill_blank=0.8),
               projectname="E_field",
               in_plane_E_list=[(0.7, 0.0)],
               output_filename="anticrossing_gfactor/Efield100/wkr_new.dat",
               B_list=B_list_001 + B_list_110),
    # Anticrossing g-factor with shift in [110]
    Simulation(Options(minima_eps=1e-5, bound_limit=0.2, fill_blank=0.8),
               projectname="shift110",
               n_list=[2],
               output_filename="anticrossing_gfactor/shift110/wkr_new.dat",
               B_list=B_list_001 + B_list_110),
    # Anticrossing g-factor with shift in [100]
    Simulation(Options(minima_eps=1e-5, bound_limit=0.2, fill_blank=0.8),
               projectname="shift100",
               n_list=[2],
               output_filename="anticrossing_gfactor/shift100/wkr_new.dat",
               B_list=B_list_001 + B_list_110),
]

# Zieliński effect
Zielinski = [
    # In-plane electric 110
    Simulation(Options(minima_eps=1e-6), projectname="E_field",
               in_plane_E_list=in_plane_E_110,
               output_filename="E_field/110/wkr_new.dat",
               B_list=B_list),
    # In-plane electric 100
    Simulation(Options(minima_eps=1e-5), projectname="E_field",
               in_plane_E_list=in_plane_E_100,
               output_filename="E_field/100/wkr_new.dat",
               B_list=B_list),
    # In-plane electric 010
    Simulation(Options(minima_eps=1e-5), projectname="E_field",
               in_plane_E_list=in_plane_E_010,
               output_filename="E_field/010/wkr_new.dat",
               B_list=B_list),
    # In-plane electric m110
    Simulation(Options(minima_eps=1e-5), projectname="E_field",
               in_plane_E_list=in_plane_E_m110,
               output_filename="E_field/m110/wkr_new.dat",
               B_list=B_list),
    # Compensation 110 higher
    Simulation(Options(minima_eps=1e-6), projectname="shift110",
               n_list=[7],
               output_filename="compensation/110_high/wkr_new.dat",
               in_plane_E_list=E_compensation110_high,
               B_list=[(0.0, 0.0, 1.0)]),
    # Compensation 110
    Simulation(Options(minima_eps=1e-6), projectname="shift110",
               n_list=[2],
               output_filename="compensation/110/wkr_new.dat",
               in_plane_E_list=E_compensation110,
               B_list=[(0.0, 0.0, 1.0)]),
    # Compensation 100
    Simulation(Options(minima_eps=1e-6), projectname="shift100",
               n_list=[2],
               output_filename="compensation/100/wkr_new.dat",
               in_plane_E_list=E_compensation100,
               B_list=[(0.0, 0.0, 1.0)]),
    # Shift in [110] direction
    Simulation(Options(minima_eps=1e-5), projectname="shift110",
               n_list=[1, 23, 2, 24] + [i for i in range(3, 23)],
               output_filename="shift/110/wkr_new.dat",
               B_list=B_list),
    # Shift in [110] direction with some [100]
    Simulation(Options(minima_eps=1e-5), projectname="shift110_1_1",
               n_list=[i for i in range(1, 23)],
               output_filename="shift/110_1_1/wkr_new.dat",
               B_list=[(0.0, 0.0, 1.0)]),
    # Shift in [100] direction
    Simulation(Options(minima_eps=1e-5), projectname="shift100",
               n_list=[i for i in range(1, 23)],
               output_filename="shift/100/wkr_new.dat",
               B_list=B_list),
    # Rotation of a structure elongated from 100 to 110 eta=1.2
    Simulation(Options(minima_eps=1e-5), projectname="rotate",
               n_list=n_list_rotate,
               output_filename="rotate/Brotate/wkr_new.dat"),
    # # Rotation of a structure elongated from 100 to 110 eta=1.2 with B along QD elong axis
    Simulation(Options(minima_eps=1e-5), projectname="rotate",
               n_list=n_list_rotate,
               output_filename="rotate/Balong/wkr_new.dat",
               B_list=[(1.0, 0.0, 0.0), (0.0, 0.0, 1.0)]),
    # Rotation of a structure shifted from 100 to 110 eta=1.2
    Simulation(Options(minima_eps=1e-5), projectname="rotate_shift",
               n_list=n_list_rotate_shift,
               output_filename="rotate_shift/Brotate/wkr_new.dat"),
    # Rotation of a structure shifted from 100 to 110 eta=1.2
    Simulation(Options(minima_eps=1e-5), projectname="rotate_shift",
               n_list=n_list_rotate_shift,
               output_filename="rotate_shift/Balong/wkr_new.dat",
               B_list=[(1.0, 0.0, 0.0), (0.0, 0.0, 1.0)]),
    # Elongation 100
    Simulation(Options(minima_eps=1e-5), projectname="elong_100",
               n_list=n_list_elong100,
               output_filename="elong/100/wkr_new.dat",
               B_list=[(0.0, 0.0, 1.0), (1.0, 0.0, 0.0), (1 / sqrt2, 1 / sqrt2, 0.0)]),
    # Elongation 110
    Simulation(Options(minima_eps=1e-5), projectname="elong_110",
               n_list=n_list_elong110,
               output_filename="elong/110/wkr_new.dat",
               B_list=[(0.0, 0.0, 1.0), (1.0, 0.0, 0.0), (1 / sqrt2, 1 / sqrt2, 0.0)]),
    # Elongation 100 compensation B[100]
    Simulation(Options(minima_eps=1e-5), projectname="elong_100",
               n_list=[6],
               output_filename="elong_comp/100/B100/E100/wkr_new.dat",
               in_plane_E_list=E_elong100_comp_E100_B100,
               B_list=[(1.0, 0.0, 0.0)]),
    # Elongation 100 compensation B[100]
    Simulation(Options(minima_eps=1e-5), projectname="elong_100",
               n_list=[6],
               output_filename="elong_comp/100/B100/E110/wkr_new.dat",
               in_plane_E_list=E_elong100_comp_E110_B100,
               B_list=[(1.0, 0.0, 0.0)]),
    # Elongation 100 compensation B[110]
    Simulation(Options(minima_eps=1e-5), projectname="elong_100",
               n_list=[7],
               output_filename="elong_comp/100/B110/E100/wkr_new.dat",
               in_plane_E_list=E_elong100_comp_E100_B110,
               B_list=[(1.0/sqrt2, 1.0/sqrt2, 0.0)]),
    # Elongation 100 compensation B[110]
    Simulation(Options(minima_eps=1e-5), projectname="elong_100",
               n_list=[7],
               output_filename="elong_comp/100/B110/E110/wkr_new.dat",
               in_plane_E_list=E_elong100_comp_E110_B110,
               B_list=[(1.0/sqrt2, 1.0/sqrt2, 0.0)]),
    # Elongation 100 compensation B[001]
    Simulation(Options(minima_eps=1e-5), projectname="elong_100",
               n_list=[7],
               output_filename="elong_comp/100/B001/E100/wkr_new.dat",
               in_plane_E_list=E_elong100_comp_E100_B001,
               B_list=[(0.0, 0.0, 1.0)]),
    # Elongation 100 compensation B[001]
    Simulation(Options(minima_eps=1e-5), projectname="elong_100",
               n_list=[7],
               output_filename="elong_comp/100/B001/E110/wkr_new.dat",
               in_plane_E_list=E_elong100_comp_E110_B001,
               B_list=[(0.0, 0.0, 1.0)]),
    # B-field dependence in z
    Simulation(Options(minima_eps=1e-6, write_fit_data=True),
               projectname="shift110",
               n_list=[2],
               output_filename="B_field_gfactor/wkr_new.dat",
               in_plane_E_list=[(0., 0.)],
               B_list=B_list_log_z),
    # B-field dependence in-plane
    Simulation(Options(minima_eps=1e-7, write_fit_data=True),
               projectname="shift110",
               n_list=[2],
               output_filename="B_field_gfactor/wkr_new.dat",
               in_plane_E_list=[(0., 0.)],
               B_list=B_list_log_inplane),
    # B-field dependence in-plane for shift in [100]
    Simulation(Options(minima_eps=1e-6, write_fit_data=True),
               projectname="shift100",
               n_list=[2],
               output_filename="B_field_gfactor/100/wkr_new.dat",
               in_plane_E_list=[(0., 0.)],
               B_list=B_list_log_inplane_100),
]

# g-factor
gfactor = [
    # Example
    Simulation(Options(minima_eps=1e-6), projectname="E_field",
               in_plane_E_list=[(0.0, 0.0), (3.5355339059327373, 3.5355339059327373)],
               output_filename="example/wkr_new.dat",
               B_list=[(0.0, 0.0, 1.0)]),
    # B-field dependence in symmetrical case
    Simulation(Options(),
               projectname="shift110",
               n_list=[1],
               output_filename="B_field_gfactor/symm/wkr_new.dat",
               in_plane_E_list=[(0., 0.)],
               B_list=B_list_symm_log),
    # B-field in various directions
    Simulation(Options(), projectname="E_field",
               output_filename="B_field/wkr_new.dat",
               B_list=B_list_extended),
    # In concentration
    Simulation(Options(), projectname="diffc",
               n_list=[20] + [i for i in range(1, 18)],
               output_filename="QD_params/concentration/wkr_new.dat",
               B_list=B_list),
    # Distance between QDs
    Simulation(Options(), projectname="diffH",
               n_list=[i for i in range(1, 27)],
               output_filename="QD_params/distance/wkr_new.dat",
               B_list=B_list),
    # Radius of upper QD
    Simulation(Options(gfactor_to_right=False), projectname="QDtopvar",
               n_list=[i for i in range(1, 14)],
               output_filename="QD_params/upper_radius/wkr_new.dat",
               B_list=B_list),
    # Radius of lower QD
    Simulation(Options(), projectname="QDdownvar",
               n_list=[13]+[i for i in range(1, 13)],
               output_filename="QD_params/lower_radius/wkr_new.dat",
               B_list=B_list),
    # QDs height
    Simulation(Options(), projectname="diffD",
               n_list=[i for i in range(2, 20)],
               output_filename="QD_params/height/wkr_new.dat",
               B_list=B_list),
    # QDs radius
    Simulation(Options(), projectname="diffR",
               n_list=[i for i in range(1, 26)],
               output_filename="QD_params/radius/wkr_new.dat",
               B_list=B_list),
]

sims = (Zielinski + anti_gfactor + gfactor)