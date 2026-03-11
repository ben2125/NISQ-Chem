# main.py
from src.molecule import QuantumMolecule
from src.vqe_engine import VQESolver
from src.zne_mitigation import ErrorMitigator

if __name__ == "__main__":
    print("\n========================================================")
    print(" NISQ-Chem: AI-Orchestrated Quantum Error Mitigation")
    print("========================================================\n")

    # 1. Initialize Hamiltonian
    h2 = QuantumMolecule.hydrogen_model()
    
    if h2.exact_energy:
        print(f"Target Exact Ground State: {h2.exact_energy:.5f} Hartree\n")

    # 2. Execute VQE under simulated hardware noise
    solver = VQESolver(molecule=h2, optimizer='COBYLA')
    optimal_params, noisy_energy = solver.run()

    # 3. Apply Zero-Noise Extrapolation
    mitigator = ErrorMitigator(solver=solver, optimal_params=optimal_params)
    zne_energy, improvement = mitigator.extrapolate(method='polynomial', degree=2)

    print("\n--- Final Results ---")
    print(f"Raw Noisy Energy:     {noisy_energy:.5f} Hartree")
    print(f"ZNE Mitigated Energy: {zne_energy:.5f} Hartree")
    print(f"Error Mitigated By:   {improvement:.1f}%")
