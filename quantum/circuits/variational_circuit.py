import pennylane as qml


def variational_layer(weights, wires):

    for i in range(len(wires)):
        qml.RY(weights[i], wires=wires[i])

    for i in range(len(wires) - 1):
        qml.CNOT(wires=[wires[i], wires[i + 1]])