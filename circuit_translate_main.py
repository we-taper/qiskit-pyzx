from collections import OrderedDict, namedtuple
from typing import Dict

import pyzx
from pyzx.circuit import Circuit
from qiskit.circuit import ClassicalRegister, QuantumCircuit, QuantumRegister, \
    Qubit
from qiskit.dagcircuit import DAGCircuit

from circuit_translator import check_classical_control, to_pyzx_gate, \
    add_non_unitary_gate

Translated = namedtuple(
    'Translated', ['circuit',
                   'qreg_to_pyreg_range',
                   'pyreg_range_to_qreg',
                   'qregs', 'cregs'
                   ])


def dag_to_pyzx_circuit(dag: DAGCircuit):
    """Build a ``QuantumCircuit`` object from a ``DAGCircuit``.

    Args:
        dag (DAGCircuit): the input dag.

    Return:
        QuantumCircuit: the circuit representing the input dag.
    """
    # In Qiskit, the quantum registers can have many diff names, whereas in PyZX circuit, there is only one global qubits.
    # We need a mapping from the global qubits back to the named qubits
    pyreg_range_to_qreg = dict()  # map the start idx of the named qreg to the qreg
    qreg_to_pyreg_range = dict()  # maps the qreg name to the start idx of global qreg
    tot_qb_count = 0

    qregs = OrderedDict()
    for qreg in dag.qregs.values():
        qreg_tmp = QuantumRegister(qreg.size, name=qreg.name)
        qregs[qreg.name] = qreg_tmp
        pyreg_range_to_qreg[tot_qb_count] = qreg
        qreg_to_pyreg_range[qreg.name] = tot_qb_count
        tot_qb_count += qreg.size

    cregs = OrderedDict()
    for creg in dag.cregs.values():
        creg_tmp = ClassicalRegister(creg.size, name=creg.name)
        cregs[creg.name] = creg_tmp

    gates = []

    for node in dag.topological_op_nodes():
        # collects the qregs
        qubits = [
            qreg_to_pyreg_range[qubit.register.name] + qubit.index
            for qubit in node.qargs
        ]

        # collects the cregs, which is passed (without conversion) to PyZX
        clbits = []
        for clbit in node.cargs:
            clbits.append(cregs[clbit.register.name][clbit.index])

        # if node.condition is not None:
        #     raise NotImplementedError(f"Classical control is not supported by PyZX")
        inst = node.op
        if check_classical_control(inst, qubits, gates,
                                   clbits=clbits, condition=node.condition):
            pass
        else:
            to_pyzx_gate(inst, qubits, gates,
                         clbits=clbits, condition=node.condition)

    name = '' if dag.name is None else str(dag.name)
    circuit = Circuit(tot_qb_count, name=name)
    circuit.gates = gates
    return Translated(
        circuit, qreg_to_pyreg_range, pyreg_range_to_qreg,
        list(qregs.values()), list(cregs.values()))


def pyzx_circ_to_dag(
        circ: pyzx.circuit.Circuit, translated: Translated):
    dagcircuit = DAGCircuit()
    dagcircuit.name = circ.name
    pyreg_range_to_qreg = translated.pyreg_range_to_qreg
    # produce a lookup table from the pyreg_range_to_qreg
    # TODO(hx) Maybe we should do this inside dag_to_pyzx_circuit
    pyreg_to_qubit = dict()
    for start_idx, qreg in pyreg_range_to_qreg.items():
        for idx in range(start_idx, qreg.size):
            pyreg_to_qubit[idx] = qreg[idx - start_idx]

    [dagcircuit.add_qreg(qreg) for qreg in translated.qregs]
    [dagcircuit.add_creg(creg) for creg in translated.cregs]

    instructions = []
    for gate in circ.gates:
        if add_non_unitary_gate(
                gate, pyreg_to_qubit, dagcircuit):
            pass
        else:
            add_normal_gate(gate, pyreg_to_qubit, dagcircuit)
