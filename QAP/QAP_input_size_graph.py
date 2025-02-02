import QAP.QAP_nonlinear as QAP_nonlinear
import QAP_classical
import QAP.QAP_cqm as QAP_cqm
import QAP.matrix_gen as matrix_gen
import time
import matplotlib.pyplot as plt
"""
# Initialize state variables
N_rooms = 3 #number of rooms (receive supplies)
N_supply = 3 #number of supply closets (give supplies)
max_flow = 100 #maximum value of flow from a given supply closet to each room
max_distance = 1 #maximum distance between any two points in the graph
time_steps = 5 #number of times the flow matrix changes
penalty = 10 # penalty for moving
iterations = 4

cqm_objectives = []
nl_objectives = []
classical_objectives = []
room_sizes = []

for i in range(iterations):
    # define flow matrix and distance matrices
    # we use three small distance matrices instead of one large one since we do not need all the distances
    flow = helper.random_time_matrix(time_steps, N_supply, N_rooms, max_flow)
    room_supply_distance = helper.random_matrix(N_supply, N_rooms, max_distance)
    room_room_distance = helper.random_symmetric_matrix(N_rooms, 0, max_distance)
    supply_supply_distance = helper.random_symmetric_matrix(N_supply, 0, max_distance)

    # Call the quantum solution
    start_time = time.time()
    cqm_objective = cqm_qap_hospital.quantum_solution(N_rooms, N_supply, flow, room_supply_distance, room_room_distance, supply_supply_distance, time_steps, penalty)[1]
    cqm_time = time.time()-start_time
    start_time = time.time()
    nl_objective = QAP_hospital.quantum_solution2(N_rooms, N_supply, flow, room_supply_distance, room_room_distance, supply_supply_distance, time_steps, penalty)
    nl_time = time.time() - start_time
    start_time = time.time()
    classical_objective = QAP_classical.classical_solution(N_rooms, N_supply, flow, room_supply_distance, room_room_distance, supply_supply_distance, time_steps, penalty)
    classical_time = time.time() - start_time

    cqm_objectives.append(cqm_objective)
    nl_objectives.append(nl_objective)
    classical_objectives.append(classical_objective)

    room_sizes.append(N_rooms)

    N_rooms *= 2
    N_supply *= 2


print(cqm_objectives)
print(nl_objectives)
print(classical_objectives)
"""
room_sizes = [3, 6, 12, 24]
cqm_objectives = [1003.1519595884798, 3934.1774818203467, 13956.00198680342, 59293.213775978]
nl_objectives = [1188.05985978, 4866.90236137, 18759.86743135, 78650.40743452]
classical_objectives = [1523.3569096441408, 6050.677949927152, 23436.134552905274, 95157.7262519355]


sums = [c + n + cl for c, n, cl in zip(cqm_objectives, nl_objectives, classical_objectives)]
cqm_objectives = [c/cl for c, cl in zip(cqm_objectives, sums)]
nl_objectives = [n/c for n, c in zip(nl_objectives, sums)]
classical_objectives = [n/c for n, c in zip(classical_objectives, sums)]

# Create the scatter plot
plt.plot(room_sizes, cqm_objectives, c='blue', label='Constrained Quantum Model')
plt.plot(room_sizes, nl_objectives, c='red', label='Non-Linear Quantum Model')
plt.plot(room_sizes, classical_objectives, c='green', label = 'Classical Model')

# Add a legend
plt.legend()

# Add labels and title (optional)
plt.xlabel('Number of Rooms')
plt.ylabel('Minimization Objective Value Ratio')
plt.title('Effectiveness of Algorithms based on Rooms')

# Display the plot
plt.show()