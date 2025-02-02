# <demo_name>

Assignment issues are a massive problem when it comes to distributing resources effectively. This repository tackles this issue by introducing a modified QAP solution aimed at assisting hospital staff with positioning resources and staff:
- Bipartite QAP sectioned into suppliers and consumers
- Time dependent flow rates enabling for variations in patient necessities
- Penalties for moving supply closets and consumers between time periods

These additions ensure that our QAP solution is adapted to the unpredictability of real world situations.

![D-Wave Logo](dwave_logo.png)

## Usage

To use the constrained quantum model, run the following code,

```bash
python example.py
```

### Inputs
All the necessary inputs can be found in example.py. Note that these are state variables that define
how the model will run. This includes the number of rooms present, penalty for moving, and number
of time steps. Note the following,
- The matrices used for input are randomly generated matrices based on the input size
- To use the other quantum models, replace all calls to hospital_qcm with this model

### Outputs
The output from example.py will be an minimal objective value along with the assignments that lead to
this solution. In addition, it will output the time it took for the calculation.
- For the non linear result, the output it prints is the object type, but the actual object exists.

## Problem Description 

The goal of this problem is to create permutations of suppliers and consumers so that the total amount of work needed to transport supplies is minimized.

Objectives to be optimized: The product of the flow and the distances between the suppliers and clients at every point in time was minimized in order to find the minimum amount of work necessary to bring supplies to clients.
Time was a necessary tradeoff, especially for smaller sized problems. Unfortunately, there weren't enough qubits needed to simulate more massive systems where classical systems are significantly slower than quantum.

Constraints: The distance matrices within each type of location is assumed to be symmetric. However, the parameters for the system are heavily customizable.

## Model Overview
In this project, we model hospital equipment rooms as suppliers and patients as the clients. If there are ```N_rooms``` clients and ```N_supply``` suppliers, then we will have matrices of ```N_supply x N_rooms``` to which we will have to apply constraints and an objective function.

### Parameters
```N_rooms (N_r)```: The number of patients
```N_supply (N_s)```: The number of supply closets
```flow (f)```: Matrix of flow from supply closets to patients
```room_supply_distance (rs)```: Matrix of distances from patient rooms to supply closets
```room_room_distance (rr)```: Matrix of distance from patient rooms to other patient rooms
```supply_supply_distance (ss)```: Matrix of distance from supply rooms to other supply rooms
```time_steps (T)```: Number of time steps the algorithms runs through
```penalty (p)```: Constant multiplier to the distance acting as a penalty of moving between time steps

### Variables
```X[t, i, r]```: Binary variable if at time t, patient room r occupies location i
```Y[t, j, s]```: Binary variable if at time t, supply room s occupies location j

### Objective
There are two parts of the objective, one from the actual objective and the other being the penalty for moving between rooms. The actual objective is given by,
```f[t, s, r] * rs[j, i] * X[(t, i, r)] * Y[(t, j, s)].```
The penalty will be,
```p * rr[i, i_prev] * X[(t, i, r)] * X[(t-1, i_prev, r)] + p * ss[i, i_prev] * Y[(t, j, s)] * Y[(t-1, j_prev, s)]```.

### Constraints
There are two constraints. The first is that there is exactly 1 room/supply in each room. This is encoded by,
```sum(X[(t, i, r)] for r in range(N_rooms)) == 1```.
The second constraint is that each room is only chosen once over all the positions,
```sum(X[(t, i, r)] for i in range(N_rooms)) == 1```.

## Code Overview

* All of the source code is in the QAP file in the respository. If you want, you can take a look at them if needed.
* Each of the models is encoded in a function that can be called so long as you import the class in your code.
* matrix_gen.py contains all of the generation code for the random matrices.
* QAP_comparison.py in the QAP folder is a comparison platform to visualize the differences between the models.

## References

A. D-Wave, "D-Wave iQuHackathon 2025 Challenges", [D-Wave Challenge](https://github.com/iQuHACK/2025-D-Wave)
B. Ocean, "D-Wave Ocean Software Documentation", [Ocean Documentation][https://docs.ocean.dwavesys.com/en/stable/index.html]

## License

Released under the Apache License 2.0. See [LICENSE](LICENSE) file.
