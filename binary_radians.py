# This program generates binary radian and sine tables constants for fixed
# point integer trigonometry. The output consists of assembler, C, and Forth
# files useful for computing enviroments without floating point hardware.
# Examples include classic the GPS, eight bit microprocessors (e.g. 65c02), and
# microcontrollers (e.g. R65f11, Flash Forth systems).

# Binary angular measurement defines a brad as the unit circle circumference
# divided by a power of 2^N where N is the size of a machine word.
# E.g. brad = 2Pi / 2^n
#
# Brads may be signed or unsigned depending upon the application
# For more information: https://en.wikipedia.org/wiki/Binary_angular_measurement

import math
import sys

# todo: parse command line or prompt user for n.
n = 12
num_of_brads = 2 ** n
brad_ratio = 2 * math.pi / num_of_brads
fraction_bits = 14
scaling_factor = 2 ** fraction_bits

# Values for common angles in brads with ten bits of precision
degree_angle = int(num_of_brads / 360)
acute_angle = int(num_of_brads / 8)
right_angle = int(num_of_brads / 4)
straight_angle = int(num_of_brads / 2)
reflex_angle = int(num_of_brads - right_angle)
max_brad = num_of_brads - 1

print("hex")
print(f"{degree_angle:04x} constant DEGREE_ANGLE")
print(f"{acute_angle:04x} constant ACUTE_ANGLE")
print(f"{right_angle:04x} constant RIGHT_ANGLE")
print(f"{straight_angle:04x} constant STRAIGHT_ANGLE")
print(f"{reflex_angle:04x} constant REFLEX_ANGLE")
print(f"{fraction_bits:04x} constant BITSHIFT_FACTOR")
print(f"{scaling_factor:04x} constant SCALING_FACTOR")

column = 0
count = 0
print("create sineTable")
print("  ",end='')
for brad in range(0, right_angle+1, 1):
    val = int(math.sin(brad_ratio * brad) * scaling_factor)
    print(f"{val:04x} , ",end='')
    column += 1
    count += 1
    if (column == 10):
        print("")
        print("  ",end='')
        column = 0

print("")
print(f"{count} constant SINE_TABLE_SIZE")
print("decimal")
