import numpy as np

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
def vrms(x_dBuA):
    return 10**((x_dBuA - 0.214)/20)

# Combine two uncorrelated white noise sources
def combine_white_noise(n1, n2):
    return np.sqrt(n1**2 + n2**2)

# Compute Vrms of amplifier alone with datasheet-specified
#   test resistor thermal noise removed
def vrms_amp_alone(ein, r_test):
    return np.sqrt(vrms(ein)**2 - tnoise(r_test)**2) 

# Remove 150 ohm test resistor thermal noise from datasheet EIN figures
ein0 = dBuA(vrms_amp_alone(ein0, 150))
ein1 = dBuA(vrms_amp_alone(ein1, 150))

# Print results
print()
print("EIN amp0 short: {:.1f} dBuA".format(ein0))
print("EIN amp1 short: {:.1f} dBuA".format(ein1))

# Compute EIN with 350 Ohm source impedance
mic_ein0 = dBuA(combine_white_noise(tnoise(mic_impedance), vrms(ein0)))
mic_ein1 = dBuA(combine_white_noise(tnoise(mic_impedance), vrms(ein1)))

# Print results
print()
print("EIN amp0 @ {} Ohm: {:.1f} dBuA".format(mic_impedance, mic_ein0))
print("EIN amp1 @ {} Ohm: {:.1f} dBuA".format(mic_impedance, mic_ein1))
print("SNR improvement: {:.1f} dB".format(mic_ein0 - mic_ein1))
print()