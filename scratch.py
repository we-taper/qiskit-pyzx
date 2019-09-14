from math import pi

import pyzx
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.converters import *

from circuit_translate_main import dag_to_pyzx_circuit, pyzx_circ_to_dag


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
q_a = QuantumRegister(2, 'a')
c = ClassicalRegister(1, 'c')
circ = QuantumCircuit(q, q_a, c)
# circ.rz(0.1 * pi, q[1])
# circ.cx(q[0], q[1])
# circ.measure(q[0], c[0])
# circ.measure(q[0], c[0])
# circ.measure(q[0], c[0])
# circ.rz(0.2 * pi, q[1])
# circ.cx(q[0], q[1])
# circ.rz(0.3 * pi, q[0])
# circ.x(q[0]).c_if(c, 1)
# circ.rz(0.4 * pi, q[1])
# circ.cx(q[1], q[0])
# circ.h(q_a[0])
# circ.h(q_a[0])
# circ.x(q_a[0])
# circ.rx(pi, q_a[1])
# circ.ry(pi, q_a[1])
# circ.rz(0.1 * pi, q_a[1])
circ.z(q[1])
circ.cx(q[1], q[0])
# circ.measure(q[0], c[0])
circ.reset(q[0])
circ.cx(q[1], q[0])
circ.z(q[1])
print('Before circ')
print(circ.qasm())
dag = circuit_to_dag(circ)
ret = dag_to_pyzx_circuit(dag)
print('pyzx circ (before opt)')
print(ret.circuit.to_qasm())
reduced = optimize(ret.circuit)
print('pyzx circ (after opt)')
print(reduced.to_qasm())
dag_new = pyzx_circ_to_dag(reduced, ret)
print('circ (after opt)')
print(dag_to_circuit(dag_new).qasm())
# =======
# reduced = optimize(ret[0])

# for gate in reduced.gates:
#     if isinstance(gate, pyzx.gates.Nonunitary):
#         print(gate.stored_data)

# print(reduced.to_qasm())
# >>>>>>> Stashed changes
