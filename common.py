import numpy as np
from os import system, popen

# Constants
mu = 5.7883818012e-5  # Bohr magneton in appropriate units
sqrt2 = 2.0**0.5  # √2


def ϕ(error):
    ϕ = (np.sqrt(5.0) - 1.0) / 2.0  # Golden ratio - 1, ≈0.618
    error = error**2
    return ϕ if error == 1.0 else (error + ϕ * (1.0 - error))


# Width of a screen calculations are conducted on, defaults to 102 characters,
# so that there are 100 pixels of useful space
def screen_w():
    data = popen('stty size', 'r').read().split()
    # If readout is successful return number of columns
    if data:
        rows, columns = popen('stty size', 'r').read().split()
        return int(columns)
    # Otherwise return default number
    else:
        return 102


# Compile psi to make sure it is the recent version
def make_psi():
    echo("Compiling psi")
    system("make psi")


# Check is variables are "close"
def close(x, y, eps=1e-8):
    return abs(x - y) < eps


def B_direction(B):
    if B[0] == 0 and B[1] == 0:
        return "[001]"
    elif B[0] == 1:
        return "[100]"
    elif B[1] == 1:
        return "[010]"
    elif B[0] > 0:
        return "[110]"
    elif B[0] < 0:
        return "[-110]"
    # assert False, "Wrong magnetic field direction!"
    return ""


# "Sign" of a field to allow for plotting data in arbitrary direction
def field_sign(B):
    if B[1] > 0:
        return 1
    if B[0] == 1.0:
        return 1
    return -1


def sort_and_remove_dupl(X):
    return sorted(list(set(X)))


def inplane_vector_from_angle(alpha):
    alpha = np.deg2rad(alpha)
    return (np.cos(alpha), np.sin(alpha), 0.0)


##############################################################################
#                                   Output                                   #
##############################################################################


# Print message to the terminal
def echo(message):
    system("echo " + str(message))


# Print screen-wide line of a given sign
def echo_nice_line(sign="*"):
    assert len(sign) == 1
    echo(encase(sign * screen_w()))


# Encase message in quotation marks
def encase(message):
    return '"' + str(message) + '"'


# Output number as a percentile
def percent(x, dec_places=5):
    return str(round(x * 100, dec_places)) + "%"


# Clear output file
def clear_output_file(filename):
    with open(filename, 'w') as file:
        file.write("")


def psi_safeguard():
    system("python calc/psi_safeguard.py & disown")


def psi_release():
    system("killall python")


def str_to_complex(number):
    number = number[1:-1].split(",")
    return float(number[0]) + 1j*float(number[1])

##################
# List utilities #
##################


def gen_Elist(input, dir):
    input = sort_and_remove_dupl(input)
    if dir == "110":
        return [(i/sqrt2, i/sqrt2) for i in input]
    elif dir == "100":
        return [(i, 0.0) for i in input]
    elif dir == "010":
        return [(0.0, i) for i in input]
    elif dir == "m110":
        return [(-i/sqrt2, i/sqrt2) for i in input]
    else:
        assert False, "Bad dir in gen_Elist"


def gen_Blist(input, dir):
    input = sort_and_remove_dupl(input)
    if dir == "110":
        return [(i/sqrt2, i/sqrt2, 0.0) for i in input]
    elif dir == "100":
        return [(i, 0.0, 0.0) for i in input]
    elif dir == "010":
        return [(0.0, i, 0.0) for i in input]
    elif dir == "m110":
        return [(-i/sqrt2, i/sqrt2, 0.0) for i in input]
    elif dir == "001":
        return [(0.0, 0.0, i) for i in input]
    else:
        assert False, "Bad dir in gen_Blist"


def gen_Blist_multiple(input, dirs):
    input = sort_and_remove_dupl(input)
    B_lists = [gen_Blist(input, dir) for dir in dirs]
    return sum([list(x) for x in zip(*B_lists)], [])


def sort_and_remove_dupl(X):
    X = sorted(list(set(X)))
    i = 1
    while i < len(X):
        if close(X[i], X[i-1]):
            X.pop(i)
        else:
            i += 1
    return X
