import networkx as nx
from qiskit.circuit import QuantumCircuit
from qiskit.converters import circuit_to_dag, dag_to_circuit

# Making first circuit: bell state
qc1 = QuantumCircuit(2, 2, name="bell")
qc1.h(0)
qc1.cx(0, 1)
qc1.measure([0, 1], [0, 1])

print(qc1)
dag = circuit_to_dag(qc1)

# we can get a networkx DAG graph form it:
dag_nx = dag.to_networkx()
print(f"Confirm from networkx that this is a DAG graph: {nx.is_directed_acyclic_graph(dag_nx)}")


# some function which optimize dag


qc2 = dag_to_circuit(dag)

print(qc2)
