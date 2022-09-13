#!/usr/bin/env bash

# Update data from Polaron
calc/output_data.py

# diffc project
cd diffc
gnuplot gfactor.plt

# diffD project
cd ../diffD
gnuplot gfactor.plt

# diffRandH project
cd ../diffRandH
gnuplot gfactor.plt

# shift110 project
cd ../shift110
gnuplot gfactor.plt

# shift100 project
cd ../shift100
gnuplot gfactor.plt

# E_field project
cd ../E_field
gnuplot gfactor.plt
