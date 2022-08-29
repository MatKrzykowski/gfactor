import numpy as np
import lmfit


##############################################################################
#                                  Parabola                                  #
##############################################################################
#
# Fit to the parabola ax²+bx+c = 0
# Minimum found via x₀ = -½b/a

# Find parabola coefficients a, b and c given 3 points
# Other parts of the code should ensure that this function behaves well,
# for example there is no division by 0 or minimum is outside desired range
def parabola(A, B, C  # 3 points taken from calculations
             ):
    # Assign values from the calculations using point method
    x1, y1 = A.point
    x2, y2 = B.point
    x3, y3 = C.point

    # Normalize values for better precision (point B should be in 0,0)
    x1, y1 = x1 - B.point[0], y1 - B.point[1]
    x2, y2 = x2 - B.point[0], y2 - B.point[1]
    x3, y3 = x3 - B.point[0], y3 - B.point[1]

    # Variables used to decrease number of computations
    x1p2, x3p2, x1mx3 = x1**2, x3**2, x1 - x3

    # Calculate a, b and c coefficients
    a = (y1 / x1 - (y1 - y3) / x1mx3) / (x1p2 / x1 - (x1p2 - x3p2) / x1mx3)
    b = (y1 - a * x1p2) / x1
    c = y1 - a * x1p2 - b * x1
    return a, b, c


# Find minimum given 3 points using well know formula
def para_min(A, B, C):
    # Calculate coefficients a, b and c
    a, b, c = parabola(A, B, C)
    # Calculate minimum
    minimum = -0.5 * b / a
    # Compensate for changes in parabola function
    return minimum + B.E_z


##############################################################################
#                                   Fitting                                  #
##############################################################################
#
# Fit to function √(Δ² + (A(x-x₀))²)
# Minimum found via x₀

# Residue funtion used by lmfit
def residue(params,  # parameters object provided by lmfit
            x,  # array of x
            y  # array of y
            ):
    y = np.array(y)
    Δ = params["Δ"]  # Anticrossing parameter
    x_0 = params["x_0"]  # Position of minimum parameter
    A = params["A"]  # Scaling parameter due to Stark effect
    return y - np.array([np.sqrt(Δ**2 + (A * (X - x_0))**2) for X in x])


# Find minimum given arrays of x and y
def fit_min(x,  # array of x
            y,  # array of y
            # Initial guess for minimum position, necessary to ensure fitting
            # procedure converges to correct values
            x_0=0.0
            ):
    # Initialize parameters object and provide initial guesses for values
    params = lmfit.Parameters()
    params.add("Δ", value=y[1])
    params.add("x_0", value=x_0, min=x[0], max=x[2])
    params.add("A", value=0.0027)
    # Let lmfit do the fitting procedure
    params = lmfit.minimize(residue, params=params, args=(x, y)).params
    # Return minimum position value resulting from the fitting procedure
    return params.valuesdict()["x_0"]
