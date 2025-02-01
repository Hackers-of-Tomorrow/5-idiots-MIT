import numpy as np
from scipy.optimize import minimize
import helper

def classical_solution(N_rooms, N_supply, flow, room_supply_distance, room_room_distance, supply_supply_distance, time_steps):

    # Define the objective function
    def objective_function(x, time_step):
        """
        x: A flat array representing the concatenated permutations of rooms and supply facilities.
        time_step: The current time step (used to index the flow matrix).
        """
        # Split x into room and supply permutations
        room_permutation = x[:N_rooms].astype(int)
        supply_permutation = x[N_rooms:].astype(int)

        # Calculate the cost of flow between supply facilities and rooms
        flow_cost = np.sum(flow[time_step][supply_permutation][:, room_permutation] * room_supply_distance)

        # Calculate the penalty for moving rooms
        room_penalty = np.sum(room_room_distance[room_permutation][:, old_room_permutation])

        # Calculate the penalty for moving supply facilities
        supply_penalty = np.sum(supply_supply_distance[supply_permutation][:, old_supply_permutation])

        # Total cost
        total_cost = flow_cost + room_penalty + supply_penalty
        return total_cost

    # Initialize old permutations
    old_room_permutation = np.arange(N_rooms)
    old_supply_permutation = np.arange(N_supply)

    total_cost = 0

    # Simulation loop
    for i in range(time_steps):
        # Initial guess for the permutations (flattened array)
        x0 = np.concatenate([old_room_permutation, old_supply_permutation])

        # Bounds for the variables (ensure they are within valid permutation indices)
        bounds = [(0, N_rooms - 1)] * N_rooms + [(0, N_supply - 1)] * N_supply

        # Constraints: Ensure no duplicate indices in permutations
        def room_constraint(x):
            return len(set(x[:N_rooms])) - N_rooms  # Must be 0 for valid permutation

        def supply_constraint(x):
            return len(set(x[N_rooms:])) - N_supply  # Must be 0 for valid permutation

        constraints = [
            {"type": "eq", "fun": room_constraint},
            {"type": "eq", "fun": supply_constraint},
        ]

        # Solve the optimization problem
        result = minimize(
            objective_function,
            x0,
            args=(i,),
            bounds=bounds,
            constraints=constraints,
            method="SLSQP",  # Sequential Least Squares Programming
        )

        total_cost += result.fun

        # Extract the optimized permutations
        optimized_room_permutation = result.x[:N_rooms].astype(int)
        optimized_supply_permutation = result.x[N_rooms:].astype(int)

        # Update old permutations
        old_room_permutation = optimized_room_permutation
        old_supply_permutation = optimized_supply_permutation

    return total_cost


if __name__ == '__main__':
    # Initialize state variables
    N_rooms = 3
    N_supply = 2
    max_flow = 100
    max_distance = 1
    time_steps = 10

    # Generate matrices
    flow = helper.random_time_matrix(time_steps, N_supply, N_rooms, max_flow)
    room_supply_distance = helper.random_matrix(N_supply, N_rooms, max_distance)
    room_room_distance = helper.random_symmetric_matrix(N_rooms, 0, max_distance)
    supply_supply_distance = helper.random_symmetric_matrix(N_supply, 0, max_distance)

    classical_solution(flow, room_supply_distance, room_room_distance, supply_supply_distance, time_steps)