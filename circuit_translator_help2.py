from functools import singledispatch
from itertools import chain
from math import pi
from typing import Dict

import pyzx
import pyzx.circuit.gates as zx_g
import qiskit.extensions.standard as qk_g
from qiskit.circuit import Qubit
from qiskit.dagcircuit import DAGCircuit


@singledispatch
def get_op_qargs_from_pyzx(
        gate: pyzx.gates.Gate,
        pyreg_to_qubit: Dict[int, Qubit]):
    """Append the right qiskit op and qargs from the gate.

    The return is a list of such op and qargs.
    """
    raise NotImplementedError(
        f"Conversion from {type(gate)} to qiskit has not been implemented.")


@get_op_qargs_from_pyzx.register(zx_g.ZPhase)
def _f(gate: zx_g.ZPhase,
       pyreg_to_qubit: Dict[int, Qubit]):
    return [(
        qk_g.RZGate(float(gate.phase) * pi),
        [pyreg_to_qubit[gate.target]]
    )]


@get_op_qargs_from_pyzx.register(zx_g.Z)
def _f(gate: zx_g.Z,
       pyreg_to_qubit: Dict[int, Qubit]):
    return [(
        qk_g.ZGate(), [pyreg_to_qubit[gate.target]]
    )]


@get_op_qargs_from_pyzx.register(zx_g.S)
def _f(gate: zx_g.ZPhase,
       pyreg_to_qubit: Dict[int, Qubit]):
    return [(
        qk_g.SGate(), [pyreg_to_qubit[gate.target]]
    )]


@get_op_qargs_from_pyzx.register(zx_g.T)
def _f(gate: zx_g.T,
       pyreg_to_qubit: Dict[int, Qubit]):
    return [(
        qk_g.TGate(), [pyreg_to_qubit[gate.target]]
    )]


@get_op_qargs_from_pyzx.register(zx_g.XPhase)
def _f(gate: zx_g.XPhase,
       pyreg_to_qubit: Dict[int, Qubit]):
    return [(
        qk_g.RXGate(float(gate.phase) * pi),
        [pyreg_to_qubit[gate.target]]
    )]


@get_op_qargs_from_pyzx.register(zx_g.NOT)
def _f(gate: zx_g.NOT,
       pyreg_to_qubit: Dict[int, Qubit]):
    return [(
        qk_g.XGate(), [pyreg_to_qubit[gate.target]]
    )]


@get_op_qargs_from_pyzx.register(zx_g.HAD)
def _f(gate: zx_g.HAD,
       pyreg_to_qubit: Dict[int, Qubit]):
    return [(
        qk_g.HGate(), [pyreg_to_qubit[gate.target]]
    )]


@get_op_qargs_from_pyzx.register(zx_g.CNOT)
def _f(gate: zx_g.CNOT,
       pyreg_to_qubit: Dict[int, Qubit]):
    return [(
        qk_g.CnotGate(),
        [pyreg_to_qubit[gate.control], pyreg_to_qubit[gate.target]]
    )]


@get_op_qargs_from_pyzx.register(zx_g.CZ)
def _f(gate: zx_g.CZ,
       pyreg_to_qubit: Dict[int, Qubit]):
    return [(
        qk_g.CzGate(),
        [pyreg_to_qubit[gate.control], pyreg_to_qubit[gate.target]]
    )]


@get_op_qargs_from_pyzx.register(zx_g.CX)
def _f(gate: zx_g.CZ,
       pyreg_to_qubit: Dict[int, Qubit]):
    raise NotImplementedError("CX in PyZX is not the CNOT we know.")


@get_op_qargs_from_pyzx.register(zx_g.SWAP)
def _f(gate: zx_g.SWAP,
       pyreg_to_qubit: Dict[int, Qubit]):
    return [(
        qk_g.SwapGate(),
        [pyreg_to_qubit[gate.control], pyreg_to_qubit[gate.target]]
    )]


@get_op_qargs_from_pyzx.register(zx_g.Tofolli)
def _f(gate: zx_g.Tofolli,
       pyreg_to_qubit: Dict[int, Qubit]):
    return [(
        qk_g.ToffoliGate(),
        [pyreg_to_qubit[gate.ctrl1],
         pyreg_to_qubit[gate.ctrl2],
         [gate.target]]
    )]


@get_op_qargs_from_pyzx.register(zx_g.CCZ)
def _f(gate: zx_g.CCZ,
       pyreg_to_qubit: Dict[int, Qubit]):
    basic_gates = gate.to_basic_gates()
    basic_gates = [
        get_op_qargs_from_pyzx(bg, pyreg_to_qubit)
        for bg in basic_gates
    ]
    return list(chain.from_iterable(basic_gates))


def add_normal_gate(
        gate: pyzx.gates.Gate,
        pyreg_to_qubit: Dict[int, Qubit],
        dagcircuit: DAGCircuit):
    op_qargs_list = get_op_qargs_from_pyzx(gate, pyreg_to_qubit)
    for op, qarg in op_qargs_list:
        dagcircuit.apply_operation_back(
            op=op,
            qargs=qarg,
            cargs=[],
            condition=None
        )
