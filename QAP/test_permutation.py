
import cqm_qap_hospital
import QAP_hospital
import helper
import numpy as np

def test_permutation(N_rooms, N_supply, flow, room_supply_distance, room_room_distance, supply_supply_distance, time_steps, penalty, X, Y):
    total_cost = 0
    for t in range(time_steps):
         for i in range(N_rooms):
            for j in range(N_supply):
                for r in range(N_rooms):
                    for s in range(N_supply):
                        cost_flow = flow[t, s, r] * room_supply_distance[j, i]
                        if cost_flow != 0:
                            total_cost += cost_flow * X[(t, i, r)] * Y[(t, j, s)]
    for t in range(1, time_steps):
        for i in range(N_rooms):
             for r in range(N_rooms):
                for i_prev in range(N_rooms):
                    dist_rooms = room_room_distance[i, i_prev]
                    if dist_rooms != 0:
                        total_cost += penalty * dist_rooms * X[(t, i, r)] * X[(t-1, i_prev, r)]
             for i in range(N_supply):
                for s in range(N_supply):
                    for i_prev in range(N_supply):
                        dist_supp = supply_supply_distance[i, i_prev]
                        if dist_supp != 0:
                            total_cost += penalty * dist_supp * Y[(t, i, s)] * Y[(t-1, i_prev, s)]
    return total_cost

if __name__ == '__main__':
    # Initialize state variables
    N_rooms = 4 #number of rooms (receive supplies)
    N_supply = 3 #number of supply closets (give supplies)
    max_flow = 100 #maximum value of flow from a given supply closet to each room
    max_distance = 1 #maximum distance between any two points in the graph
    time_steps = 10 #number of times the flow matrix changes
    penalty = 10

    # define flow matrix and distance matrices
    # we use three small distance matrices instead of one large one since we do not need all the distances
    flow = helper.random_time_matrix(time_steps, N_supply, N_rooms, max_flow)
    room_supply_distance = helper.random_matrix(N_supply, N_rooms, max_distance)
    room_room_distance = helper.random_symmetric_matrix(N_rooms, 0, max_distance)
    supply_supply_distance = helper.random_symmetric_matrix(N_supply, 0, max_distance)

    # Call the quantum solution
    # print(quantum_solution(N_rooms, N_supply, flow, room_supply_distance, room_room_distance, supply_supply_distance, time_steps, 10))
    # print('1 finished in ', time.time() - t)
    # t = time.time()
    cost_nl, permutations_nl = QAP_hospital.quantum_solution2(N_rooms, N_supply, flow, room_supply_distance, room_room_distance, supply_supply_distance, time_steps, penalty)
    X = []
    Y = []
    print(permutations_nl)
    for t in range(time_steps):
        Xi = [[0]*N_rooms for _ in range(N_rooms)]
        Yi = [[0]*N_supply for _ in range(N_supply)]
        for i in range(N_rooms):
            Xi[i][int(permutations_nl[t][i])] = 1
            # Xi[int(permutations_nl[t][i])][i] = 1
        for i in range(N_supply):
            Yi[i][int(permutations_nl[t+time_steps][i])] = 1
            # Yi[int(permutations_nl[t][i])][i] = 1
        X.append(Xi)
        Y.append(Yi)
    print(X)
    calculated_cost_nl = test_permutation(N_rooms, N_supply, flow, room_supply_distance, room_room_distance, supply_supply_distance, time_steps, penalty, np.array(X), np.array(Y))
    cost_cqm, XY = cqm_qap_hospital.quantum_solution(N_rooms, N_supply, flow, room_supply_distance, room_room_distance, supply_supply_distance, time_steps, penalty)
    # print("ASASDASDASDASD")
    # print(X)
    # print(Y)
    calculated_cost_cqm = test_permutation(N_rooms, N_supply, flow, room_supply_distance, room_room_distance, supply_supply_distance, time_steps, penalty, XY[0], XY[1])

    print("NL: ", cost_nl, calculated_cost_nl)
    print("CQM:", cost_cqm, calculated_cost_cqm)



