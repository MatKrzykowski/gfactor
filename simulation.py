from itertools import product

from calculation import Calculation
from common import clear_output_file, B_direction, echo
from output import write_to_file, write_to_file_unsorted, write_info_minimum, \
    write_info_ranges, write_info_gfactor, write_info_piezo, \
    write_fitting_points, write_gtensor
from psi import Psi
from structure import Structure


# Class for the entire simulation
class Simulation():
    def __init__(self, options,
                 projectname="QD",  # Name of the project for kp calculations
                 n_list=[1],  # Structure number list
                 in_plane_E_list=[(0., 0.)],  # In-plane electric field list
                 B_list=[(0., 0., 1.)],  # External magnetic field list
                 output_filename="wkr_new.dat",  # Output file name
                 read_special=True  # Check to avoid recursive behavior
                 ):

        # Assign variables
        self.options = options
        self.projectname = projectname
        self.n_list = n_list
        self.in_plane_E_list = in_plane_E_list
        self.B_list = B_list

        output_filename = "data/" + output_filename
        self.output_filename = output_filename
        self.unsorted_filename = output_filename.replace("new", "unsorted")
        self.minimum_filename = output_filename.replace("wkr_new", "minimum{}")
        self.ranges_filename = output_filename.replace("wkr_new", "ranges{}")
        self.gfactor_filename = output_filename.replace("wkr_new", "gfactor{}")
        self.piezo_filename = output_filename.replace("wkr_new", "piezo{}")
        self.B_fit_filename = output_filename.replace("wkr_new", "fit_data")
        self.B_gtensor_filename = output_filename.replace("wkr_new", "gtensor")

        # Assign structures list
        self.structures = self.generate_structures

        # Number of calculations read, used to avoid reading same data
        # multiple times, starts at 0
        self.n_calc = 0

        # Read data from the files
        self.read_files()
        if self.options.read_special_cases and read_special:
            self.read_special_cases()
        self.read_additional()
        if "gtensor" in self.output_filename:
            self.read_coeffs()

    # Generate structures for given parameter lists
    @property
    def generate_structures(self):
        structures = []
        # for B, n, E in product(self.B_list, self.n_list, self.in_plane_E_list):
        # for n, B, E in product(self.n_list, self.B_list, self.in_plane_E_list):
        for n, E, B in product(self.n_list, self.in_plane_E_list, self.B_list):
            structures.append(Structure(self, n, E, B))
        # Assign previous struct to the struct
        for i, struct in enumerate(structures):
            struct.sim = self
            if i > 0:
                struct.previous = structures[i - 1]
            if i > 1:
                struct.previous2 = structures[i - 2]
            if i > 2:
                struct.previous3 = structures[i - 3]
        # Assign next struct to the struct
        structs_reverse = structures[::-1]
        for i, struct in enumerate(structs_reverse):
            if i > 0:
                struct.next = structs_reverse[i - 1]
            if i > 1:
                struct.next2 = structs_reverse[i - 2]
            if i > 2:
                struct.next3 = structs_reverse[i - 3]
        return structures

    ###########################################################################
    #                              Data readout                               #
    ###########################################################################

    # Directory where results are being stored
    @property
    def results_dir(self):
        if self.options.Polaron:
            result = "/home/mkrzykow/Storage"
        else:
            # result = "/home/mkrzykow/polaronStorage"
            result = "/home/mateusz/PolaronStorage"
        result += "/{}/results/".format(self.options.kp_dir)

        return result + self.projectname + "/WaveFuns/"

    # Name of the local file
    @property
    def local_filename(self):
        return self.results_dir + "local.dat"

    # Name of the wkr_single file
    @property
    def wkr_filename(self):
        return self.results_dir + "wkr_single.dat"

    @property
    def additional_filename(self):
        return self.results_dir + "various.dat"

    @property
    def coeffs_filename(self):
        return self.results_dir + "coeffs.dat"

    # Read data from the files
    def read_files(self):
        i = 0  # Current line index
        # Open input files
        with open(self.wkr_filename) as file_wkr:
            with open(self.local_filename) as file_local:
                # Loop over input files lines
                for line_wkr, line_local in zip(file_wkr, file_local):
                    i += 1
                    # Update only if there is new data
                    if i > self.n_calc:
                        # Add new calculation to appropriate structure
                        calc = Calculation(line_wkr, line_local)
                        self.add_to_structures(calc)

                # Update number of read lines
                self.n_calc = i

        # Do a single calculation is no files to read from
        if i == 0:
            Psi(self.structures[0]).run()

        # Clean-up after data readout
        self.clean_up()

    def read_additional(self):
        try:
            with open(self.additional_filename) as file:
                for line in file:
                    n_calc = int(line.split()[-1])
                    n_str = int(line.split()[-2])
                    for struct in self.structures:
                        for calc in struct.calcs:
                            if calc.n_calc == n_calc and calc.n_str == n_str:
                                calc.add_additional(line)
                                struct.additional = calc
        except FileNotFoundError:
            echo("There is no file with additional data in "
                 + self.projectname)

    def read_coeffs(self):
        try:
            with open(self.coeffs_filename) as file:
                for line in file:
                    n_calc = int(line.split()[-1])
                    n_str = int(line.split()[-2])
                    for struct in self.structures:
                        for calc in struct.calcs:
                            if calc.n_calc == n_calc and calc.n_str == n_str:
                                calc.add_coeffs(line)
        except FileNotFoundError:
            echo("There is no file with coefficients in "
                 + self.projectname)

    # Read special cases of the same structures in different projects
    def read_special_cases(self):
        # Dictionary of repeated structures
        special = {
            "E_field": [1, (0.0, 0.0)],
            "diffc": [5, (0.0, 0.0)],
            "shift100": [1, (0.0, 0.0)],
            "shift110": [1, (0.0, 0.0)],
            "QDtopvar": [7, (0.0, 0.0)],
            "QDdownvar": [6, (0.0, 0.0)]
        }
        # If all requirements are met
        if self.projectname in special.keys():
            for key in special.keys():
                if key != self.projectname:
                    for struct in self.structures:
                        if (struct.n_str == special[self.projectname][0] and
                                struct.E_xy == special[self.projectname][1]):
                            # Create simulation to read data
                            sim = Simulation(self.options,
                                             projectname=key,
                                             n_list=[special[key][0]],
                                             in_plane_E_list=[struct.E_xy],
                                             B_list=[struct.B],
                                             read_special=False)
                            # Copy the data to the structure object
                            for calc in sim.structures[0].calcs:
                                struct.calcs.append(calc)
        # Clean up after the reading
        self.clean_up()

    # Add new calculation to appropriate structure
    def add_to_structures(self, calc):
        for struct in self.structures:
            if struct.calc_belongs(calc):
                struct.calcs.append(calc)
                calc.struct = struct
                break  # Break as the structure has been found

    ##########################################################################
    #                            Data generation                             #
    ##########################################################################

    # Generate inner bounds
    def gen_various(self):
        for struct in self.structures:
            struct.gen_various()

    # Generate inner bounds
    def gen_minimas(self):
        for struct in self.structures:
            struct.gen_minimas()

    # Fill blank spaces
    def fill_blanks(self, outer=True):
        for struct in self.structures:
            struct.fill_blanks(outer)

    # Generate required minimum
    def gen_left_outer(self):
        for struct in self.structures:
            struct.calc_bounds(outer=True, left=True, right=False)

    # Generate required minimum
    def gen_required(self):
        for struct in self.structures:
            struct.calc_based_on_previous()
            struct.calc_bounds(outer=True)
            struct.calc_bounds(outer=False)
            if not struct.has_minimum:
                struct.fill_blanks(outer=False)
            struct.gen_minimas()
            struct.calc_right()
            if self.options.fill_blanks_limit < 0.5:
                struct.fill_blanks(outer=False)
                struct.fill_blanks_near_anticrossing()
                struct.fill_blanks_near_anticrossing()
                struct.fill_blanks_near_anticrossing()
                struct.fill_blanks_near_anticrossing()
                struct.fill_blanks_near_anticrossing()
                # struct.fill_blanks(outer=True)

    # Generate additional data
    def continue_generating(self):
        for struct in self.structures:
            struct.calc_based_on_previous()
            # Increase limits to make sure they are met
            struct.limits[0] -= 1
            struct.limits[1] += 1
            # Look for minimas in the entire range
            struct.gen_minimas(outer=False)
            # Do calculations for the inner range
            struct.calc_bounds(outer=False, left=False)
            struct.calc_bounds(outer=False, right=False)
            struct.fill_blanks(outer=False)
            # Do calculations for the outer range
            struct.calc_bounds(outer=True, left=False)
            struct.calc_bounds(outer=True, right=False)
            struct.fill_blanks(outer=True)
            # Look for minimas in the entire range again
            struct.gen_minimas(outer=False)

    ###########################################################################
    #                                Clean up                                 #
    ###########################################################################

    # One method to do all clean up procedures
    def clean_up(self):
        self.sort_structures()  # Sorting data
        self.remove_repeats()  # Removing repeated entries
        self.update_limits()  # Updating limits
        self.update_ranges()  # Updating ranges
        self.update_minimum()  # Updating ranges

    # Sort structures by the Ez of their calculations
    def sort_structures(self):
        for struct in self.structures:
            struct.sort_per_Ez()

    # Update limits
    def update_limits(self):
        for struct in self.structures:
            struct.update_limits()

    # Update inner and outer ranges
    def update_ranges(self):
        for struct in self.structures:
            struct.update_ranges()

    # Remove repeated entries
    def remove_repeats(self):
        for struct in self.structures:
            struct.remove_repeats()

    # Update minimum information
    def update_minimum(self):
        for struct in self.structures:
            struct.update_minimum()

    ###########################################################################
    #                            Output and infos                             #
    ###########################################################################

    # Write data to the file
    def write_to_file(self, filename=""):
        # If not provided use default filename
        if filename == "":
            filename = self.output_filename

        # Clear the output file
        clear_output_file(filename)

        # Loop over all structures
        for struct in self.structures:
            write_to_file(struct, filename)

    # Write data to the file
    def write_to_file_unsorted_sim(self):
        filename = self.unsorted_filename

        # Clear the output file
        clear_output_file(filename)

        # Loop over all structures
        for struct in self.structures:
            write_to_file_unsorted(struct, filename)

    @property
    def B_string_list(self):
        if "Brotate" in self.output_filename:
            return ["[110]"]
        else:
            return [B_direction(B) for B in self.B_list]

    # Write info about the minimum to the output file
    def write_minimum_info(self):
        for B in self.B_string_list:
            clear_output_file(self.minimum_filename.format(B))
        for struct in self.structures:
            write_info_minimum(struct, self.minimum_filename)

    # Write info about the minimum to the output file
    def write_ranges_info(self):
        for B in self.B_string_list:
            clear_output_file(self.ranges_filename.format(B))
        for struct in self.structures:
            write_info_ranges(struct, self.ranges_filename)

    # Write info about the minimum to the output file
    def write_gfactor_info(self):
        for B in self.B_string_list:
            clear_output_file(self.gfactor_filename.format(B))
        for struct in self.structures:
            write_info_gfactor(struct, self.gfactor_filename)

    # Write info about the minimum to the output file
    def write_piezo_info(self):
        for B in self.B_string_list:
            clear_output_file(self.piezo_filename.format(B))
        for struct in self.structures:
            if struct.additional is not None:
                write_info_piezo(struct, self.piezo_filename)    

    def write_fitting_points(self):
        write_fitting_points(self, self.B_fit_filename)

    def write_gtensor(self):
        write_gtensor(self, self.B_gtensor_filename)

    @property
    def n(self):
        return sum([struct.n for struct in self.structures])
