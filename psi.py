from time import sleep
from os import system

from common import echo, encase, screen_w, percent, psi_safeguard, psi_release
from common import close, sqrt2
from clear_files import clear_files


# Psi class, meant to prepare and execute calculation
class Psi():
    def __init__(self, struct,
                 outer=True,
                 E_z=0.0,
                 eps_factor=1.0,
                 E_diff=1.0,
                 message="",
                 # max_seconds=60.0,
                 max_seconds=180.2,
                 sleep_interval=0.1,
                 kp_log="kp_log",
                 kp_skip=20,
                 error=0,
                 minimum=None):
        self.struct = struct
        self.outer = outer
        self.E_z = E_z
        self.E_diff = E_diff
        self.message = message
        self.eps = struct.options.eps * eps_factor
        self.max_seconds = max_seconds
        self.sleep_interval = sleep_interval
        self.kp_log = kp_log
        self.kp_skip = kp_skip
        self.error = error
        self.minimum = minimum

        self.w = screen_w() - 2
        self.chars_old = "─┼░▒▓█"
        self.chars = "═╪░▒▓█"

    def current_position(self, outer, minimum=None):
        position = self.struct.pos_in_range(self.E_z, outer, minimum)
        return int(self.w * position) + 1

    def bar(self, outer=True, recursive=False, minimum=None):
        # If inner print bar for outer and abjusted space between bars
        if not outer:
            self.bar(outer=True, recursive=True)
            self.between_bars(outer=True, ext=True)

        # B = ["├"] + self.w * [self.chars[0]] + ["┤"]
        B = ["╠"] + self.w * [self.chars[0]] + ["╣"]
        for calc in self.struct.calcs:
            x = self.struct.pos_in_range(calc.E_z, outer)
            if 0.0 < x < 1.0:
                x = int(self.w * x)
                B[x + 1] = self.increase_char(B[x + 1])

        B[self.current_position(outer)] = "X"
        echo(encase("".join(B)))
        if minimum is None:
            if not recursive:
                self.between_bars(outer)
        else:
            self.between_bars(outer=False, ext=True, minimum=None)

            B = ["┠"] + self.w * [self.chars[0]] + ["┫"]
            # B = ["╠"] + self.w * [self.chars[0]] + ["╣"]
            # B = ["├"] + self.w * [self.chars[0]] + ["┤"]
            for calc in self.struct.calcs:
                x = self.struct.pos_in_range(calc.E_z, outer=outer,
                                             minimum=minimum)
                if 0.0 < x < 1.0:
                    x = int(self.w * x)
                    B[x + 1] = self.increase_char(B[x + 1])

            B[self.current_position(outer, minimum)] = "X"
            echo(encase("".join(B)))
            self.between_bars(outer, minimum=minimum)

    def between_bars(self, outer, ext=False, minimum=None):
        # Write E-field values
        current_E_range = self.struct.E_range(outer, minimum)
        left_E = [i for i in str(round(current_E_range[0], 4))]
        right_E = [i for i in str(round(current_E_range[-1], 4))]
        B1 = left_E + [" "] * (self.w + 2 - len(left_E + right_E)) + right_E

        # Write E-field value if there is free space to do so
        X_E = [i for i in str(round(self.E_z, 4))]
        x = self.current_position(outer, minimum)
        if len(set(B1[x:x + len(X_E)])) == 1:
            B1 = B1[:x] + X_E + B1[x + len(X_E):]

        if ext:
            my_minimum = None if outer else self.minimum
            E = self.struct.E_range(outer=False, minimum=my_minimum)[0]
            x1 = int(self.w * self.struct.pos_in_range(E, outer=outer))

            E = self.struct.E_range(outer=False, minimum=my_minimum)[1]
            x2 = int(self.w * self.struct.pos_in_range(E, outer=outer))
            B2 = ["╓"] + ["─"] * x1
            B2 += [" "] * (x2 - x1 + 1) + (self.w - x2 - 1) * ["─"] + ["╖"]
            B2[x1 + 1] = "╜"
            B2[x2 + 1] = "╙" if B2[x2 + 1] != "╜" else "╨"

            if B1[x1 + 1] == " ":
                B1[x1 + 1] = "║"
            if B1[x2 + 1] == " ":
                B1[x2 + 1] = "║"

            B3 = ["║"] + self.w * [" "] + ["║"]
            echo(encase("".join(B1)))
            echo(encase("".join(B2)))
            echo(encase("".join(B3)))
        else:
            echo(encase("".join(B1)))

    def increase_char(self, char):
        return self.chars[min(len(self.chars) - 1, self.chars.index(char) + 1)]

    # Run single calculation
    def run(self):
        Bz_str = " -Bz {:.10f}".format(self.struct.B[2])
        Ex_str = " -Ex {:.10f}".format(self.struct.E_x)
        Ey_str = " -Ey {:.10f}".format(self.struct.E_y)

        assert self.error <= 1, "Error is too large"
        if self.minimum and self.E_diff > 1e-3:
            pass
            # self.eps *= 1e3 * min(1.0, self.E_diff)
        elif self.outer and self.E_diff > 1e-1:
            self.eps *= 1e1 * min(1.0, self.E_diff)

        # Run the calculation
        system("python run.py psi " +
               "--projectname " + self.struct.projectname +
               " -Bx {:.10f}".format(self.struct.B[0]) +
               " -By {:.10f}".format(self.struct.B[1]) +
               Bz_str +
               " -n {}".format(self.struct.n_str) +
               Ex_str +
               Ey_str +
               " -Ez {:.10f}".format(self.E_z) +
               " --nev_h 4 --eps " + str(self.eps) +
               " > kp_log 2> errlog & disown")

        self.struct.sim.read_additional()
        self.struct.sim.counter.update()
        self.calculation_info()
        psi_safeguard()
        self.bar(self.outer, minimum=self.minimum)

        done, last_line, time_last_line = False, "", 0
        clear_files(self.struct.projectname)
        while not done:
            sleep(self.sleep_interval)
            with open(self.kp_log) as file:
                lines = list(file)
                if not lines:
                    continue
                if lines[-1] == last_line:
                    time_last_line += self.sleep_interval
                else:
                    last_line, time_last_line = lines[-1], 0
                    if "EPS" in last_line:
                        n_iter = int(last_line.split()[0])
                        if n_iter in [1, 2, 3, 4] or not n_iter % self.kp_skip:
                            echo('"' + last_line.rstrip("\n") + '"')

                if time_last_line >= self.max_seconds:
                    done = True
                    self.kill_psi()
                    echo("Emergency exit!!")

                if "Done" in last_line:
                    done = True
                    echo("Done")

        # Read files to update the data
        self.struct.sim.read_files()
        psi_release()

    # Print information about the calculation
    def calculation_info(self):
        echo("")
        echo(self.message)
        echo("projectname {} ".format(self.struct.projectname) +
             " nstr {} ".format(self.struct.n_str) +
             " Ex {:.8f}".format(self.struct.E_x) +
             " Ey {:.8f}".format(self.struct.E_y) +
             " Ez {:.8f}".format(self.E_z) +
             " Bx {:.8f}".format(self.struct.B[0]) +
             " By {:.8f}".format(self.struct.B[1]) +
             " Bz {:.8f}".format(self.struct.B[2]) +
             " eps {:.2e}".format(self.eps) +
             " " + percent(self.E_diff)
             + ((' ">" ' + percent(self.error)) if self.error else ""))

    def kill_psi(self):
        echo("Calculation stopped!")
        system("killall psi")
