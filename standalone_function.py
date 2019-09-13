import qiskit
import pyzx

def pyzx_optimize(circuit: qiskit.QuantumCircuit) -> qiskit.QuantumCircuit:
    parser = pyzx.circuit.qasmparser.QASMParser()
    pyzx_graph = parser.parse(circuit.qasm()).to_graph()

    # Phase 1
    pyzx.simplify.full_reduce(pyzx_graph)

    # Phase 2
    pyzx_circuit = pyzx.extract.streaming_extract(pyzx_graph)

    # Phase 3
    pyzx_circuit = pyzx_circuit.to_basic_gates()

    # Phase 4
    pyzx_circuit = pyzx.optimize.basic_optimization(pyzx_circuit)

    # Phase 5
    pyzx_circuit = pyzx_circuit.to_basic_gates()

    # Phase 6
    pyzx_circuit = pyzx_circuit.split_phase_gates()

    result = qiskit.QuantumCircuit.from_qasm_str(pyzx_circuit.to_qasm())
    result.name = "{}_zx_optimized".format(circuit.name)
    return result
