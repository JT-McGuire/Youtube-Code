import numpy as np
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------------
# Constants & Thermodynamics Setup
# -----------------------------------------------------------------------------
gamma = 1.4
CR = 5.0                 # Standard 5:1 Compression Ratio
V_bdc = 1.0              # Bottom Dead Center Volume (1.0 relative)
V_tdc = V_bdc / CR       # Top Dead Center Volume (0.2)

P1 = 1.0                 # Ambient pressure (atm)
T1 = 288.0               # Ambient temperature (K)
dT_combustion = 1000.0   # Heat addition (K)
mR = (P1 * V_bdc) / T1   # Ideal gas scaling

# Helper for Isentropic Curve (P * V^gamma = Const)
def isentropic_path(V_start, V_end, P_start):
    V = np.linspace(V_start, V_end, 300)
    P = P_start * (V_start / V)**gamma
    return V, P

# -----------------------------------------------------------------------------
# 1. State Calculations: Otto Cycle
# -----------------------------------------------------------------------------
P2_otto = P1 * (CR**gamma)              # 9.52 atm
T2_otto = T1 * (CR**(gamma - 1.0))      # 547.8 K (~274°C)

T3_otto = T2_otto + dT_combustion       # 1547.8 K
P3_otto = P2_otto * (T3_otto / T2_otto) # 26.9 atm (~27 atm)

# Standard 5:1 Expansion (ends at V_bdc = 1.0)
P4_otto = P3_otto * ((V_tdc / V_bdc)**gamma) # 2.82 atm
T4_otto = T3_otto * ((V_tdc / V_bdc)**(gamma - 1.0)) # 681 K

# Extended Expansion down to 1.5 atm (~7.8:1 ratio)
P_exp_end = 1.5
V_exp_end = V_tdc * (P3_otto / P_exp_end)**(1.0 / gamma) # V ~ 1.57

# Generate Curves
V_otto_comp, P_otto_comp = isentropic_path(V_bdc, V_tdc, P1)
V_otto_exp_std, P_otto_exp_std = isentropic_path(V_tdc, V_bdc, P3_otto)
V_otto_exp_ext, P_otto_exp_ext = isentropic_path(V_tdc, V_exp_end, P3_otto)

# -----------------------------------------------------------------------------
# 2. State Calculations: Lenoir Cycle
# -----------------------------------------------------------------------------
T2_len = T1 + dT_combustion             # 1288 K
P2_len = (mR * T2_len) / V_bdc          # 4.47 atm (~4.5 atm)

V_len_exp_end = V_bdc * (P2_len / P_exp_end)**(1.0 / gamma) # V ~ 2.18
V_len_exp, P_len_exp = isentropic_path(V_bdc, V_len_exp_end, P2_len)

# -----------------------------------------------------------------------------
# Plot Formatting Helper
# -----------------------------------------------------------------------------
def format_ax(ax, title, vlo, vhi, plo, phi):
    ax.set_title(title, fontsize=13, fontweight='bold', pad=10)
    ax.set_xlabel('Volume (Normalized)', fontsize=11)
    ax.set_ylabel('Pressure (atm)', fontsize=11)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_ylim(plo, phi)
    ax.set_xlim(vlo, vhi)

# =============================================================================
# GRAPH 1: Idealized Lenoir Cycle Alone
# =============================================================================
fig1, ax1 = plt.subplots(figsize=(8, 5.5))

ax1.plot([V_bdc, V_bdc], [P1, P2_len], 'r-', lw=2.5, label='Ignition (+1000K)')
ax1.plot(V_len_exp, P_len_exp, 'b-', lw=2.5, label='Expansion to 1.5 atm')
ax1.plot([V_len_exp_end, V_bdc], [P1, P1], 'g--', lw=2.0, label='Exhaust / Return')

# Fill Work Area
ax1.fill_between(V_len_exp, P1, P_len_exp, color='orange', alpha=0.35, label='Net Work Integral')

format_ax(ax1, 'Idealized Lenoir Cycle (No Pre-Compression)', 0.8, 2.5, 0, 30)
ax1.legend(loc='upper right')
plt.tight_layout()

# =============================================================================
# GRAPH 2: Idealized Otto Cycle Alone
# =============================================================================
fig2, ax2 = plt.subplots(figsize=(8, 5.5))

# Lines
ax2.plot(V_otto_comp, P_otto_comp, 'k-', lw=2.5, label='5:1 Compression')
ax2.plot([V_tdc, V_tdc], [P2_otto, P3_otto], 'r-', lw=2.5, label='Ignition (+1000K)')
ax2.plot(V_otto_exp_std, P_otto_exp_std, 'b-', lw=2.5, label='5:1 Expansion')
ax2.plot(V_otto_exp_ext[V_otto_exp_ext >= V_bdc], P_otto_exp_ext[V_otto_exp_ext >= V_bdc], 
         'b--', lw=2.0, label='Expansion to 1.5 atm')
ax2.plot([1, 1], [1,P_otto_exp_std[-1]], 'g--', lw=2.0, label='Standard Otto')

# Extended Otto Net Work Fill (Main Loop + Extended Tail down to 1.0 atm)
mask_otto_main = (V_otto_exp_ext >= V_tdc) & (V_otto_exp_ext <= V_bdc)
mask_otto_tail = V_otto_exp_ext > V_bdc

# 1. Main loop area (above compression curve)
V_main_g2 = V_otto_exp_ext[mask_otto_main]
P_comp_g2 = np.interp(V_main_g2, V_otto_comp[::-1], P_otto_comp[::-1])
ax2.fill_between(V_main_g2, P_comp_g2, P_otto_exp_ext[mask_otto_main], 
                 color='mediumseagreen', alpha=0.35, label='Extended Otto Net Work')

# 2. Extended tail area (above 1.0 atm baseline)
ax2.fill_between(V_otto_exp_ext[mask_otto_tail], P1, P_otto_exp_ext[mask_otto_tail], 
                 color='mediumseagreen', alpha=0.35)

format_ax(ax2, 'Idealized Otto Cycle (With Extended Expansion)', 0, 1.9, 0, 30)
ax2.legend(loc='upper right')
plt.tight_layout()

# =============================================================================
# GRAPH 3: Direct Comparison (Lenoir vs. Otto)
# =============================================================================
fig3, ax3 = plt.subplots(figsize=(9, 6.5))

# 1. Lenoir Cycle Lines & Fill
ax3.plot([V_bdc, V_bdc], [P1, P2_len], color='red', linestyle='--', lw=2, label='Lenoir Ignition (+1000K)')
ax3.plot(V_len_exp, P_len_exp, color='red', linestyle='--', lw=2, label='Lenoir Expansion to 1.5 atm')
ax3.plot([V_len_exp_end, V_bdc], [P1, P1], color='red', linestyle=':', lw=1.5)
ax3.fill_between(V_len_exp, P1, P_len_exp, color='red', alpha=0.15, label='Lenoir Work Area')

# 2. Otto Cycle Lines
ax3.plot(V_otto_comp, P_otto_comp, color='black', lw=2.5, label='Otto Compression (5:1)')
ax3.plot([V_tdc, V_tdc], [P2_otto, P3_otto], color='blue', lw=2.5, label='Otto Ignition (+1000K)')
ax3.plot(V_otto_exp_ext, P_otto_exp_ext, color='blue', lw=2.5, label='Otto Expansion to 1.5 atm')
ax3.plot([V_exp_end, V_exp_end], [P_exp_end, P1], color='blue', linestyle=':', lw=1.5)
ax3.plot([V_exp_end, V_bdc], [P1, P1], color='blue', linestyle=':', lw=1.5)

# 3. Extended Otto Net Work Fill (Main Loop + Extended Tail down to 1.0 atm)
mask_main = (V_otto_exp_ext >= V_tdc) & (V_otto_exp_ext <= V_bdc)
mask_tail = V_otto_exp_ext > V_bdc

# Main Loop (V = 0.2 to 1.0)
V_main = V_otto_exp_ext[mask_main]
P_comp_match = np.interp(V_main, V_otto_comp[::-1], P_otto_comp[::-1])
ax3.fill_between(V_main, P_comp_match, P_otto_exp_ext[mask_main], 
                 color='dodgerblue', alpha=0.30, label='Otto Net Work Area')

# Over-expanded tail (V = 1.0 to V_exp_end) down to P1 (1.0 atm)
ax3.fill_between(V_otto_exp_ext[mask_tail], P1, P_otto_exp_ext[mask_tail], 
                 color='dodgerblue', alpha=0.30)

format_ax(ax3, 'Direct Comparison: Lenoir vs. Otto Cycle', 0, 2.5, 0, 30)
ax3.legend(loc='upper right', framealpha=0.9)
plt.tight_layout()

plt.show()