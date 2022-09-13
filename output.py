from os import system

from common import mu

int_str = "{:2d}\t"
sci_str = "{:20.13e}\t"


# Write new line symbol to the file
def new_line(file):
    file.write("\n")


# Data from the calculation to be written in the output file
def write_line(calc):
    line = []  # Initialize empty list of strings, to be merged later

    # Append E-field and B-field
    line += [sci_str.format(E) for E in calc.E]
    line += [sci_str.format(B) for B in calc.B]

    # Append energies in order due to localization
    line += [sci_str.format(E) for E in calc.energies_in_localization_order]

    # Append structure number
    line += [int_str.format(calc.n_str)]

    # Add end line character
    line += ["\n"]

    return "".join(line)


# Data from the calculation to be written in the output file
def write_line_unsorted(calc):
    line = []  # Initialize empty list of strings, to be merged later

    # Append E-field and B-field
    line += [sci_str.format(E) for E in calc.E]
    line += [sci_str.format(B) for B in calc.B]

    # Append energies in order due to localization
    line += [sci_str.format(E) for E in calc.energy]

    # Append localizations
    line += [sci_str.format(local) for local in calc.local]

    # Append localizations
    line += [sci_str.format(spin) for spin in calc.S_z]

    # Append structure number
    line += [int_str.format(calc.n_str)]

    # Add end line character
    line += ["\n"]

    return "".join(line)


# Write structure records to the output file
def write_to_file(struct, filename):
    # Append to the given file all allegible records
    with open(filename, 'a') as file:
        for calc in struct.calcs:
            if calc.to_be_written:
                file.write(write_line(calc))
        file.write("\n\n")  # Adhere to gnuplot standard


# Write structure records to the output file
def write_to_file_unsorted(struct, filename):
    # Append to the given file all allegible records
    with open(filename, 'a') as file:
        for calc in struct.calcs:
            # if calc.in_range:
            file.write(write_line_unsorted(calc))
            # if struct.projectname == "E_field":
            #     print(calc.n_calc)
        file.write("\n\n")  # Adhere to gnuplot standard


def write_info_minimum(struct, filename):
    # Append to the given file
    filename = filename.format(struct.B_direction)
    with open(filename, 'a') as file:
        if struct.has_minimum:
            file.write(int_str.format(struct.n_str) +
                       sci_str.format(struct.E_x) +
                       sci_str.format(struct.E_y) +
                       sci_str.format(struct.x_axis) +
                       sci_str.format(struct.minimum.E_z) +
                       sci_str.format(struct.minimum.anti_signed) +
                       sci_str.format(struct.minimum.anti / (struct.minimum.B_value * mu)) +
                       sci_str.format(struct.minimum.local[0]) +
                       sci_str.format(struct.minimum.local[1]) +
                       sci_str.format(struct.minimum.S_z[0]) +
                       sci_str.format(struct.minimum.S_z[1]) +
                       sci_str.format(struct.minimum.S_z[2]) +
                       sci_str.format(struct.minimum.S_z[3]) +
                       str(struct.gfactors_sign_diff)
                       )
            new_line(file)


def write_info_ranges(struct, filename):
    # Append to the given file
    filename = filename.format(struct.B_direction)
    with open(filename, 'a') as file:
        left_outer, right_outer = struct.outer_range
        left_inner, right_inner = struct.inner_range
        file.write(int_str.format(struct.n_str) +
                   sci_str.format(struct.E_x) +
                   sci_str.format(struct.E_y) +
                   sci_str.format(struct.x_axis) +
                   sci_str.format(left_outer) +
                   sci_str.format(left_inner) +
                   sci_str.format(right_inner) +
                   sci_str.format(right_outer)
                   )
        new_line(file)


def write_info_gfactor(struct, filename):
    # Append to the given file
    filename = filename.format(struct.B_direction)
    if struct.gfactors[0] is None:
        return None
    with open(filename, 'a') as file:
        file.write(int_str.format(struct.n_str) +
                   sci_str.format(struct.E_x) +
                   sci_str.format(struct.E_y) +
                   sci_str.format(struct.x_axis) +
                   sci_str.format(struct.gfactors[0]) +
                   sci_str.format(struct.gfactors[1])
                   )
        new_line(file)


def write_info_piezo(struct, filename):
    # Append to the given file
    filename = filename.format(struct.B_direction)
    with open(filename, 'a') as file:
        piezo_str = ""
        for i in range(8):
            for j in range(4):
                piezo_str += sci_str.format(struct.piezo[i][j])
        for j in range(4):
            result = 0
            for i in range(8):
                result += struct.piezo[i][j]
            piezo_str += sci_str.format(result)
        file.write(int_str.format(struct.n_str) +
                   sci_str.format(struct.E_x) +
                   sci_str.format(struct.E_y) +
                   sci_str.format(struct.x_axis) +
                   sci_str.format(struct.additional.E_z) +
                   piezo_str
                   )
        new_line(file)


def write_fitting_points(sim, filename):
    if "B_field_gfactor" not in sim.output_filename:
        return None
    with open(filename, "w") as file:
        for struct in sim.structures:
            for calc in struct.calcs:
                if struct.in_range_exclusive(calc.E_z, outer=True):
                    file.write(sci_str.format(struct.x_axis) +
                               sci_str.format(calc.E_z) +
                               sci_str.format(calc.energy[0]) +
                               sci_str.format(calc.energy[1]) +
                               sci_str.format(calc.energy[2]) +
                               sci_str.format(calc.energy[3])
                               )
                    new_line(file)


def write_gtensor(sim, filename):
    with open(filename, "w") as file:
        for struct in sim.structures:
            if struct.gfactors[0] is not None:
                file.write(int_str.format(struct.n_str) +
                           sci_str.format(struct.B_x) +
                           sci_str.format(struct.B_y) +
                           sci_str.format(struct.B_z) +
                           sci_str.format(struct.phi) +
                           sci_str.format(struct.theta) +
                           sci_str.format(struct.gfactors[0]) +
                           sci_str.format(struct.gfactors[1])
                           )
                if struct.coeffs is not None:
                    file.write(sci_str.format(struct.coeffs[0, 0]) +
                               sci_str.format(struct.coeffs[0, 1]) +
                               sci_str.format(struct.coeffs[1, 0]) +
                               sci_str.format(struct.coeffs[1, 1])
                               )
                new_line(file)


def copy_wkr(sim):
    for filename in ["wkr_single.dat", "local.dat", "various.dat"]:
        # new_filename = sim.output_filename.replace("wkr_new.dat", filename)
        new_filename = "wkr_backup/" + sim.projectname + "/" + filename
        system("cp ~/PolaronStorage/test/results/{}/WaveFuns/{} {}".format(
            sim.projectname, filename, new_filename))
