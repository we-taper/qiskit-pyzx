from math import pi

import pyzx
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.converters import *

from circuit_translate_main import dag_to_pyzx_circuit


def optimize(c):
    pyzx_graph = c.to_graph()

    # Phase 1
    pyzx.simplify.full_reduce(pyzx_graph)

    # Phase 2
    pyzx_circuit = pyzx.extract.streaming_extract(pyzx_graph)

    # Phase 3
    pyzx_circuit = pyzx_circuit.to_basic_gates()

    # Phase 4
    try:
        # First try including the phase polynomial optimizer
        pyzx_circuit = pyzx.optimize.full_optimize(pyzx_circuit)
    except TypeError:
        # The phase polynomial optimizer only works on Clifford+T circuits.
        # Fall back to the basic optimizer
        pyzx_circuit = pyzx.optimize.basic_optimization(pyzx_circuit)

    # Phase 5
    pyzx_circuit = pyzx_circuit.to_basic_gates()

    # Phase 6
    pyzx_circuit = pyzx_circuit.split_phase_gates()

    return pyzx_circuit


q = QuantumRegister(2, 'q')
q2 = QuantumRegister(2, 'a')
circ = QuantumCircuit(q, q2)
circ.rz(0.1 * pi, q[1])
circ.cx(q[0], q[1])
circ.rz(0.2 * pi, q[1])
circ.cx(q[0], q[1])
circ.rz(0.3 * pi, q[0])
circ.rz(0.4 * pi, q[1])
circ.cx(q[1], q[0])
dag = circuit_to_dag(circ)
ret = dag_to_pyzx_circuit(dag)
reduced = optimize(ret[0])
