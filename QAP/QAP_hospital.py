"""
Background for the QAP problem

**CHANGES FROM QAP**

1. Introduce N simulations (we do N permutations) where N is the number of time steps
2. Between each simulation, add a penalty factor that penalize the closets if they move closets and departments
3. Two types of facilities, one that needs a supply and one that gives supplies
    - Two permutations, one that needs supplies and another that gets supplies, but they can't overlap locations
"""

# Create necessary imports
import numpy as np
# from dimod.generators import and_gate, combinations
from dwave.system import LeapHybridNLSampler
from dwave.optimization import Model
import helper as helper

def quantum_solution(N_rooms, N_supply, flow, room_supply_distance, room_room_distance, supply_supply_distance, time_steps):

    total_cost = 0
    # Generate the non linear quantum model
    model = Model()

    model_flow = model.constant(flow)
    model_rs_distance = model.constant(room_supply_distance)
    model_rr_distance = model.constant(room_room_distance)
    model_ss_distance = model.constant(supply_supply_distance)

    #create two lists for permutations of rooms and supply closets
    permutation_rooms = model.list(N_rooms)
    permutation_supply = model.list(N_supply)

    #store the previous permutation
    old_room_permutation = model.list(N_rooms)
    old_supply_permutation = model.list(N_supply)

    sampler = LeapHybridNLSampler()

    # Output the results

    for i in range(time_steps):
        #cost: the cost of transporting goods as defined in the problem statement
        cost = (model_flow[i][permutation_supply][:, permutation_rooms] * model_rs_distance).sum()
        #room_penalty: the penalty cost of moving rooms (scales with distance traveled for each room)
        room_penalty = (model_rr_distance[permutation_rooms][old_room_permutation]).sum()
        #supply_penalty: the penalty cost of moving supply closets (also scales with distance)
        supply_penalty = (model_ss_distance[permutation_supply][old_supply_permutation]).sum()
        #minimize the total cost (finds a combination of a good layout without moving too many rooms)
        model.minimize(cost + room_penalty + supply_penalty)

        #samples the model to determine the permutations of rooms and closets
        sampler.sample(model)
        with model.lock():
            # print(list(sym.state(0) for sym in model.iter_decisions()))
            states = list(sym for sym in model.iter_decisions())
            old_supply_permutation = states[3]
            old_room_permutation = states[2]
            # print(model.objective.state(0))
            total_cost += model.objective.state(0)

    return total_cost


if __name__ == '__main__':
    # Initialize state variables
    N_rooms = 3 #number of rooms (receive supplies)
    N_supply = 2 #number of supply closets (give supplies)
    max_flow = 100 #maximum value of flow from a given supply closet to each room
    max_distance = 1 #maximum distance between any two points in the graph
    time_steps = 10 #number of times the flow matrix changes


    # define flow matrix and distance matrices
    # we use three small distance matrices instead of one large one since we do not need all the distances
    flow = helper.random_time_matrix(time_steps, N_supply, N_rooms, max_flow)
    room_supply_distance = helper.random_matrix(N_supply, N_rooms, max_distance)
    room_room_distance = helper.random_symmetric_matrix(N_rooms, 0, max_distance)
    supply_supply_distance = helper.random_symmetric_matrix(N_supply, 0, max_distance)

    # Call the quantum solution
    print(quantum_solution(N_rooms, N_supply, flow, room_supply_distance, room_room_distance, supply_supply_distance, time_steps))
