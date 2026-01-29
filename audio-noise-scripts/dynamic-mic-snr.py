import numpy as np

'''

This script computes the SNR of a dynamic microphone with given source
impedance and sensitivity (grab from mic datasheet). It uses the provided
EIN figure (A-weighted, in dBu) to estimate a true SNR.

This assumes all figures are in dBu and A-weighted. If using dBV, you must
first convert to dBu by adding 2.2 dB to input values. (dBu = dBV + 2.2)
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
degC = 23                  # Ambient temp in degrees C
ein_int = -129             # Datasheet EIN of interface/recorder in dBu(A)
mic_impedance = 350        # Microphone source impedance in Ohms
mic_sensitivity_mV = 2.7   # Mic sensitivity in mV/Pa

# Thermal noise voltage for resistance x (Ohm)
def tnoise(x):
    kb = 1.381e-23
    return np.sqrt(4*kb*(degC+273.15)*x*20000)

# Convert Vrms to dBu with A-weighting correction
def dBuA(x_rms):
    return 20*np.log10(x_rms/0.775) - 2

# Convert Vrms to dBu unweighted
def dBuU(x_rms):
    return 20*np.log10(x_rms/0.775)

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


#### BEGIN SCRIPT ####

# Remove 150 ohm test resistor thermal noise from datasheet EIN figure
ein_int = dBuA(vrms_amp_alone(ein_int, 150))

# Compute A-weighted EIN with actual mic impedance
mic_ein = dBuA(combine_white_noise(tnoise(mic_impedance), vrmsA(ein_int)))
mic_sig = dBuU(mic_sensitivity_mV/1000.0)

# Print results
print()
print("EIN shorted: {:.1f} dBuA".format(ein_int))
print("EIN with mic: {:.1f} dBuA".format(mic_ein))
print("Mic level @ 94 dB SPL: {:.1f} dBu".format(mic_sig))
print()
print("Overall SNR: {:.1f} dB".format(mic_sig - mic_ein))
print()