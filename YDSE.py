import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# -----------------------
# Constants
# -----------------------
I0 = 1
y = np.linspace(-0.01, 0.01, 2000)

# =========================================================
# Intensity Function
# =========================================================
def calculate_intensity(wavelength, y, d, L, I0):
    phase = (np.pi * d * y) / (wavelength * L)
    return 4 * I0 * (np.cos(phase))**2

# =========================================================
# Fringe Pattern
# =========================================================
def show_fringe_pattern(wavelength, wavelength_nm, d, L):
    Y, X = np.meshgrid(y, np.linspace(0, 1, 300))
    phase = (np.pi * d * Y) / (wavelength * L)
    pattern = 4 * I0 * (np.cos(phase))**2

    plt.figure()
    plt.imshow(pattern, extent=[-10, 10, 0, 1], aspect='auto')
    plt.title(f"Fringe Pattern (λ = {wavelength_nm} nm)")
    plt.text(-9, 0.8, f"λ = {wavelength_nm} nm", color='white')
    plt.xlabel("Position (mm)")
    plt.yticks([])
    plt.show()

# =========================================================
# OPTION 1: Interactive Simulation
# =========================================================
def run_interactive_simulation():
    wavelength_nm_init = 500
    d_init = 0.3e-3
    L_init = 1.5

    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0.1, bottom=0.3)

    wavelength = wavelength_nm_init * 1e-9
    intensity = calculate_intensity(wavelength, y, d_init, L_init, I0)

    line, = ax.plot(y * 1000, intensity)

    ax.set_xlabel("Position (mm)")
    ax.set_ylabel("Intensity")
    ax.set_title("Interactive Study of Single Wavelength")
    ax.grid()

    # -------- Fringe Orders --------
    def draw_orders(wavelength, d, L):
        for txt in ax.texts:
            txt.remove()

        beta = (wavelength * L) / d

        for m in range(-3, 4):
            y_m = m * beta * 1000
            if -10 < y_m < 10:
                ax.axvline(x=y_m, linestyle=':', alpha=0.5)
                ax.text(y_m, max(line.get_ydata())*0.8, f"m={m}", ha='center', fontsize=8)

    draw_orders(wavelength, d_init, L_init)

    # -------- Sliders --------
    ax_lambda = plt.axes([0.1, 0.2, 0.8, 0.03])
    ax_d = plt.axes([0.1, 0.15, 0.8, 0.03])
    ax_L = plt.axes([0.1, 0.1, 0.8, 0.03])

    slider_lambda = Slider(ax_lambda, 'Wavelength (nm)', 1, 700, valinit=wavelength_nm_init)
    slider_d = Slider(ax_d, 'd (mm)', 0.01, 1.0, valinit=d_init*1000)
    slider_L = Slider(ax_L, 'L (m)', 0.1, 3.0, valinit=L_init)

    # -------- Update --------
    def update(val):
        wavelength_nm = slider_lambda.val
        d_mm = slider_d.val
        L = slider_L.val

        wavelength = wavelength_nm * 1e-9
        d = d_mm * 1e-3

        new_intensity = calculate_intensity(wavelength, y, d, L, I0)

        line.set_ydata(new_intensity)
        ax.set_title(f"λ={wavelength_nm:.1f} nm | d={d_mm:.2f} mm | L={L:.2f} m")

        draw_orders(wavelength, d, L)
        fig.canvas.draw_idle()

    slider_lambda.on_changed(update)
    slider_d.on_changed(update)
    slider_L.on_changed(update)

    plt.show()

# =========================================================
# OPTION 2: Compare Two Wavelengths
# =========================================================
def compare_wavelengths():
    w1 = float(input("Enter first wavelength (nm): "))
    w2 = float(input("Enter second wavelength (nm): "))

    lambda1 = w1 * 1e-9
    lambda2 = w2 * 1e-9

    d = 0.3e-3
    L = 1.5

    I1 = calculate_intensity(lambda1, y, d, L, I0)
    I2 = calculate_intensity(lambda2, y, d, L, I0)

    plt.figure()
    plt.plot(y * 1000, I1, label=f"{w1} nm")
    plt.plot(y * 1000, I2, label=f"{w2} nm")
    plt.xlabel("Position (mm)")
    plt.ylabel("Intensity")
    plt.title("Comparison of Two Wavelengths")
    plt.grid()
    plt.legend()
    plt.show()

    # Fringe option
    if input("Show fringe patterns? (y/n): ").lower() == 'y':
        show_fringe_pattern(lambda1, w1, d, L)
        show_fringe_pattern(lambda2, w2, d, L)

# =========================================================
# MAIN PROGRAM
# =========================================================
print("=== Young Double Slit Simulator ===")
print("1. Interactive Study of Single Wavelength")
print("2. Compare Two Wavelengths")

try:
    choice = int(input("Enter your choice (1/2): "))

    if choice == 1:
        run_interactive_simulation()

    elif choice == 2:
        compare_wavelengths()

    else:
        print("Invalid choice")

except:
    print("Invalid input")
