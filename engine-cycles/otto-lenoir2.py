import numpy as np
import matplotlib.pyplot as plt

# Constants
gamma = 1.4
p1 = 1.0        # Ambient pressure
v_min = 1.0     # Top Dead Center (TDC)
v_max = 5.0     # Bottom Dead Center (BDC)
q_in = 15.0     # Total Heat Input (Normalized)

# Initial Relative Temperature at (P1, V_max) set to 1.0
t1 = 1.0 

def get_p(v_start, p_start, v_array):
    return p_start * (v_start / v_array)**gamma

# --- OTTO CYCLE CALCULATIONS ---
# 1-2: Compression
v1_2 = np.linspace(v_max, v_min, 200)
p1_2 = get_p(v_max, p1, v1_2)
p2 = p1_2[-1]

# 2-3: Combustion (P3 = P2 + (gamma-1) * Q / V)
p3 = p2 + (gamma - 1) * q_in / v_min 
# Otto Peak Temp at P3, V_min
t_otto_peak = (p3 * v_min) / (p1 * v_max)

# 3-4: Expansion
v3_4 = np.linspace(v_min, v_max, 200)
p3_4 = get_p(v_min, p3, v3_4)
p4 = p3_4[-1]

work_otto = np.trapz(p3_4, v3_4) + np.trapz(p1_2, v1_2)

# --- LENOIR CYCLE CALCULATIONS ---
# L1-L2: Combustion at V_max
pl2 = p1 + (gamma - 1) * q_in / v_max
# Lenoir Peak Temp at PL2, V_max
t_lenoir_peak = (pl2 * v_max) / (p1 * v_max)

# L2-L3: Expansion
vl_final = v_max * (pl2 / p1)**(1/gamma)
vl_range = np.linspace(v_max, vl_final, 200)
pl_range = get_p(v_max, pl2, vl_range)

work_lenoir = np.trapz(pl_range, vl_range) - (p1 * (vl_final - v_max))

# --- PLOTTING ---
fig, ax = plt.subplots(figsize=(12, 7))

# Plot Otto (Warm colors)
ax.plot(v1_2, p1_2, color='orangered', lw=2, label='Otto: Compression')
ax.plot([v_min, v_min], [p2, p3], color='red', lw=2, label='Otto: Combustion')
ax.plot(v3_4, p3_4, color='chocolate', lw=2, label='Otto: Expansion')
ax.plot([v_max, v_max], [p4, p1], color='gold', lw=2, label='Otto: Exhaust')

# Plot Lenoir (Cool colors)
ax.plot([v_max, v_max], [p1, pl2], color='mediumblue', lw=2, label='Lenoir: Combustion')
ax.plot(vl_range, pl_range, color='deepskyblue', lw=2, label='Lenoir: Expansion')
ax.axhline(y=p1, color='navy', ls='--', alpha=0.3, label='Ambient Pressure')

# Label Peak Temperatures
ax.scatter([v_min], [p3], color='red', zorder=5)
ax.annotate(f'Otto Peak T: {t_otto_peak:.1f}x', xy=(v_min, p3), xytext=(v_min+0.2, p3),
            arrowprops=dict(arrowstyle='->', color='red'), color='darkred', fontweight='bold')

ax.scatter([v_max], [pl2], color='mediumblue', zorder=5)
ax.annotate(f'Lenoir Peak T: {t_lenoir_peak:.1f}x', xy=(v_max, pl2), xytext=(v_max+0.3, pl2+2),
            arrowprops=dict(arrowstyle='->', color='mediumblue'), color='blue', fontweight='bold')

# Place work numbers
ax.text(v_min + (v_max-v_min)*0.35, (p2+p3)*0.25, f'Otto Work:\n{work_otto:.2f}', 
        color='darkred', fontweight='bold', fontsize=12, ha='center', bbox=dict(facecolor='white', alpha=0.7))

ax.text(v_max + (vl_final-v_max)*0.35, (p1+pl2)*0.3, f'Lenoir Work:\n{work_lenoir:.2f}', 
        color='blue', fontweight='bold', fontsize=12, ha='center', bbox=dict(facecolor='white', alpha=0.7))

ax.set_title(f'PV Diagram: Otto vs Lenoir\nSame Heat Input', fontsize=14)
ax.set_xlabel('Volume (V)')
ax.set_ylabel('Pressure (P)')
ax.legend(loc='upper right')
ax.grid(True, alpha=0.2)

plt.tight_layout()
plt.show()