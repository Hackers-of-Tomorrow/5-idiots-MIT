import matplotlib.pyplot
import QAP_nonlinear
import QAP_classical
import QAP_cqm
import QAP.matrix_gen as matrix_gen
import time
import matplotlib.pyplot as plt

# Initialize state variables
N_rooms = 300 #number of rooms (receive supplies)
N_supply = 400 #number of supply closets (give supplies)

max_flow = 100 #maximum value of flow from a given supply closet to each room
max_distance = 100 #maximum distance between any two points in the graph
time_steps = 5 #number of times the flow matrix changes
penalty = 10 # penalty for moving
iterations = 4

cqm_objectives = []
cqm_times = []
nl_objectives = []
nl_times = []
classical_objectives = []
classical_times = []

for i in range(iterations):
    # define flow matrix and distance matrices
    # we use three small distance matrices instead of one large one since we do not need all the distances
    flow = matrix_gen.random_time_matrix(time_steps, N_supply, N_rooms, max_flow)
    room_supply_distance = matrix_gen.random_matrix(N_supply, N_rooms, max_distance)
    room_room_distance = matrix_gen.random_symmetric_matrix(N_rooms, 0, max_distance)
    supply_supply_distance = matrix_gen.random_symmetric_matrix(N_supply, 0, max_distance)

    # Call the quantum solution
    start_time = time.time()
    cqm_objective = QAP_cqm.quantum_solution(N_rooms, N_supply, flow, room_supply_distance, room_room_distance, supply_supply_distance, time_steps, penalty)[1]
    cqm_time = time.time()-start_time
    start_time = time.time()
    nl_objective = QAP_nonlinear.quantum_solution2(N_rooms, N_supply, flow, room_supply_distance, room_room_distance, supply_supply_distance, time_steps, penalty)
    nl_time = time.time() - start_time
    start_time = time.time()
    classical_objective = QAP_classical.classical_solution(N_rooms, N_supply, flow, room_supply_distance, room_room_distance, supply_supply_distance, time_steps, penalty)
    classical_time = time.time() - start_time

    cqm_objectives.append(cqm_objective)
    cqm_times.append(cqm_time)
    nl_objectives.append(nl_objective)
    nl_times.append(nl_time)
    classical_objectives.append(classical_objective)
    classical_times.append(classical_time)

    N_rooms *= 2
    N_supply *= 2

print(cqm_objectives)
print(cqm_times)
print(nl_objectives)
print(nl_times)
print(classical_objectives)
print(classical_times)


sums = [c + n + cl for c, n, cl in zip(cqm_objectives, nl_objectives, classical_objectives)]
cqm_objectives = [c/cl for c, cl in zip(cqm_objectives, sums)]
nl_objectives = [n/c for n, c in zip(nl_objectives, sums)]
classical_objectives = [n/c for n, c in zip(classical_objectives, sums)]

# Create the scatter plot
plt.scatter(cqm_times, cqm_objectives, c='blue', label='Constrained Quantum Model')
plt.scatter(nl_times, nl_objectives, c='red', label='Non-Linear Quantum Model')
plt.scatter(classical_times, classical_objectives, c='green', label = 'Classical Model')

# Add a legend
plt.legend()

# Add labels and title (optional)
plt.xlabel('Run-Time (s)')
plt.xscale("log")
plt.ylabel('Objective Function Ratio')
plt.title('Effectiveness of Quantum vs. Classical Algorithms')

# Display the plot
plt.show()