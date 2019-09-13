from circuit_translate_main import dag_to_pyzx_circuit
from qiskit.converters import *
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit.dagcircuit import DAGCircuit
q = QuantumRegister(3, 'q')
q2 = QuantumRegister(2, 'a')
circ = QuantumCircuit(q, q2)
circ.h(q[0])
circ.cx(q[0], q[1])
circ.rz(0.5, q[1])
circ.h(q2[0])
dag = circuit_to_dag(circ)
dag_to_pyzx_circuit(dag)

