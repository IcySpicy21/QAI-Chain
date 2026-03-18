import pennylane as qml


def get_device(n_qubits=4):
    return qml.device("default.qubit", wires=n_qubits)