# src/visualization.py
import matplotlib.pyplot as plt
import numpy as np

class QuantumDashboard:
    """Generates professional-grade diagnostic plots for VQE and ZNE results."""
    
    @staticmethod
    def generate_report(energy_history, zne_data, molecule_name="H2"):
        """
        Creates a dual-panel visual report.
        zne_data: dict containing 'scales', 'energies', 'exact', 'zne_val', 'poly_coeffs'
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # --- Panel 1: VQE Convergence ---
        ax1.plot(energy_history, color='tab:red', linewidth=1.5, alpha=0.8, label='Noisy VQE Trajectory')
        ax1.axhline(y=zne_data['exact'], color='black', linestyle='--', label='Exact Ground State')
        ax1.set_title(f"VQE Convergence: {molecule_name} under Hardware Noise", fontsize=13)
        ax1.set_xlabel("Optimization Iteration")
        ax1.set_ylabel("Energy (Hartrees)")
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # --- Panel 2: ZNE Extrapolation ---
        scales = zne_data['scales']
        energies = zne_data['energies']
        poly = zne_data['poly_coeffs']
        
        # Plot raw noisy points
        ax2.scatter(scales, energies, color='red', s=80, label='Measured Noisy Points', zorder=5)
        
        # Plot the extrapolation curve
        x_fit = np.linspace(0, max(scales), 100)
        y_fit = np.polyval(poly, x_fit)
        ax2.plot(x_fit, y_fit, color='tab:orange', linestyle='--', label='Quadratic Fit')
        
        # Highlight the Zero-Noise Prediction
        ax2.scatter([0], [zne_data['zne_val']], color='green', marker='*', s=250, label='ZNE Prediction', zorder=6)
        ax2.axhline(y=zne_data['exact'], color='black', linestyle=':', alpha=0.6, label='Theoretical Truth')
        
        ax2.set_title("Zero-Noise Extrapolation (ZNE) Mitigation", fontsize=13)
        ax2.set_xlabel("Noise Scale Factor (λ)")
        ax2.set_ylabel("Extrapolated Energy")
        ax2.set_xlim(-0.2, max(scales) + 0.5)
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig("vqe_zne_report.png", dpi=300)
        print("\n[SUCCESS] Diagnostic report saved as 'vqe_zne_report.png'")
        plt.show()
