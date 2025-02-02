import numpy as np
import dimod
from dimod import ConstrainedQuadraticModel, Binary
from dwave.system import LeapHybridCQMSampler

def quantum_solution(
    N_rooms,
    N_supply,
    flow,
    room_supply_distance,
    room_room_distance,
    supply_supply_distance,
    time_steps,
    penalty
):
    """
    Formulates the room–supply assignment problem as a CQM and solves it using
    LeapHybridCQMSampler (dimod 1.13.0).

    Args:
        N_rooms (int): Number of rooms to be permuted at each time step.
        N_supply (int): Number of supply closets to be permuted at each time step.
        flow (3D array): flow[t, s, r] = flow at time t from supply s to room r.
        room_supply_distance (2D array): distance[s, r] = distance between supply s and room r.
        room_room_distance (2D array): distance[r1, r2] = distance between rooms r1 and r2.
        supply_supply_distance (2D array): distance[s1, s2] = distance between supplies s1 and s2.
        time_steps (int): Number of discrete times (t=0..time_steps-1).
        penalty (float): Penalty factor for occupant movement between consecutive time steps.

    Returns:
        (best_sample, best_energy):
          - best_sample (dict): assignment of variables for the best feasible solution
          - best_energy (float): corresponding objective value
        If no feasible solution is found, returns (None, None).
    """

    # --------------------------------------------------
    # 1) Create a CQM
    # --------------------------------------------------
    cqm = ConstrainedQuadraticModel()

    # --------------------------------------------------
    # 2) Define binary variables for permutations
    # --------------------------------------------------
    # X[t, i, r] = 1 if at time t, "room r" occupies "position i"
    # Y[t, j, s] = 1 if at time t, "supply s" occupies "position j"
    #
    # "position" is just an index from 0..(N_rooms-1) or 0..(N_supply-1).
    # This way, we ensure each occupant is used exactly once.

    X = {}  # For rooms
    Y = {}  # For supplies

    for t in range(time_steps):
        for i in range(N_rooms):
            for r in range(N_rooms):
                X[(t, i, r)] = Binary(f"X_{t}_{i}_{r}")
        for i in range(N_supply):
            for s in range(N_supply):
                Y[(t, i, s)] = Binary(f"Y_{t}_{i}_{s}")

    # --------------------------------------------------
    # 3) Permutation constraints
    # --------------------------------------------------
    # Rooms:
    #   (a) each "position i" has exactly 1 room
    #   (b) each room r appears exactly once among the positions
    for t in range(time_steps):
        # (a) exactly 1 room in position i
        for i in range(N_rooms):
            cqm.add_constraint(
                sum(X[(t, i, r)] for r in range(N_rooms)) == 1,
                label=f"rooms_one_per_position_t{t}_i{i}"
            )
        # (b) each room r is in exactly 1 position
        for r in range(N_rooms):
            cqm.add_constraint(
                sum(X[(t, i, r)] for i in range(N_rooms)) == 1,
                label=f"rooms_one_position_t{t}_r{r}"
            )

    # Supplies:
    #   (a) each "position i" has exactly 1 supply
    #   (b) each supply s appears exactly once among the positions
    for t in range(time_steps):
        # (a) exactly 1 supply in position i
        for i in range(N_supply):
            cqm.add_constraint(
                sum(Y[(t, i, s)] for s in range(N_supply)) == 1,
                label=f"supplies_one_per_position_t{t}_i{i}"
            )
        # (b) each supply s is in exactly 1 position
        for s in range(N_supply):
            cqm.add_constraint(
                sum(Y[(t, i, s)] for i in range(N_supply)) == 1,
                label=f"supplies_one_position_t{t}_s{s}"
            )

    # --------------------------------------------------
    # 4) Build the objective
    # --------------------------------------------------
    #
    # Objective = Flow cost + Movement penalty
    #
    # Flow Cost:
    #   If X[t,i,r] = 1 and Y[t,i,s] = 1 (same position i in time t),
    #   cost += flow[t, s, r] * room_supply_distance[s, r].
    #
    # Movement penalty:
    #   If X[t,i,r]=1 and X[t-1,i,r_prev]=1, cost += penalty * room_room_distance[r,r_prev].
    #   Similarly for Y[t,i,s] and Y[t-1,i,s_prev].

    objective_expr = 0

    # (A) Flow cost
    for t in range(time_steps):
        for i in range(N_rooms):
            for j in range(N_supply):
                for r in range(N_rooms):
                    for s in range(N_supply):
                        cost_flow = flow[t, s, r] * room_supply_distance[j, i]
                        if cost_flow != 0:
                            objective_expr += cost_flow * X[(t, i, r)] * Y[(t, j, s)]

    # (B) Movement penalty: Rooms
    for t in range(1, time_steps):
        for i in range(N_rooms):
            for r in range(N_rooms):
                for i_prev in range(N_rooms):
                    dist_rooms = room_room_distance[i, i_prev]
                    if dist_rooms != 0:
                        objective_expr += penalty * dist_rooms * X[(t, i, r)] * X[(t-1, i_prev, r)]

    # Movement penalty: Supplies
    for t in range(1, time_steps):
        for i in range(N_supply):
            for s in range(N_supply):
                for i_prev in range(N_supply):
                    dist_supp = supply_supply_distance[i, i_prev]
                    if dist_supp != 0:
                        objective_expr += penalty * dist_supp * Y[(t, i, s)] * Y[(t-1, i_prev, s)]

    # Set the CQM objective
    cqm.set_objective(objective_expr)

    # --------------------------------------------------
    # 5) Solve the CQM with LeapHybridCQMSampler
    # --------------------------------------------------
    sampler = LeapHybridCQMSampler()
    sampleset = sampler.sample_cqm(cqm, label="RoomSupplyCQM_via_helper")

    # Filter feasible solutions
    feasible = sampleset.filter(lambda d: d.is_feasible)
    if not feasible:
        print("No feasible solution found.")
        return None, None

    best = feasible.first
    return best.sample, best.energy


if __name__ == "__main__":
    import time
    import matrix_gen as matrix_gen

    # Example usage
    N_rooms = 16
    N_supply = 12
    time_steps = 12
    penalty = 40

    # ----------------------------------------------------
    # Use helper.py to generate random matrices
    # ----------------------------------------------------
    # These helper functions are defined in your helper.py:
    #   random_symmetric_matrix(n, minflow, maxflow)
    #   random_matrix(n, m, max)
    #   random_time_matrix(number, n, m, max)
    # Make sure 'helper.py' is in the same directory or PYTHONPATH.

    # Flow: shape (time_steps, N_supply, N_rooms)
    max_flow = 10
    flow = matrix_gen.random_time_matrix(time_steps, N_supply, N_rooms, max_flow)

    # room_supply_distance: shape (N_supply, N_rooms)
    max_dist = 5
    room_supply_distance = matrix_gen.random_matrix(N_supply, N_rooms, max_dist)

    # room_room_distance: shape (N_rooms, N_rooms), symmetrical
    room_room_distance = matrix_gen.random_symmetric_matrix(N_rooms, 0, max_dist)

    # supply_supply_distance: shape (N_supply, N_supply), symmetrical
    supply_supply_distance = matrix_gen.random_symmetric_matrix(N_supply, 0, max_dist)

    # ----------------------------------------------------
    # Solve
    # ----------------------------------------------------
    start_time = time.time()

    best_sample, best_energy = quantum_solution(
        N_rooms,
        N_supply,
        flow,
        room_supply_distance,
        room_room_distance,
        supply_supply_distance,
        time_steps,
        penalty
    )
    end_time = time.time()

    if best_sample is not None:
        print(f"\nFound a feasible solution with objective value = {best_energy:.2f}")
        print("Variables assigned value 1 in the solution:")
        for var, val in best_sample.items():
            if abs(val) > 0.5:  # i.e. binary = 1
                print(f"  {var} = 1")
    else:
        print("No feasible solution found.")

    print(f"Solved in {end_time - start_time:.2f} seconds.")
