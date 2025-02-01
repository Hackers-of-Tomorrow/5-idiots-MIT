import QAP_hospital
import QAP_classical
import helper
import time

# Initialize state variables
N_rooms = 3 #number of rooms (receive supplies)
N_supply = 2 #number of supply closets (give supplies)
max_flow = 100 #maximum value of flow from a given supply closet to each room
max_distance = 1 #maximum distance between any two points in the graph
time_steps = 5 #number of times the flow matrix changes


# define flow matrix and distance matrices
# we use three small distance matrices instead of one large one since we do not need all the distances
flow = helper.random_time_matrix(time_steps, N_supply, N_rooms, max_flow)
room_supply_distance = helper.random_matrix(N_supply, N_rooms, max_distance)
room_room_distance = helper.random_symmetric_matrix(N_rooms, 0, max_distance)
supply_supply_distance = helper.random_symmetric_matrix(N_supply, 0, max_distance)

# Call the quantum solution
start_time = time.time()
quantum_objective = QAP_hospital.quantum_solution(N_rooms, N_supply, flow, room_supply_distance, room_room_distance, supply_supply_distance, time_steps)
quantum_time = time.time()-start_time
start_time = time.time()
classical_objective = QAP_classical.classical_solution(N_rooms, N_supply, flow, room_supply_distance, room_room_distance, supply_supply_distance, time_steps)
classical_time = time.time() - start_time

print("Quantum Objective: ", quantum_objective)
print("Quantum Time: ", quantum_time)
print("Classical Objective: ", classical_objective)
print("Classical Time: ", classical_time)

