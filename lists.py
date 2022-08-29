from numpy import linspace, logspace, cos, sin, pi, array, log10

from common import sqrt2, gen_Elist, gen_Blist_multiple


# List of magnetic fields
B_list = [
    (0.0, 0.0, 1.0),
    (1 / sqrt2, 1 / sqrt2, 0.0),
]

B_list_001 = [
    (0.0, 0.0, 1.0),
    (0.0, 0.0, 1e-4),
]

B_list_110 = [
    (1 / sqrt2, 1 / sqrt2, 0.0),
    (1e-4 / sqrt2, 1e-4 / sqrt2, 0.0),
]

B_list_extended = [
    (0.0, 0.0, 1.0),
    (1.0, 0.0, 0.0),
    (1 / sqrt2, 1 / sqrt2, 0.0),
    (0.0, 1.0, 0.0),
    (-1 / sqrt2, 1 / sqrt2, 0.0),
]

B_list_log_inplane = gen_Blist_multiple(list(logspace(-4, 1, 1+5*2**2)) + list(logspace(-1, 1, 1+2*2**3)) + list(logspace(-0.5, 1, 1+1.5*2**4)) + list(logspace(0.75, 1, 1+0.25*2**5))
                                        # + list(linspace(0.5, 10, 20))
                                        + list(logspace(1.0, 1.25, 1+0.25*2**5))
                                        + [0.5835, 7.09272]
                                        , ["110"])
B_list_log_inplane_100 = gen_Blist_multiple(list(logspace(-4, 1, 1+5*2**2)) + list(logspace(-1, 1, 1+2*2**3)) + list(logspace(-0.5, 1, 1+1.5*2**4)) + list(logspace(0.75, 1, 1+0.25*2**5)), ["110"])
B_list_log_z = gen_Blist_multiple(list(logspace(-4, 1, 1+5*2**2)) + list(logspace(-1, 1, 1+2*2**3)) + list(logspace(-0.5, 1, 1+1.5*2**4)) + list(logspace(0.75, 1, 1+0.25*2**5))
                                # + list(logspace(0, 1, 9))
                                  , ["001"])
B_list_symm_log = gen_Blist_multiple(list(logspace(-4, 1, 1+5*2**2)) + list(logspace(-0.5, 1, 1+1.5*2**3)) + list(logspace(0.625, 1, 1+0.375*2**4))
                                    #  + list(logspace(0, 1, 9))
                                     , ["001", "110"])

in_plane_E_110 = gen_Elist(list(linspace(-0.5,3.0,36)) +
    [0.05, -0.05, 0.0005, -0.0005,
    5.4305800795127e-01, 1.0854683060910, 1.0856302335439, 1.0857921609968, 1.0859540884496, 1.0861160159025, 1.6291740238538] +
    list(linspace(3.0, 10.0, 15)) + list(linspace(3.0, 5.0, 9))
    ,"110")

in_plane_E_100 = gen_Elist(list(linspace(0.0, 10.0, 21)) + list(linspace(0.0, 2.0, 41)) +
                           list(linspace(3.0, 4.0, 11)) + list(linspace(6.5, 7.0, 6)) + [1.525, 6.825, 6.831, 6.834, 6.835, 6.836, 6.837, 6.85, 8.6, 8.7, 8.75, 8.753, 8.756, 8.762, 8.775, 8.8],"100")

in_plane_E_010 = gen_Elist(list(linspace(0.0, 10.0, 11)), "010")

in_plane_E_m110 = gen_Elist(list(linspace(0.0, 10.0, 11)) + list(linspace(0.0, 5.0, 21)) + [0.125, 0.375, 1.75, 5.75, 6.06, 6.125, 6.19, 6.25, 6.312, 6.343, 6.359, 6.367, 6.371, 6.373, 6.375, 6.44, 6.5, 6.57, 6.625, 6.75, 6.875]
    , "m110")

E_compensation110 = gen_Elist(list(linspace(-1.0, 0.0, 11)) +
                              [-0.545, -0.52, -0.54, -5.4602785643225e-01, -5.3655262556435e-01, -5.3329993437089e-01, -5.3202714216476e-01, -5.3188572080852e-01, -5.3174429945228e-01, -5.3047150724615e-01, -5.2721881605269e-01, -5.1774358518479e-01]
                              ,"110")
E_compensation100 = gen_Elist(list(linspace(-0.6, 0.5, 23)) + list(linspace(-0.1, 0.3, 17)),"100")
E_compensation110_high = gen_Elist(list(linspace(-5.0, 0.0, 11)) + list(linspace(-3.155, -3.15, 6)) + list(linspace(-3.7, -2.7, 21)) + 
    [3.1531046257704682, -2.6, -2.7, -3.14, -3.145, -3.153107312885234, -3.1531086564425768, -3.1531046257704682, -3.15311, -3.15322, -3.16, -3.165]
    ,"110")

E_elong100_comp_E110_B001 = gen_Elist(list(linspace(0.0, 4.0, 17)) + list(linspace(0.0, 2.0, 17)), "110")
E_elong100_comp_E100_B001 = gen_Elist(list(linspace(0.0, 4.0, 17)) + list(linspace(0.0, 2.0, 17)), "100")
E_elong100_comp_E110_B110 = gen_Elist(list(linspace(0.0, 4.0, 21)), "110")
E_elong100_comp_E100_B110 = gen_Elist(list(linspace(0.0, 4.0, 21)) + list(linspace(0.6, 0.7, 6)) + list(linspace(0.0, 0.9, 10)) + [0.05, 0.15, 0.25, 0.55, 1.7, 1.85, 1.9, 1.95, 2.05, 2.1],"100")
E_elong100_comp_E110_B100 = gen_Elist(list(linspace(0.0, 4.0, 21)) + list(linspace(1.0, 1.5, 3)), "110")
E_elong100_comp_E100_B100 = gen_Elist(list(linspace(0.0, 4.0, 21)) + list(linspace(0.0, 0.6, 7)) + [0.025, 0.05, 0.075, 0.15, 0.25, 1.25, 1.3, 1.35, 1.45, 1.5, 2.1, 2.15], "100")

# E_elong110_comp_E100_B100 = gen_Elist(list(linspace(-4.0, 4.0, 9)), "100")[::-1]
# E_elong110_comp_E110_B100 = gen_Elist(list(linspace(-4.0, 4.0, 9)), "110")[::-1]

B_list_gtensor = [(cos(phi) * sin(theta),
                   sin(phi) * sin(theta),
                   cos(theta))
                  for theta in sorted(set(linspace(0, pi, 9)[1:-1])
                                      | {pi/16, pi*15/16})
                  for phi in linspace(0, pi, 9)[:-1]
                  ] + [(0., 0., 1.), (0., 0., -1.)]
B_list_gtensor = array(B_list_gtensor)

B_list_gtensor_xz = array([(sin(phi)/sqrt2, sin(phi)/sqrt2, cos(phi)) for phi in linspace(0, pi, 65)])
B_list_gtensor_yz = array([(-sin(phi)/sqrt2, sin(phi)/sqrt2, cos(phi)) for phi in linspace(0, pi, 65)])
B_list_gtensor_x = array([(sin(phi), 0.0, cos(phi)) for phi in linspace(0, pi, 65)])
B_list_gtensor_y = array([(0.0, sin(phi), cos(phi)) for phi in linspace(0, pi, 65)])
B_list_gtensor_xy = array([(cos(phi), sin(phi), 0.0) for phi in linspace(0, pi, 65)])

n_list_rotate = [ # degrees
    27, 1, 2, 3, 4, 5, 6,  # -5-25
    20, 17, 26, 24, 25, 7, 18, 19,  # 28, 29, 29.0554, 29.0588, 29.1176, 30, 31, 32
    16, 28, 8, 29, 15, 30, 9,  # 32.5, 33.75, 35, 36.25, 37.5, 38.75, 40
    11, 12, 13, 14, #41-44
    10, #45
    # 21, 22, 23, #50-65
    ]
n_list_rotate_shift = [1,2,3,4,17,23,5,24,18,25,6,26,19,27,7,28,20,29,8,30,21,31,9,32,22,34,33,35,10]
n_list_elong100 = [1,19,2,20,3,21,4,22,5,23,6] + [13] + [i for i in range(7, 12)] + [i for i in range(14, 19)]
n_list_elong110 = [1,17,2,18,3,19,4,20,5,21,6] + [i for i in range(7, 17)]
