# src/molecule.py
from qiskit.quantum_info import SparsePauliOp

class QuantumMolecule:
    """Represents the target molecule and its quantum mechanical Hamiltonian."""
    
    def __init__(self, name, hamiltonian, exact_energy=None):
        self.name = name
        self.hamiltonian = hamiltonian
        self.exact_energy = exact_energy

    @classmethod
    def hydrogen_model(cls):
        """Returns the pre-computed 2-qubit Hamiltonian for H2."""
        h2_hamiltonian = SparsePauliOp.from_list([
            ("II", -1.052373245772859),
            ("IZ", 0.39793742484318045),
            ("ZI", -0.39793742484318045),
            ("ZZ", -0.01128010425623538),
            ("XX", 0.18093119978423156)
        ])
        # Exact ground state energy in Hartrees
        exact_energy = -1.85727503
        
        return cls(name="H2", hamiltonian=h2_hamiltonian, exact_energy=exact_energy)
