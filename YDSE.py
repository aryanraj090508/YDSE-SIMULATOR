import numpy as np
import matplotlib.pyplot as plt

# -----------------------
# Constants
# -----------------------
d = 0.3e-3   # slit distance (m)
L = 1.5      # screen distance (m)
I0 = 1       # intensity of one slit

# -----------------------
# Screen points
# -----------------------
y = np.linspace(-0.01, 0.01, 2000)

# =========================================================
# FUNCTION: Calculate Intensity
# =========================================================
def calculate_intensity(wavelength, y, d, L, I0):
    phase = (np.pi * d * y) / (wavelength * L)
    return 4 * I0 * (np.cos(phase))**2

# =========================================================
# FUNCTION: Plot Graph
# =========================================================
def plot_graph(y, intensity, label=None, title=""):
    plt.plot(y * 1000, intensity, label=label)
    plt.xlabel("Position on Screen (mm)")
    plt.ylabel("Intensity (relative units)")
    plt.title(title)
    plt.grid()
    
    # Central fringe marker
    plt.axvline(x=0, linestyle=':', label="Central Fringe")

    if label:
        plt.legend()

# =========================================================
# FUNCTION: Show Fringe Pattern (WITH LABEL)
# =========================================================
def show_fringe_pattern(wavelength, wavelength_nm):
    Y, X = np.meshgrid(y, np.linspace(0, 1, 300))
    phase = (np.pi * d * Y) / (wavelength * L)
    pattern = 4 * I0 * (np.cos(phase))**2

    plt.figure()
    plt.imshow(pattern, extent=[-10, 10, 0, 1], aspect='auto')

    # 👇 Title with wavelength
    plt.title(f"Fringe Pattern (λ = {wavelength_nm} nm)")

    # 👇 Label inside image (extra clarity)
    plt.text(-9, 0.8, f"λ = {wavelength_nm} nm", color='white', fontsize=10)

    plt.xlabel("Position (mm)")
    plt.yticks([])
    plt.show()

# =========================================================
# MAIN PROGRAM
# =========================================================
print("=== Young Double Slit Simulator ===")
print("1. Study Single Wavelength")
print("2. Compare Two Wavelengths")

try:
    choice = int(input("Enter your choice (1 or 2): "))

    # =====================================================
    # OPTION 1: Single Wavelength
    # =====================================================
    if choice == 1:
        wavelength_nm = float(input("Enter wavelength (in nm): "))
        wavelength = wavelength_nm * 1e-9

        beta = (wavelength * L) / d
        intensity = calculate_intensity(wavelength, y, d, L, I0)

        print("\n--- Results ---")
        print(f"Wavelength: {wavelength_nm} nm")
        print(f"Fringe width (β = λL/d): {beta*1000:.3f} mm")
        print(f"Maximum intensity: {np.max(intensity):.2f} (relative units)")

        plt.figure()
        plot_graph(y, intensity, title="Interference Pattern")
        plt.show()

        show = input("Do you want to see fringe pattern? (y/n): ")
        if show.lower() == 'y':
            show_fringe_pattern(wavelength, wavelength_nm)

    # =====================================================
    # OPTION 2: Compare Two Wavelengths
    # =====================================================
    elif choice == 2:
        lambda1_nm = float(input("Enter first wavelength (in nm): "))
        lambda2_nm = float(input("Enter second wavelength (in nm): "))

        lambda1 = lambda1_nm * 1e-9
        lambda2 = lambda2_nm * 1e-9

        beta1 = (lambda1 * L) / d
        beta2 = (lambda2 * L) / d

        I1 = calculate_intensity(lambda1, y, d, L, I0)
        I2 = calculate_intensity(lambda2, y, d, L, I0)

        print("\n--- Results ---")
        print(f"Wavelength 1: {lambda1_nm} nm | Fringe width: {beta1*1000:.3f} mm")
        print(f"Wavelength 2: {lambda2_nm} nm | Fringe width: {beta2*1000:.3f} mm")

        plt.figure()
        plot_graph(y, I1, label=f"{lambda1_nm} nm", title="Wavelength Comparison")
        plot_graph(y, I2, label=f"{lambda2_nm} nm")
        plt.legend()
        plt.show()

        show = input("Do you want to see fringe patterns? (y/n): ")
        if show.lower() == 'y':
            show_fringe_pattern(lambda1, lambda1_nm)
            show_fringe_pattern(lambda2, lambda2_nm)

    else:
        print("Invalid choice.")

except:
    print("Invalid input. Please enter numbers only.")
