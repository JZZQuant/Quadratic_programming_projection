from constraints_updation import update_constraints_list


def solver_main(sparse, supplies, demands):
    import numpy as np

    # converting everything to lists
    request_list = []
    for i in range(sparse.shape[0]):
        request_list.append(set(np.where(sparse[i,])[1]))
    supplies = list(supplies)
    demands = list(demands)

    # Adding first constraint
    existing_constraints = [request_list[0]]
    constraints_supply = [sum([supplies[i] for i in list(existing_constraints[0])])]
    constraints_demand = [demands[0]]
    constraints_availability = [constraints_supply[0] - constraints_demand[0]]

    # Looping for other rows
    for current_row in range(1, (len(request_list) - 1)):
        processed_requests = request_list[:current_row]
        processed_demands = demands[:current_row]
        current_request = request_list[current_row]
        current_demand = demands[current_row]
        existing_constraints, constraints_supply, constraints_demand, constraints_availability = update_constraints_list(
            current_request, current_demand, existing_constraints, constraints_supply, constraints_demand,
            constraints_availability, supplies, processed_requests, processed_demands)
        # print(current_row, len(existing_constraints), len(constraints_availability))

    return existing_constraints, constraints_availability
