import numpy as np

from common import mu, str_to_complex


# Calculation class, meant to represent a single kp calculation
class Calculation():
    def __init__(self,
                 l_wkr,  # line containing information from wkr_single.dat
                 l_local  # line containing information about localization
                 ):
        # Split input data lines for further analysis
        l_wkr = l_wkr.split()
        l_local = l_local.split()

        # Save external electric and magnetic fields
        self.E = [float(l_wkr[i]) for i in range(3)]
        self.B = [float(l_wkr[i]) for i in range(3, 6)]

        # Save structure and calculation numbers
        self.n_str, self.n_calc = int(l_wkr[-2]), int(l_wkr[-1])

        # Number of states calculated, should always be 4 for now
        nev = (len(l_wkr) - 14) // 3
        self.nev = nev
        assert self.nev == 4, "Number of states is not equal 4"

        # Save energies as well as orbital and spin angular momenta
        self.energy = [float(l_wkr[i]) for i in range(6, 6 + nev)]
        self.J_z = [float(l_wkr[i]) for i in range(6 + nev, 6 + nev * 2)]
        self.S_z = [float(l_wkr[i]) for i in range(6 + nev * 2, 6 + nev * 3)]

        # Continuous and discrete localization
        self.local = [float(l_local[i]) for i in range(6, 6 + nev)]
        self.discrete_local = [int(2 * i) for i in self.local]

        # Assert to check that readout form wkr_single and local is consistant
        assert self.n_str == int(l_local[-2]), str([self.n_str, self.n_calc])
        assert self.n_calc == int(l_local[-1]), str([self.n_str, self.n_calc])

        # Placeholder for additional data
        self.struct = None
        self.piezo = None
        self.spin_inplane = None
        self.g_inplane_sign = None

    # Define < operator to be able to sort calculations
    def __lt__(self, other):
        return self.E_z < other.E_z

    ##########################################################################
    #                                 Fields                                 #
    ##########################################################################

    # E-field in z direction for convinience
    @property
    def E_z(self):
        return self.E[2]

    # B-field in z direction for convinience
    @property
    def B_z(self):
        return self.B[2]

    # B-field value
    @property
    def B_value(self):
        return np.linalg.norm(self.B)

    ##########################################################################
    #                              Localization                              #
    ##########################################################################

    # Localization of the lower pair of states
    @property
    def local_low(self):
        return (self.local[0] + self.local[1]) / 2

    # Localization of the upper pair of states
    @property
    def local_up(self):
        return (self.local[2] + self.local[3]) / 2

    ##########################################################################
    #                              Anticrossing                              #
    ##########################################################################

    # Energy splitting between two lowest states
    @property
    def anti(self):
        return (self.energy[1] - self.energy[0])

    @property
    def anti_signed(self):
        bias = 1e-5
        # return self.anti * np.sign(self.S_z[0])
        return self.anti * np.sign(self.S_z[0] - self.S_z[1] + bias)

    ###########################################################################
    #                             Fitting utility                             #
    ###########################################################################

    # Coordinates of the point representing the calculation in 2D for fitting
    @property
    def point(self):
        return (self.E_z, self.anti)

    ##########################################################################
    #                                g-factor                                #
    ##########################################################################

    # g-factor of the dublet in the lower QD
    @property
    def g_low(self):
        E = self.energies_in_localization_order
        return (E[1] - E[0]) / mu / self.B_value

    # g-factor of the dublet in the upper QD
    @property
    def g_up(self):
        E = self.energies_in_localization_order
        return (E[3] - E[2]) / mu / self.B_value

    ##########################################################################
    #                             Output utility                             #
    ##########################################################################

    # Check if this calculation should be written in the output file
    @property
    def to_be_written(self):
        # 2 out of 4 states must be localized in the upper QD
        return sum(self.discrete_local) == 2

    # Segregate and return energies in desired order
    @property
    def energies_in_localization_order(self):
        return self.swap(self.energy)

    ###########################################################################
    #                          Swapping within lists                          #
    ###########################################################################

    def do_swap(self, i, n):
        # Out-of-plane magnetic field case
        if self.B_z == 1.0:
            # Swap if spin is the other way around
            if self.S_z[i] < 0:
                return True
        # In-plane magnetic field case
        else:
            # There must be additional information to be provided
            if self.struct.additional is not None:
                # Swap if g-factor sign is negative
                if self.struct.additional.g_inplane_sign[n] < 0:
                    return True
        # In any other case do not swap
        return False

    # Segregate and return energies in desired order
    # After the swap the order should be: lower down and up, upper down and up
    def swap(self, old_list):
        new_list = []
        # Loop over possible localizations
        for n in [0, 1]:
            # Loop over discrete localization values
            for i, d_local in enumerate(self.discrete_local):
                # If localizations match
                if d_local == n:
                    # Increase new list and check if 2 new were added
                    new_list.append(old_list[i])
                    if len(new_list) == 2 * (n + 1):
                        # Swap these 2 new if needed
                        if self.do_swap(i, n):
                            new_list[2 * n], new_list[2 * n + 1] = \
                                new_list[2 * n + 1], new_list[2 * n]
        # Return the new list
        return new_list

    ##########################################################################
    #                         Additional information                         #
    ##########################################################################

    # Add additional information if available
    def add_additional(self,
                       line  # String containing additional information
                       ):
        # Split the line for further analysis
        line = line.split()
        # Save information about piezo and in-plane g-factor
        # self.piezo = [float(i) for i in line[6:10]]
        # self.piezo = self.swap(self.piezo)
        # self.spin_inplane = [float(i) for i in line[10:14]]
        self.piezo = [[float(i) for i in line[6 + 4 * j:10 + 4 * j]]
                      for j in range(8)]
        for i in range(8):
            self.piezo[i] = self.swap(self.piezo[i])
        self.spin_inplane = [float(i) for i in line[38:42]]
        # Sort spin into localizations
        spin_inplane_sorted = [[], []]
        for spin, local in zip(self.spin_inplane, self.discrete_local):
            spin_inplane_sorted[local].append(spin)
        # Determine g-factor sign for a given localization
        self.g_inplane_sign = []
        for i in [0, 1]:
            if spin_inplane_sorted[i][0] < spin_inplane_sorted[i][1]:
                self.g_inplane_sign.append(1.0)
            else:
                self.g_inplane_sign.append(-1.0)

    # Add additional information if available
    def add_coeffs(self,
                   line  # String containing additional information
                   ):
        # Split the line for further analysis
        line = line.split()
        coeffs = np.array([[str_to_complex(line[6+i*4+j])
                            for j in range(4)] for i in range(8)])
        coeffs_up = coeffs[2, :]
        coeffs_down = coeffs[5, :]
        self.struct.coeffs = np.array([[coeffs_up[0], coeffs_down[0]],
                                       [coeffs_up[2], coeffs_down[2]]])

    @property
    def in_range(self):
        if self.struct.sim.options.restrict_unsorted:
            return self.struct.in_range(self.E_z, outer=False)
        else:
            return self.struct.in_range(self.E_z, outer=True)
