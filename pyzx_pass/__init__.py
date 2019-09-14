import pyzx
from qiskit.transpiler.basepasses import BasePass

from circuit_translate_main import dag_to_pyzx_circuit, pyzx_circ_to_dag

__all__ = ['optimize', 'PyZXPass']


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


class PyZXPass(BasePass):

    def __init__(self):
        super(PyZXPass, self).__init__()
        self._hash = id(self)

    def run(self, dag):
        translated = dag_to_pyzx_circuit(dag)
        optimized = optimize(translated.circuit)
        dag = pyzx_circ_to_dag(optimized, translated)
        return dag
