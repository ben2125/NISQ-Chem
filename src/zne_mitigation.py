# src/zne_mitigation.py
import numpy as np

class ErrorMitigator:
    """Applies Zero-Noise Extrapolation (ZNE) to recover the theoretical noise-free state."""
    
    def __init__(self, solver, optimal_params):
        self.solver = solver
        self.optimal_params = optimal_params
        self.measured_energies = []
        self.scale_factors = []

    def extrapolate(self, method='polynomial', degree=2):
        """Scales hardware noise and extrapolates back to zero."""
        print("--- Executing Zero-Noise Extrapolation ---")
        self.scale_factors = [1, 2, 3, 4]
        
        for scale in self.scale_factors:
            print(f"Sampling energy at {scale}x hardware noise...")
            # We use more shots (4096) to reduce statistical variance during mitigation
            energy = self.solver.evaluate_energy(self.optimal_params, scale=scale, custom_shots=4096)
            self.measured_energies.append(energy)
            
        if method == 'polynomial':
            poly_coefficients = np.polyfit(self.scale_factors, self.measured_energies, deg=degree)
            zne_energy = np.polyval(poly_coefficients, 0)
        else:
            raise ValueError("Currently only 'polynomial' extrapolation is supported.")
            
        # Calculate improvement metric if exact energy is known
        improvement = 0
        if self.solver.molecule.exact_energy is not None:
            exact = self.solver.molecule.exact_energy
            raw_error = abs(self.measured_energies[0] - exact)
            zne_error = abs(zne_energy - exact)
            if raw_error > 0:
                improvement = ((raw_error - zne_error) / raw_error) * 100
                
        return zne_energy, improvement
