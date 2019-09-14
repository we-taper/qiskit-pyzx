import qiskit
import pyzx

from qiskit.converters import circuit_to_dag, dag_to_circuit
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

def pyzx_optimize(circuit: qiskit.QuantumCircuit) -> qiskit.QuantumCircuit:
    ret = dag_to_pyzx_circuit(circuit_to_dag(circuit))
    pyzx_circuit = ret.circuit

    reduced = optimize(ret.circuit)

    dag = pyzx_circ_to_dag(reduced, ret)
    result = dag_to_circuit(dag)
    result.name = "{}_zx_optimized".format(circuit.name)
    return result
