from qiskit import QuantumCircuit

def build_standard_circuit(x, th):
    qc = QuantumCircuit(2)
    qc.ry(x[0], 0)
    qc.ry(x[1], 1)
    qc.ry(th[0], 0)
    qc.ry(th[1], 1)
    qc.cx(0, 1)
    qc.ry(th[2], 0)
    qc.ry(th[3], 1)
    qc.cx(1, 0)
    qc.ry(th[4], 0)
    qc.ry(th[5], 1)
    return qc