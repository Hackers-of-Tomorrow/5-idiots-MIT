"""
EXAMPLE CODE

- To use other models, import necessary classes.
- Make sure to change variables at the top based on desired constraints.
- If you have matrices you wish to use, you can replace the random matrix generation with your matrices!
"""

# Perform necessary imports
import time
import QAP.QAP_cqm
import QAP.QAP_classical
import QAP.QAP_nonlinear
import QAP.matrix_gen


# Define variables
N_rooms = 5
N_supply = 4
time_steps = 3
penalty = 10
max_dist = 5
max_flow = 10


# Flow: shape (time_steps, N_supply, N_rooms)
flow = QAP.matrix_gen.random_time_matrix(time_steps, N_supply, N_rooms, max_flow)

# room_supply_distance: shape (N_supply, N_rooms)
room_supply_distance = QAP.matrix_gen.random_matrix(N_supply, N_rooms, max_dist)

# room_room_distance: shape (N_rooms, N_rooms), symmetrical
room_room_distance = QAP.matrix_gen.random_symmetric_matrix(N_rooms, 0, max_dist)

# supply_supply_distance: shape (N_supply, N_supply), symmetrical
supply_supply_distance = QAP.matrix_gen.random_symmetric_matrix(N_supply, 0, max_dist)

# Start the timer
start_time = time.time()

# Run the quantum solution algorithm for cqm
best_sample, best_energy = QAP.QAP_nonlinear.quantum_solution(
        N_rooms,
        N_supply,
        flow,
        room_supply_distance,
        room_room_distance,
        supply_supply_distance,
        time_steps,
        penalty
    )

# End the timer
end_time = time.time()

# Print the best result and the time for running
if best_sample is not None:
    print(f"\nFound a feasible solution with objective value = {best_energy:.2f}")
    if type(best_sample) == dict:
        print("Variables assigned value 1 in the solution:")
        for var, val in best_sample.items():
            if abs(val) > 0.5:  # i.e. binary = 1
                print(f"  {var} = 1")
else:
    print("No feasible solution found.")

print(f"Solved in {end_time - start_time:.2f} seconds.")