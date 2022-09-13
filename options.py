from os import popen

# Options class, containing various options for the calculations
class Options():
    def __init__(self,
                 eps=1e-6,
                 minima_eps=1e-0,
                 fill_blank=0.8,
                 bound_limit=0.39999,
                 gtensor_E=None,
                 write_fit_data=False,
                 restrict_unsorted=False,
                 gfactor_to_right=True):

        # Output settings
        self.write_gtensor = False if gtensor_E is None else True
        self.write_default = True if gtensor_E is None else False
        self.write_fit_data = write_fit_data

        # Continue calculations with increased threshold
        self.continue_calculations = True

        # kp calculation epsilon
        self.eps = eps

        # kp calculation epsilon for finding minimas
        self.eps_factor_for_minima = 1e-2

        # Decrease in epsilon for outer calculations requiring less precision
        self.eps_factor_for_outer = 1e0

        # Localization cut-off level
        self.limit = 0.05

        # % density limit for bounds calculations
        self.bound_limit = bound_limit

        # % density limit for bounds calculations
        self.right_limit = 0.0999999

        # Maximum percent allowed when filling blanks
        self.fill_blanks_limit = fill_blank

        # Increase factor for additional calculations
        self.continous_factor = 1.5

        # Allowed error for finding minimas, in E-field units
        self.minima_eps = minima_eps

        # Default range
        self.default_limits = (-40.0, 30.0)

        # Change of limits if needed adjustment
        self.limit_update = 8.01

        # True if calculations conducted on Polaron
        # False is meant for data analysis and printing output files
        self.Polaron = self.is_Polaron()

        # Load between same structures in different projects
        self.read_special_cases = False

        # Remove old minimas
        self.remove_old_minimas = False

        # Once in how many calculations to use bisection method
        # 1 ⟹ always
        # large number ⟹ never
        self.parabola_freq = 3
        self.bisection_freq = 5

        self.kp_dir = "test"

        self.do_calcs_from_file = False

        self.enable_counter = True

        self.gtensor_E = gtensor_E

        self.restrict_unsorted = restrict_unsorted

        self.calc_minima_from_previous = True

        self.gfactor_to_right = gfactor_to_right

    # Increase precision for additional calculations
    def increase_threshold(self):
        self.calc_minima_from_previous = False
        # self.minima_eps /= self.continous_factor
        self.bound_limit /= self.continous_factor
        self.right_limit /= self.continous_factor
        # self.fill_blanks_limit /= self.continous_factor

    @property
    def minima_vicinity(self):
        return self.minima_eps * 1e2

    def is_Polaron(self):
        return "polaron" in popen("echo $HOSTNAME").read()
