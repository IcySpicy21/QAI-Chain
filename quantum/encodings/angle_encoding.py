import pennylane as qml


def angle_encoding(x, wires):

    qml.AngleEmbedding(x, wires=wires)