from functools import singledispatch
import qiskit.extensions.standard as qk_g
import pyzx.circuit.gates as pyzx_g

# from .barrier import Barrier
# from .ccx import ToffoliGate
# from .cswap import FredkinGate
# from .cx import CnotGate
# from .cxbase import CXBase
# from .cy import CyGate
# from .cz import CzGate
# from .swap import SwapGate
# from .h import HGate
# from .iden import IdGate
# from .s import SGate
# from .s import SdgGate
# from .t import TGate
# from .t import TdgGate
# from .u0 import U0Gate
# from .u1 import U1Gate
# from .u2 import U2Gate
# from .u3 import U3Gate
# from .ubase import UBase
# from .x import XGate
# from .y import YGate
# from .z import ZGate
# from .rx import RXGate
# from .ry import RYGate
# from .rz import RZGate
# from .cu1 import Cu1Gate
# from .ch import CHGate
# from .crz import CrzGate
# from .cu3 import Cu3Gate
# from .rzz import RZZGate



@singledispatch
def to_pyzx_gate(qiskit_gate, targets, *args):
    raise NotImplementedError(f"The gate {type(qiskit_gate)} have not been implemented.")


@to_pyzx_gate.register(qk_g.ToffoliGate)
def to_pyzx_gate_1(qiskit_gate, targets, *args):
    return pyzx_g.Tofolli()