from functools import singledispatch
from math import pi

import pyzx.circuit.gates as pyzx_g
import qiskit.extensions.standard as qk_g


# from .barrier import Barrier
# from .cswap import FredkinGate
# from .cy import CyGate
# from .u0 import U0Gate
# from .cu1 import Cu1Gate
# from .ch import CHGate
# from .cu3 import Cu3Gate
# from .rzz import RZZGate

# from .crz import CrzGate
# from .u1 import U1Gate
# from .u2 import U2Gate
# from .u3 import U3Gate


@singledispatch
def to_pyzx_gate(qiskit_gate, targets, gatelist: list):
    raise NotImplementedError(
        f"The gate {type(qiskit_gate)} have not been implemented.")


@to_pyzx_gate.register(qk_g.ToffoliGate)
def to_pyzx_gate_1(qiskit_gate, targets, gatelist: list):
    return gatelist.append(
        pyzx_g.Tofolli(ctrl1=targets[0], ctrl2=targets[1], target=targets[2]))


@to_pyzx_gate.register(qk_g.CnotGate)
def to_pyzx_gate_2(qiskit_gate, targets, gatelist: list):
    return gatelist.append(pyzx_g.CNOT(control=targets[0], target=targets[1]))


# TODO: what is the diff btw cxbase and cnotgate?
@to_pyzx_gate.register(qk_g.CXBase)
def to_pyzx_gate_3(qiskit_gate, targets, gatelist: list):
    return gatelist.append(pyzx_g.CNOT(control=targets[0], target=targets[1]))


@to_pyzx_gate.register(qk_g.CyGate)
def to_pyzx_gate_4(qiskit_gate, targets, gatelist: list):
    raise NotImplementedError(
        f"TODO: implement the rule from CY to CXCZCPhase")


@to_pyzx_gate.register(qk_g.CzGate)
def to_pyzx_gate_5(qiskit_gate, targets, gatelist: list):
    gatelist.append(pyzx_g.CZ(control=targets[0], target=targets[1]))


@to_pyzx_gate.register(qk_g.SwapGate)
def to_pyzx_gate_6(qiskit_gate, targets, gatelist: list):
    gatelist.append(pyzx_g.SWAP(control=targets[0], target=targets[1]))


@to_pyzx_gate.register(qk_g.HGate)
def to_pyzx_gate_7(qiskit_gate, targets, gatelist: list):
    gatelist.append(pyzx_g.HAD(target=targets[0]))


@to_pyzx_gate.register(qk_g.IdGate)
def to_pyzx_gate_7(qiskit_gate, targets, gatelist: list):
    pass


@to_pyzx_gate.register(qk_g.SGate)
def to_pyzx_gate_8(qiskit_gate, targets, gatelist: list):
    gatelist.append(pyzx_g.S(target=targets[0]))


@to_pyzx_gate.register(qk_g.SdgGate)
def to_pyzx_gate_9(qiskit_gate, targets, gatelist: list):
    gatelist.append(pyzx_g.S(target=targets[0], adjoint=True))


@to_pyzx_gate.register(qk_g.TGate)
def to_pyzx_gate_9(qiskit_gate, targets, gatelist: list):
    gatelist.append(pyzx_g.T(target=targets[0]))


@to_pyzx_gate.register(qk_g.TdgGate)
def to_pyzx_gate_9(qiskit_gate, targets, gatelist: list):
    gatelist.append(pyzx_g.T(target=targets[0], adjoint=True))


@to_pyzx_gate.register(qk_g.XGate)
def to_pyzx_gate_9(qiskit_gate, targets, gatelist: list):
    gatelist.append(pyzx_g.XPhase(target=targets[0], phase=pi))


@to_pyzx_gate.register(qk_g.YGate)
def to_pyzx_gate_9(qiskit_gate, targets, gatelist: list):
    gatelist.extend([
        pyzx_g.XPhase(target=targets[0], phase=pi),
        pyzx_g.Z(target=targets[0])
    ])


@to_pyzx_gate.register(qk_g.ZGate)
def to_pyzx_gate_9(qiskit_gate, targets, gatelist: list):
    gatelist.append(pyzx_g.Z(target=targets[0]))


@to_pyzx_gate.register(qk_g.RXGate)
def to_pyzx_gate_9(qiskit_gate: qk_g.RXGate, targets, gatelist: list):
    gatelist.append(
        pyzx_g.XPhase(target=targets[0],
                      phase=get_angle(qiskit_gate.params[0])))


@to_pyzx_gate.register(qk_g.RYGate)
def to_pyzx_gate_9(qiskit_gate: qk_g.RYGate, targets, gatelist: list):
    # YRot = SRx(theta)Sdg
    gatelist.extend([
        pyzx_g.S(target=targets[0]),
        pyzx_g.XPhase(target=targets[0],
                      phase=get_angle(qiskit_gate.params[0])),
        pyzx_g.S(target=targets[0], adjoint=True),
    ])


@to_pyzx_gate.register(qk_g.RZGate)
def to_pyzx_gate_9(qiskit_gate: qk_g.RZGate, targets, gatelist: list):
    gatelist.append(
        pyzx_g.ZPhase(target=targets[0],
                      phase=get_angle(qiskit_gate.params[0])))


def get_angle(angle):
    # 1. qiskit stores angle in Sympy.Float, which is not allowed by PyZX
    # 2. angle in pyZX is in ratios of pi
    angle = float(angle)
    angle /= pi
    return angle
