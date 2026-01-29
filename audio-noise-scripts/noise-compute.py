import numpy as np

'''

This script computes the actual equivalent input noise level [EIN] of a
dynamic microphone with given source impedance (grab from mic datasheet).

This assumes all figures are in dBu and A-weighted. If using dBV, you must
first convert to dBu by adding 2.2 dB to all input values. (dBu = dBV + 2.2)
The script assumes the datasheet EIN values are measured with a 150 Ohm
test resistor, and removes that thermal noise contribution before adding
the thermal noise of the input microphone source impedance. It also assumes
all noise is purely white and uncorrelated such that A-weighting just reduces
the noise level by 2 dB.

You'll need numpy to run it. Change the input parameters and observe the
results. Play around with the functions and enjoy!

Post questions in Youtube comments or email them to jtmcg@alum.mit.edu

'''

# Input data
degC = 23               # Ambient temp in degrees C
ein0 = -122             # Measured EIN amp0 in dBuA
ein1 = -129             # Measured EIN amp1 in dBuA
mic_impedance = 350     # Microphone source impedance in Ohm

# Thermal noise voltage for resistance x (Ohm)
def tnoise(x):
    kb = 1.381e-23
    return np.sqrt(4*kb*(degC+273.15)*x*20000)

# Convert Vrms to dBu with A-weighting correction
def dBuA(x_rms):
    return 20*np.log10(x_rms/0.775) - 2

# Convert dBu to Vrms with A-weighting correction
def vrmsA(x_dBuA):
    return 10**((x_dBuA - 0.214)/20)

# Convert dBu to Vrms unweighted
def vrmsU(x_dBuA):
    return 10**((x_dBuA - 2.214)/20)

# Combine two uncorrelated white noise sources
def combine_white_noise(vn1, vn2):
    return np.sqrt(vn1**2 + vn2**2)

# Compute Vrms of amplifier alone with datasheet-specified
#   test resistor thermal noise removed
def vrms_amp_alone(ein, r_test):
    return np.sqrt(vrmsA(ein)**2 - tnoise(r_test)**2) 

# Remove 150 ohm test resistor thermal noise from datasheet EIN figures
ein0 = dBuA(vrms_amp_alone(ein0, 150))
ein1 = dBuA(vrms_amp_alone(ein1, 150))

# Print results
print()
print("EIN amp0 short: {:.1f} dBuA".format(ein0))
print("EIN amp1 short: {:.1f} dBuA".format(ein1))

# Compute EIN with 350 Ohm source impedance
mic_ein0 = dBuA(combine_white_noise(tnoise(mic_impedance), vrmsA(ein0)))
mic_ein1 = dBuA(combine_white_noise(tnoise(mic_impedance), vrmsA(ein1)))

# Print results
print()
print("EIN amp0 @ {} Ohm: {:.1f} dBuA".format(mic_impedance, mic_ein0))
print("EIN amp1 @ {} Ohm: {:.1f} dBuA".format(mic_impedance, mic_ein1))
print("SNR improvement: {:.1f} dB".format(mic_ein0 - mic_ein1))
print()