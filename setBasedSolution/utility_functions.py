# List of utility functions


def get_intersections_with_existing_constraints(current_constraint, existing_constraints):
    return [current_constraint & existing_constraints[i] for i in range(len(existing_constraints))]


def get_all_subsets(current_constraint, intersections_with_existing_constraints, existing_constraints):
    all_subsets = [i for i, j in zip(intersections_with_existing_constraints, existing_constraints) if i == j]
    all_subsets_minus_self = [x for x in all_subsets if x != current_constraint]
    return all_subsets_minus_self


def get_all_super_subsets(subset_list):
    return [i for i in subset_list if i not in [i & j for j in subset_list if i != j]]


def get_all_supersets(current_constraint, intersections_with_existing_constraints, existing_constraints):
    all_supersets = [existing_constraints[i] for i in range(len(existing_constraints)) if
                     intersections_with_existing_constraints[i] == current_constraint]
    all_supersets_minus_self = [x for x in all_supersets if x != current_constraint]
    return all_supersets_minus_self


def get_all_overlaps(current_constraint, intersections_with_existing_constraints, existing_constraints):
    all_overlaps = [existing_constraints[i] for i in range(len(existing_constraints)) if
                    bool(intersections_with_existing_constraints[i])]
    all_overlaps_minus_self = [x for x in all_overlaps if x != current_constraint]
    return all_overlaps_minus_self


def get_non_sub_super_overlaps(all_overlaps, all_subsets, all_supersets):
    combined_sub_super_sets = all_subsets #+ all_supersets
    filtered_overlaps = [x for x in all_overlaps if x not in combined_sub_super_sets]
    return filtered_overlaps


def get_overlaps_with_unique_supersets(all_overlaps, current_constraint):
    removal_set = []
    for element1 in all_overlaps:
        for element2 in all_overlaps:
            if element1 & element2 == element1 and element1 != element2:
                ''' An assumption here as well: we need only those overlaps which are not subset of any other overlap'''
                # element1 is subset of element2; they are not equal and both have same superset
                removal_set.append(element1)
    filtered_overlaps = [element for element in all_overlaps if element not in removal_set]
    return filtered_overlaps


def get_all_demand_of_superset(superset, processed_requests, processed_demands):
    intersection_list = get_intersections_with_existing_constraints(superset, processed_requests)
    all_subsets = get_all_subsets(superset, intersection_list, processed_requests)
    if superset in processed_requests:
        all_subsets.append(superset)
    total_demand = 0
    for subset in all_subsets:
        total_demand = total_demand + processed_demands[processed_requests.index(subset)]
    return total_demand


def modify_constraint(current_superset, current_demand, existing_constraints, constraints_demand,
                      constraints_availability):
    constraint_index = existing_constraints.index(current_superset)
    constraints_demand[constraint_index] = constraints_demand[constraint_index] + current_demand
    constraints_availability[constraint_index] = constraints_availability[constraint_index] - current_demand
    return constraints_demand, constraints_availability


def add_constraint(current_request, current_demand, current_supply, existing_constraints, constraints_supply,
                   constraints_demand, constraints_availability):
    existing_constraints.append(current_request)
    constraints_supply.append(current_supply)
    constraints_demand.append(current_demand)
    constraints_availability.append(current_supply - current_demand)
    return existing_constraints, constraints_supply, constraints_demand, constraints_availability


def remove_redundancy_type_1(existing_constraints, constraints_supply, constraints_demand, constraints_availability):
    ''' Redundancy type 1 means when a subset is less or equally restrictive than a superset.
        Example: "x1 + x2 <= 20" is redundant if we also have "x1 + x2 + x3 <= 20" '''

    removal_list = []
    for current_row in range(len(existing_constraints)):
        current_constraint = existing_constraints[current_row]
        current_availability = constraints_availability[current_row]
        intersection_list = get_intersections_with_existing_constraints(current_constraint, existing_constraints)
        all_supersets = get_all_supersets(current_constraint, intersection_list, existing_constraints)
        for current_superset in all_supersets:
            superset_availability = constraints_availability[existing_constraints.index(current_superset)]
            if superset_availability <= current_availability:
                removal_list.append(current_row)
                break
    existing_constraints = [existing_constraints[i] for i in range(len(existing_constraints)) if i not in removal_list]
    constraints_supply = [constraints_supply[i] for i in range(len(constraints_supply)) if i not in removal_list]
    constraints_demand = [constraints_demand[i] for i in range(len(constraints_demand)) if i not in removal_list]
    constraints_availability = [constraints_availability[i] for i in range(len(constraints_availability)) if
                                i not in removal_list]
    return existing_constraints, constraints_supply, constraints_demand, constraints_availability


def remove_redundancy_type_2(existing_constraints, constraints_supply, constraints_demand, constraints_availability):
    ''' Redundancy type 2 means when sum of disjoint super subsets is less than a superset, the superset is redundant.
        This is true only if disjoint super subsets together can constitute the superset.
        Example: "x1 + x2 + x3 <= 20" is redundant if we also have "x1 + x2 <= 10" and x3 <=5 '''

    removal_list = []
    for current_row in range(len(existing_constraints)):
        current_constraint = existing_constraints[current_row]
        current_availability = constraints_availability[current_row]
        intersection_list = get_intersections_with_existing_constraints(current_constraint, existing_constraints)
        all_subsets = get_all_subsets(current_constraint, intersection_list, existing_constraints)
        all_super_subsets = get_all_super_subsets(all_subsets)
        if len(all_super_subsets) > 0:
            union_of_super_subsets = set.union(*all_super_subsets)
            if union_of_super_subsets == current_constraint:
                total_availability_of_subsets = 0
                for subset in all_super_subsets:
                    total_availability_of_subsets = total_availability_of_subsets + constraints_availability[
                        existing_constraints.index(subset)]
                if total_availability_of_subsets <= current_availability:
                    removal_list.append(current_row)

    existing_constraints = [existing_constraints[i] for i in range(len(existing_constraints)) if i not in removal_list]
    constraints_supply = [constraints_supply[i] for i in range(len(constraints_supply)) if i not in removal_list]
    constraints_demand = [constraints_demand[i] for i in range(len(constraints_demand)) if i not in removal_list]
    constraints_availability = [constraints_availability[i] for i in range(len(constraints_availability)) if
                                i not in removal_list]
    return existing_constraints, constraints_supply, constraints_demand, constraints_availability
