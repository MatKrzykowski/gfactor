from numpy import log2, ceil, sqrt, arccos, arctan2
from numpy.linalg import norm

from itertools import product

from common import close, encase, percent, ϕ
from common import echo, B_direction, inplane_vector_from_angle
from fit import para_min, fit_min
from psi import Psi


# Structure class representing calculations for given structure and fields
class Structure():
    # Initialize object
    def __init__(self, sim, n_str, E_xy, B):
        # Assign variables
        self.sim = sim  # Simulation object, needed to read files
        self.projectname = sim.projectname  # Project name
        self.options = sim.options  # Options object
        self.n_str = n_str  # Structure number
        self.E_xy = E_xy  # In-plane E-field list
        self.E_x = E_xy[0]  # E-field in x direction
        self.E_y = E_xy[1]  # E-field in y direction
        self.calcs = []  # Calculations list
        self.B = B  if "Brotate" not in self.sim.output_filename else inplane_vector_from_angle(self.angle) # Magnetic field tuple
        self.B_val = norm(B)  # Magnetic field tuple
        self.B_x = self.B[0]  # B-field in x direction
        self.B_y = self.B[1]  # B-field in y direction
        self.B_z = self.B[2]  # B-field in z direction
        # Min and max E-field considered for calculations
        self.limits = list(self.options.default_limits)
        self.B_direction = B_direction(self.B) if "Brotate" not in self.sim.output_filename else "[110]"
        self.additional = None
        self.coeffs = None
        self.minimum = None
        self.E_min_diff = None
        self.minimum_index = None

        # Previous structure in the list, may or may not be overwritten
        self.previous = None
        self.previous2 = None
        self.previous3 = None
        self.next = None
        self.next2 = None
        self.next3 = None

    ###########################################################################
    #                                   Ranges                                #
    ###########################################################################

    # Either outer or inner E-field range
    def E_range(self, outer=True, minimum=None):
        if minimum is not None:
            return self.minimum_range(minimum)
        else:
            return self.outer_range if outer else self.inner_range

    def minimum_range(self, minimum):
        left_border = minimum - self.options.minima_vicinity / 2.0
        right_border = minimum + self.options.minima_vicinity / 2.0
        left_list = [E for E in self.E_z_list if E <= left_border]
        right_list = [E for E in self.E_z_list if E >= right_border]
        if left_list and right_list:
            left = max(left_list)
            right = min(right_list)
            return (left, right)
        return None

    # Check if given E-field value is in range
    def in_range(self, E, outer=True, minimum=None):
        # This includes edge cases
        current_range = self.E_range(outer, minimum)
        return current_range[0] <= E <= current_range[1]

    # Check if given E-field value is in range
    def in_range_exclusive(self, E, outer=True, minimum=None):
        # This includes edge cases
        current_range = self.E_range(outer, minimum)
        return current_range[0] < E < current_range[1]

    # Return position within a range from 0 to 1, -1 if outside the range
    def pos_in_range(self, E, outer=True, minimum=None):
        if self.in_range(E, outer, minimum):
            distance_to_left = (E - self.E_range(outer, minimum)[0])
            return distance_to_left / self.span(outer, minimum)
        else:
            return -1

    # Inner and outer lengths of the ranges
    def span(self, outer=True, minimum=None):
        if minimum is None:
            return self.outer_span if outer else self.inner_span
        else:
            return self.minimum_span(minimum)

    @property
    def outer_span(self):
        return self.outer_range[1] - self.outer_range[0]

    @property
    def inner_span(self):
        return self.inner_range[1] - self.inner_range[0]

    def minimum_span(self, minimum):
        current_range = self.minimum_range(minimum)
        return current_range[1] - current_range[0]

    ###########################################################################
    #                             Gaps and bounds                             #
    ###########################################################################

    # Gap in Ez in percents, either maximum or at the bounds
    def gap(self, outer, maximum=False):
        E_list = self.E_list_in_range(outer)
        # If E_list empty return 100%
        if len(E_list) <= 1:
            return 1.0 if maximum else [1.0, 1.0]
        E_diff = self.E_diff_list_in_range(outer)
        # If maximum return largest gap
        if maximum:
            return max(E_diff) / self.span(outer)
        # Otherwise return gaps in the edges
        else:
            return E_diff[0] / self.span(outer), E_diff[-1] / self.span(outer)

    @property
    def right(self):
        span = self.outer_range[1] - self.inner_range[1] if self.options.gfactor_to_right else self.inner_range[0] - self.outer_range[0]
        if not span:
            return 1.0, 1.0
        if self.options.gfactor_to_right:
            span += self.E_diff_list_in_range(False)[-1]
            E_left = self.E_diff_list_in_range(False)[-1]
            E_right = self.E_diff_list_in_range(True)[-1]
        else:
            span += self.E_diff_list_in_range(False)[0]
            E_right = self.E_diff_list_in_range(False)[0]
            E_left = self.E_diff_list_in_range(True)[0]
        return E_left / span, E_right / span

    # E-field for calculations at the bounds
    def bound_E(self, i, outer, error=0):
        E_lists = self.E_diff_list_in_threshold(outer)
        if i == 0:
            return E_lists[0][0] + ϕ(error) * E_lists[0][1]
        elif i == 1:
            return E_lists[-1][0] + (1 - ϕ(error)) * E_lists[-1][1]

    # Precision of bounds calculation
    def bound_E_percent(self, i, outer):
        E_lists = self.E_diff_list_in_threshold(outer)
        if i == 0:
            return E_lists[0][1] / self.span(outer)
        elif i == 1:
            return E_lists[-1][1] / self.span(outer)

    ##########################################################################
    #                               E-field lists                            #
    ##########################################################################

    def E_boundary(self, outer=True, left=True):
        E_list = self.E_list_in_range(outer)
        if left:
            return [E_list[0], E_list[1]]
        else:
            return [E_list[-2], E_list[-1]]

    # List of all E-field values
    @property
    def E_z_list(self):
        result = [calc.E_z for calc in self.calcs]

        if result == []:
            result = [self.limits[0]] + result + [self.limits[1]]
        else:
            if self.limits[0] < result[0]:
                result = [self.limits[0]] + result
            if self.limits[1] > result[-1]:
                result = result + [self.limits[1]]

        return result

    # E-field list within a given range
    def E_list_in_range(self, outer):
        E_range = self.E_range(outer)
        return [i for i in self.E_z_list if E_range[0] <= i <= E_range[1]]

    # E-field differences list within a given range
    def E_diff_list_in_range(self, outer):
        E_list = self.E_list_in_range(outer)
        return [E_list[i] - E_list[i - 1] for i in range(1, len(E_list))]

    # E-field and their differences list within given range and threshold
    def E_diff_list_in_threshold(self, outer, threshold=0.0):
        E_list = self.E_list_in_range(outer)
        E_diff_list = self.E_diff_list_in_range(outer)
        return [(i, j) for i, j in zip(E_list, E_diff_list) if j >= threshold]

    ###########################################################################
    #                              Calculations                               #
    ###########################################################################

    # Calculate additional points in blank spaces
    def fill_blanks(self, outer=True):
        # Minimal size of blank space to be filled
        threshold = self.options.fill_blanks_limit * self.span(outer)

        # Loop over E-fields and differences within threshold
        for E, E_diff in self.E_diff_list_in_threshold(outer, threshold):
            # Number of points to fill the blank space
            n = int(E_diff / threshold)
            # Do calculations n times
            for j in range(n):
                Psi(self, outer=outer,
                    E_z=E + E_diff * (j + 1) / (n + 1),
                    eps_factor=self.eps_factor(outer),
                    message="Filling blanks in " + self.title(outer),
                    E_diff=E_diff / self.span(outer) / n,
                    error=self.options.fill_blanks_limit).run()

    # Calculate additional points in blank spaces
    def fill_blanks_near_anticrossing(self):
        # Minimal size of blank space to be filled
        threshold = self.options.fill_blanks_limit
        threshold *= self.span(outer=False, minimum=self.minimum.E_z)
        # Loop over E-fields and differences within threshold
        for E, E_diff in self.E_diff_list_in_threshold(False, threshold):
            if not self.in_range(E, outer=False, minimum=self.minimum.E_z):
                continue
            # Number of points to fill the blank space
            n = int(E_diff / threshold)
            # Do calculations n times
            for j in range(n):
                Psi(self, outer=False,
                    E_z=E + E_diff * (j + 1) / (n + 1),
                    eps_factor=self.eps_factor(False),
                    message="Filling blanks in " + self.title(False),
                    E_diff=E_diff / self.span(False) / n,
                    minimum=self.minimum.E_z,
                    error=self.options.fill_blanks_limit).run()

    # Calculate bounds, either outer or inner
    def calc_bounds(self, outer=True, left=True, right=True):
        # Counter checking which side to calcule: 0 - left, 1 - right
        bounds = self.gap(outer)
        i = 0 if bounds[0] > bounds[1] else 1
        if right and not left:
            i = 1
        if left and not right:
            i = 0

        bounds_factor = self.bounds_factor(outer, i)
        # Do calculations as long as bounds are too large
        while max(bounds) >= self.options.bound_limit / bounds_factor:
            # Text to be displayed
            side = "bounds to the right" if i % 2 else "bounds to the left"
            # Additional factor to account for possible change in ranges
            bounds_factor = self.bounds_factor(outer, i)

            # Do calculation if density of the points not big enough
            if bounds[i % 2] >= self.options.bound_limit / bounds_factor:
                error = self.options.bound_limit / bounds_factor
                E_diff = bounds[i % 2]
                Psi(self, outer=outer,
                    E_z=self.bound_E(i % 2, outer, E_diff),
                    eps_factor=self.eps_factor(outer),
                    E_diff=E_diff,
                    message="Generating " + self.title(outer) + " " + side,
                    error=error
                    ).run()
            # Else try the other side or stop calculation
            else:
                if left and right:
                    i += 1
                # Else break as we want only one side to be calculated
                else:
                    break
            # Update information about bounds
            bounds = self.gap(outer)

    def calc_right(self):
        bounds = self.right
        bounds_factor_left = self.bounds_right[0]
        bounds_factor_right = self.bounds_right[1]
        while bounds[1] >= self.options.right_limit / bounds_factor_right:
            bounds = self.right
            bounds_factor_right = self.bounds_right[1]
            message = "Fine filling right"
            if bounds[1] >= self.options.right_limit / bounds_factor_right:
                error = self.options.right_limit / bounds_factor_right
                E_diff = bounds[1]
                Psi(self, outer=True,
                    E_z=self.bound_E(1 if self.options.gfactor_to_right else 0, self.options.gfactor_to_right, E_diff),
                    eps_factor=self.eps_factor(self.options.gfactor_to_right),
                    E_diff=E_diff,
                    message=message,
                    error=error
                    ).run()
        while bounds[0] >= self.options.right_limit / bounds_factor_left:
            bounds = self.right
            bounds_factor_left = self.bounds_right[0]
            message = "Fine filling left"
            if bounds[0] >= self.options.right_limit / bounds_factor_left:
                error = self.options.right_limit / bounds_factor_left
                E_diff = bounds[0]
                Psi(self, outer=True,
                    E_z=self.bound_E(1 if self.options.gfactor_to_right else 0, not self.options.gfactor_to_right, E_diff),
                    eps_factor=self.eps_factor(not self.options.gfactor_to_right),
                    E_diff=E_diff,
                    message=message,
                    error=error
                    ).run()

    def calc_based_on_previous(self):
        for outer, left in product([True, False], [False, True]):
            message = "Generating {} based on previous".format(
                'outer' if outer else 'inner')
            for struct in [self.previous, self.next, self.previous2, self.next2, self.previous3, self.next3]:
                if struct is None:
                    continue
                for E in struct.E_boundary(outer, left)[::-1]:
                    i = 0 if left else 1
                    bounds = self.gap(outer)
                    bounds_factor = self.bounds_factor(outer, i)
                    if bounds[i] < self.options.bound_limit / bounds_factor:
                        continue
                    E_l, E_r = self.E_boundary(outer=outer, left=left)
                    if E_l < E < E_r:
                        Psi(self, outer,
                            E_z=E,
                            message=message,
                            E_diff=bounds[i],
                            eps_factor=self.eps_factor(outer),
                            error=self.options.bound_limit / bounds_factor
                            ).run()
        if self.options.calc_minima_from_previous and self.minimum is not None:
            for struct in [self.previous, self.next, self.previous2, self.next2, self.previous3, self.next3]:
                if struct is None:
                    continue
                if not struct.has_minimum:
                    continue
                if self.E_min_diff < self.options.minima_eps:
                    continue
                here_range = self.minimum_range(self.E_min)
                if here_range is None:
                    continue
                if here_range[0] < struct.E_min < here_range[1]:
                    if close(here_range[0], struct.E_min):
                        continue
                    if close(here_range[1], struct.E_min):
                        continue
                    if close(self.minimum.E_z, struct.E_min):
                        continue
                    Psi(self, outer,
                        E_z=struct.E_min,
                        E_diff=(here_range[1] - here_range[0]
                                ) / self.span(False),
                        message="Generating minima from previous",
                        eps_factor=self.options.eps_factor_for_minima,
                        minimum=None if outer else self.E_min,
                        error=self.options.minima_eps / self.span(outer)
                        ).run()

    def bounds_factor(self, outer, i):
        bounds = self.gap(outer)
        if bounds[0] != 1:
            return 1 / (1 - bounds[(i + 1) % 2])
        else:
            return 1.0

    @property
    def bounds_right(self):
        bounds = self.right
        if bounds[0] != 1:
            return 1 / (1 - bounds[1]), 1 / (1 - bounds[0])
        else:
            return 1.0, 1.0

    ###########################################################################
    #                           Minima calculations                           #
    ###########################################################################

    def gen_various(self):
        if self.additional is not None:
            return None

        bounds_factor_left = self.bounds_right[0]
        bounds_factor_right = self.bounds_right[1]
        bounds = self.right
        if bounds[1] >= self.options.right_limit / bounds_factor_right:
            return None
        if bounds[0] >= self.options.right_limit / bounds_factor_left:
            return None

        if self.sim.options.gtensor_E is None:
            outer_range = self.E_range(True)
            inner_range = self.E_range(False)
            i = 1 if self.options.gfactor_to_right else 0
            E_goal = (inner_range[i] + outer_range[i]) / 2
            E_z = E_goal
        else:
            E_z = self.sim.options.gtensor_E

        Psi(self, outer=True,
            E_z=E_z,
            message="Generating additional data",
            eps_factor=1e0
            ).run()

    # Find and generate points for minimas
    def gen_minimas(self, outer=False):
        if self.minimum is None:
            return None
        # Initialize counter variables
        do_bisection = 0

        while True:
            i = self.minimum_index
            if self.E_min_diff < self.options.minima_eps:
                return None
            do_bisection += 1
            # Decide which method to use
            if not do_bisection % self.options.bisection_freq:
                self.bisection_minimum(i, outer)
            elif do_bisection % self.options.parabola_freq:
                self.fitting_minimum(i, outer)
            else:
                self.parabola_minimum(i, outer)

    # Look for a minimum using bisection method
    def bisection_minimum(self, i, outer):
        E_list = self.E_list_minimum(i)
        # Calculate to the left
        error = self.options.minima_eps / self.span(outer)
        E_diff = self.E_min_diff / self.span(outer)
        if self.calcs[i - 1].anti > self.calcs[i + 1].anti:
            E_z = E_list[1] - (E_list[1] - E_list[0]) * (1 - ϕ(E_diff))
        # Calculate to the right
        else:
            E_z = E_list[1] + (E_list[2] - E_list[1]) * (1 - ϕ(E_diff))
        # Run the calculation
        Psi(self, outer,
            E_z=E_z*0.98+(E_list[2] + E_list[0])/2*0.02,
            E_diff=E_diff,
            message="Generating minima by bisection",
            eps_factor=self.options.eps_factor_for_minima,
            minimum=None if outer else E_list[1],
            error=error
            ).run()

    # Look for a minimum using parabola method
    def parabola_minimum(self, i, outer):
        E_list = self.E_list_minimum(i)
        # Find E-field for a suspected minimum
        E_min = para_min(self.calcs[i - 1], self.calcs[i], self.calcs[i + 1])
        # Exit if parabola calculations are not precise enough
        if not E_list[0] < E_min < E_list[2]:
            echo("Fitting by fitting v2 skipped! " +
                 "{} not in range {}-{}".format(E_min, E_list[0], E_list[2]))
        # Calculate point for the suspected minimum if not already calculated
        if not close(E_min, E_list[1]):
            Psi(self, outer,
                E_z=E_min*0.98+(E_list[2] + E_list[0])/2*0.02,
                E_diff=self.E_min_diff / self.span(outer),
                message="Generating minima by parabolas",
                eps_factor=self.options.eps_factor_for_minima,
                minimum=None if outer else E_list[1],
                error=self.options.minima_eps / self.span(outer)
                ).run()
        # Calculate two points nearby to get proper range
        else:
            for sign in [-1, 1]:
                if self.E_min_diff < self.options.minima_eps:
                    return None
                side = "left" if sign == -1 else "right"
                Psi(self, outer,
                    E_z=E_min + sign * self.options.minima_eps / 20,
                    E_diff=self.E_min_diff / self.span(outer),
                    message="Minima confirmed, " + side + " vicinity",
                    eps_factor=self.options.eps_factor_for_minima,
                    minimum=None if outer else E_list[1],
                    error=self.options.minima_eps / self.span(outer)
                    ).run()

    def fitting_minimum(self, i, outer):
        E_list = self.E_list_minimum(i)
        # Find E-field for a suspected minimum
        x = [c.E_z for c in self.calcs if c.E_z in E_list]
        y = [c.anti for c in self.calcs if c.E_z in E_list]
        E_min = fit_min(x, y, x_0=x[1])
        # Exit if parabola calculations are not precise enough
        if not E_list[0] < E_min < E_list[2]:
            echo("Fitting by fitting v2 skipped! " +
                 "{} not in range {}-{}".format(E_min, E_list[0], E_list[2]))
        # Calculate point for the suspected minimum if not already calculated
        elif not close(E_min, E_list[1]):
            Psi(self, outer,
                E_z=E_min*0.98+(E_list[2] + E_list[0])/2*0.02,
                E_diff=self.E_min_diff / self.span(outer),
                message="Generating minima by fitting",
                eps_factor=self.options.eps_factor_for_minima,
                minimum=None if outer else E_list[1],
                error=self.options.minima_eps / self.span(outer)).run()

    ##########################################################################
    #                              Minima misc.                              #
    ##########################################################################

    # Check if a given point is a local minimum
    def is_local_minimum(self, i):
        min_neighbor = min(self.calcs[i + 1].anti, self.calcs[i - 1].anti)
        return self.calcs[i].anti < min_neighbor

    # List of E-field triplets
    def E_list_minimum(self, i):
        return [self.calcs[i + x].E_z for x in [-1, 0, 1]]

    # E-field difference around a minimum
    def E_diff_minimum(self, i):
        return self.calcs[i + 1].E_z - self.calcs[i - 1].E_z

    # Check if the structure has a minimum
    @property
    def has_minimum(self):
        return self.minimum is not None

    ###########################################################################
    #                            Update properties                            #
    ###########################################################################

    # Update limits
    def update_limits(self):
        # Update if calculations list is not empty, otherwise do nothing
        if self.calcs:
            # Decrease left side limit
            if self.limits[0] + self.options.limit_update > self.calcs[0].E_z:
                self.limits[0] = self.calcs[0].E_z - self.options.limit_update
            # Increase right side limit
            if self.limits[1] - self.options.limit_update < self.calcs[-1].E_z:
                self.limits[1] = self.calcs[-1].E_z + self.options.limit_update

    # Update ranges, both outer and inner
    def update_ranges(self):
        self.update_range(outer=True)
        self.update_range(outer=False)

    # Update either outer or inner range
    def update_range(self, outer=True):
        # Set to the default range
        range = self.limits[:]

        # Define values for definitions
        limit = self.options.limit
        low_lim_l = ((1 - limit) if outer else (1 - limit))
        up_lim_l = limit if outer else 0.0
        low_lim_r = limit
        up_lim_r = (1.0 - limit) if outer else 1.0

        # Compare every calculation to define ranges
        left_range_found = False
        for calc in self.calcs:
            # Left side range
            if calc.local_low > low_lim_l and calc.local_up > up_lim_l:
                if not left_range_found:
                    range[0] = calc.E_z
            else:
                left_range_found = True
            # Right side range
            if calc.local_low < low_lim_r:
                if calc.local_up < up_lim_r:
                    if range[1] == self.limits[1]:
                        range[1] = calc.E_z
                        # Exit as range is already found
                        break
        # Assign newly found range
        if outer:
            self.outer_range = tuple(range)
        else:
            self.inner_range = tuple(range)

    @property
    def E_min(self):
        return self.minimum.E_z

    def update_minimum(self):
        self.minimum = None
        self.minimum_index = None
        self.E_min_diff = None
        for i, calc in enumerate(self.calcs[1:-1]):
            if self.in_range_exclusive(calc.E_z, False):
                if calc.anti > self.calcs[i].anti:
                    continue
                if calc.anti > self.calcs[i + 2].anti:
                    continue
                if self.minimum is None or calc.anti < self.minimum.anti:
                    self.minimum = calc
                    self.E_min_diff = self.calcs[i + 2].E_z - self.calcs[i].E_z
                    self.minimum_index = i + 1

    ###########################################################################
    #                            Output and infos                             #
    ###########################################################################

    def title(self, outer):
        return "outer" if outer else "inner"

    def range_confidence(self, outer):
        return encase([percent(i) for i in self.gap(outer)])

    @property
    def opt_Ez_piezo(self):
        left_outer, right_outer = self.outer_range
        left_inner, right_inner = self.inner_range
        left = abs(left_outer - left_inner)
        right = abs(right_outer - right_inner)
        if left > right:
            return (left_outer * 0.5 + left_inner * 0.5)
        else:
            return (right_outer * 0.5 + right_inner * 0.5)

    ##########################################################################
    #                              Other misc.                               #
    ##########################################################################

    # Epsilon factor for kp calculations
    def eps_factor(self, outer):
        return self.options.eps_factor_for_outer if outer else 1

    # Sort calculations, if there are any
    def sort_per_Ez(self):
        if self.calcs:
            self.calcs.sort()

    # Check if calculation belongs to the structure
    def calc_belongs(self, calc):
        # Structure number is correct
        if self.n_str == calc.n_str:
            # In-plane electric field is correct
            if close(self.E_x, calc.E[0]) and close(self.E_y, calc.E[1]):
                # Magnetic field is correct
                if (close(self.B[0], calc.B[0]) and close(self.B[1], calc.B[1])
                        and close(self.B[2], calc.B[2])):
                    return True
        return False

    # Deleted repeated records
    def remove_repeats(self):
        i = 0  # Counter variable
        # Go over all pairs of neighbors
        while i < len(self.calcs) - 1:
            # If E_z is the same remove record due to unnecessary repeat
            # This increases counter by decreasing list length
            if self.calcs[i].E_z == self.calcs[i + 1].E_z:
                # if self.projectname == "E_field":
                #     echo(self.projectname+"\t" +str(self.calcs[i].n_str) + "\t" + str(self.calcs[i].n_calc))
                self.calcs.pop(i)
            # Else increase counter
            else:
                i += 1

    @property
    def gfactors(self):
        if self.additional is not None:
            return [self.additional.g_low, self.additional.g_up]
        return [None, None]

    @property
    def gfactors_sign_diff(self):
        if self.additional is not None:
            return self.gfactors[0] * self.gfactors[1] < 0.0
        return None

    @property
    def piezo(self):
        return self.additional.piezo

    @property
    def gfactor_diff(self):
        if self.gfactors[0] is None:
            return None
        return self.gfactors[0] - self.gfactors[1]

    @property
    def gfactor_sum(self):
        return sum(self.gfactors)

    @property
    def theta(self):
        return arccos(self.B_z)

    @property
    def phi(self):
        if self.B_x == self.B_y == 0.0:
            return 0.0
        else:
            return arctan2(self.B_y, self.B_x)

    @property
    def n(self):
        n = 1 if self.additional is None else 0
        # if "gtensor" in self.sim.output_filename:
        #     return 1 if self.additional is None else 0
        # if self.options.calc_additional:
        #     return 1 if self.additional is None else 0
        for outer, left in product([True, False], repeat=2):
            bounds = self.gap(outer)
            bounds_factor = self.bounds_factor(outer, left)
            x = bounds[left % 2] / self.options.bound_limit * bounds_factor
            n += max(int(ceil(log2(x))), 0)
        for i, bound in enumerate(self.right):
            bound *= self.bounds_right[i] / self.options.right_limit
            if bound > 0:
                n += max(int(ceil(log2(bound))), 0)
        # Loop over all triplets of neighboring points
        if self.has_minimum:
            x = self.E_min_diff / self.options.minima_eps
            n += min(max(int(ceil(log2(x)/3)), 0), 5)
        return n

    @property
    def x_axis(self):
        if "B_field_gfactor" in self.sim.output_filename:
            return self.B_val
        elif "rotate" in self.projectname:
            return self.angle
        elif "anticrossing_gfactor" in self.sim.output_filename:
            return self.B_val
        elif self.projectname == "E_field":
            if self.E_x < 0 and self.E_y < 0:
                return -sqrt(self.E_x**2 + self.E_y**2)
            return sqrt(self.E_x**2 + self.E_y**2)
        elif "shift" in self.projectname:
            if "compensation" in self.sim.output_filename:
                if self.E_x < 0 and self.E_y < 0:
                    return - sqrt(self.E_x**2 + self.E_y**2)
                elif self.E_y == 0:
                    return self.E_x
                return sqrt(self.E_x**2 + self.E_y**2)
            else:
                i = self.n_str - 1
                if self.n_str == 23:
                    i = 0.5
                if self.n_str == 24:
                    i = 1.5
                i = i * 2 # / 6.0 * 5.65
                if "110" in self.projectname:
                    return i * sqrt(2)
                if "100" in self.projectname:
                    return i
        elif "diffc" in self.projectname:
            return 0.15 + 0.05 * self.n_str if self.n_str <= 17 else 0.05 * (self.n_str - 17)
        elif "diffH" in self.projectname:
            return 84 + 6 * self.n_str
        elif "topvar" in self.projectname:
            return -84 + 12 * self.n_str
        elif "downvar" in self.projectname:
            return -72 + 12 * self.n_str if self.n_str != 13 else -72
        elif "diffD" in self.projectname:
            return 3 * self.n_str
        elif "diffR" in self.projectname:
            return 78 + 6 * self.n_str
        elif "elong" in self.projectname:
            if "E110" in self.sim.output_filename:
                if self.E_x < 0 and self.E_y < 0:
                    return -sqrt(self.E_x**2 + self.E_y**2)
                return sqrt(self.E_x**2 + self.E_y**2)
            elif "E100" in self.sim.output_filename:
                return self.E_x
            elif "_100" in self.projectname:
                if self.n_str < 12:
                    return 0.4 + 0.1 * self.n_str
                elif self.n_str == 13:
                    return 1.05
                elif 14 <= self.n_str <= 18:
                    return 0.2 + 0.1 * self.n_str
                elif 19 <= self.n_str <= 23:
                    return -1.35 + 0.1 * self.n_str
            elif "_110" in self.projectname:
                if self.n_str <= 16:
                    return 0.4 + 0.1 * self.n_str
                elif 17 <= self.n_str <= 21:
                    return -1.15 + 0.1 * self.n_str
        else:
            assert False, "Error, " + self.projectname + " doesn't work!"

    @property
    def angle(self):
        assert "rotate" in self.projectname, self.projectname
        if "shift" in self.projectname:
                # return 50 - 5 * self.n_str if self.n_str <= 10 else 32.5 - 5 * (self.n_str - 16)
                if self.n_str <= 10 :
                    return 50 - 5 * self.n_str
                elif self.n_str <= 22:
                    return 32.5 - 5 * (self.n_str - 16)
                elif self.n_str <= 33:
                    return 83.75 - 2.5 * self.n_str
                elif self.n_str == 34:
                    return 1.875
                elif self.n_str == 35:
                    return 0.625
        else: # Elongation along real x with shifting crystal
            if self.n_str <= 10:
                return 50 - 5 * self.n_str
            elif self.n_str <= 14:
                return 15 - self.n_str
            elif self.n_str == 15:
                return 7.5
            elif self.n_str == 16:
                return 12.5
            elif self.n_str == 17:
                return 16
            elif self.n_str == 18:
                return 14
            elif self.n_str == 19:
                return 13
            elif self.n_str == 20:
                return 17
            elif self.n_str < 24:
                return -5 * (self.n_str - 20)
            elif self.n_str == 24:
                return 15.9412
            elif self.n_str == 25:
                return 15.8824
            elif self.n_str == 26:
                return 15.9446
            elif self.n_str == 27:
                return 50
            elif self.n_str == 28:
                return 11.25
            elif self.n_str == 29:
                return 8.75
            elif self.n_str == 30:
                return 6.25
