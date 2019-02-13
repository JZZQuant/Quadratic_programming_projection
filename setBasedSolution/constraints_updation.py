# The main logic of constraint creation and modifications

from utility_functions import get_all_overlaps, get_all_subsets, get_all_super_subsets, get_all_supersets, \
    get_intersections_with_existing_constraints, get_non_sub_super_overlaps, get_overlaps_with_unique_supersets, \
    get_all_demand_of_superset, modify_constraint, add_constraint, remove_redundancy_type_1, remove_redundancy_type_2


def update_constraints_list(current_request, current_demand, existing_constraints, constraints_supply,
                            constraints_demand, constraints_availability, supplies, processed_requests, processed_demands):
    intersection_list = get_intersections_with_existing_constraints(current_request, existing_constraints)
    all_subsets = get_all_subsets(current_request, intersection_list, existing_constraints)
    all_subsets = get_all_super_subsets(all_subsets)
    all_supersets = get_all_supersets(current_request, intersection_list, existing_constraints)
    all_overlaps = get_all_overlaps(current_request, intersection_list, existing_constraints)
    all_overlaps = get_non_sub_super_overlaps(all_overlaps, all_subsets, all_supersets)
    all_overlaps = get_overlaps_with_unique_supersets(all_overlaps, current_request)

    if current_request in existing_constraints:
        # constraint with same set already exists
        all_supersets.append(current_request)
        for current_superset in all_supersets:
            constraints_demand, constraints_availability = modify_constraint(current_superset, current_demand,
                                                                             existing_constraints, constraints_demand,
                                                                             constraints_availability)

    elif len(all_subsets) > 0 or len(all_supersets) > 0 or len(all_overlaps) > 0:
        # constraint with same set doesn't exist but subsets/supersets/overlaps exist
        # Update the supersets first
        for current_superset in all_supersets:
            constraints_demand, constraints_availability = modify_constraint(current_superset, current_demand,
                                                                             existing_constraints, constraints_demand,
                                                                             constraints_availability)

        # Update current constraint based on disjoint subsets and add it to constraints list
        '''We take here only super subsets. These subsets don't have any of their subsets in this list. 
        This also ensures that two elements in this list will have absolutely zero intersection/overlaps. Had there been
        any overlap, their superset would have also existed in the existing_constraints and this superset would have got 
        selected instead of these two sets.'''
        current_demand_including_subset = current_demand
        for current_subset in all_subsets:
            subset_index = existing_constraints.index(current_subset)
            current_demand_including_subset = current_demand_including_subset + constraints_demand[subset_index]
        current_supply = sum([supplies[i] for i in list(current_request)])
        existing_constraints, constraints_supply, constraints_demand, constraints_availability = add_constraint(
            current_request, current_demand_including_subset, current_supply, existing_constraints, constraints_supply,
            constraints_demand, constraints_availability)

        # For overlap list keep creating new supersets and add them; skip if such superset already exist
        if len(all_overlaps) > 0:
            for current_overlap in all_overlaps:
                new_superset = current_request | current_overlap
                if new_superset in existing_constraints:
                    continue
                else:
                    # overlap_intersection_list = get_intersections_with_existing_constraints(current_overlap, existing_constraints)
                    # all_subset_of_current_overlap = get_all_subsets(current_overlap, overlap_intersection_list, existing_constraints)
                    # filtered_subsets = [subset for subset in all_subsets if subset not in all_subset_of_current_overlap]
                    # current_demand_including_subset = current_demand
                    # for current_subset in filtered_subsets:
                    #     subset_index = existing_constraints.index(current_subset)
                    #     current_demand_including_subset = current_demand_including_subset + constraints_demand[subset_index]
                    #
                    # overlap_index = existing_constraints.index(current_overlap)
                    # new_superset_demand = current_demand_including_subset + constraints_demand[overlap_index]
                    # # Double minus is happening for subset of overlapped part
                    new_superset_demand = get_all_demand_of_superset(new_superset, processed_requests, processed_demands)
                    new_superset_supply = sum([supplies[i] for i in list(new_superset)])
                    existing_constraints, constraints_supply, constraints_demand, constraints_availability = add_constraint(
                        new_superset, new_superset_demand, new_superset_supply, existing_constraints,
                        constraints_supply, constraints_demand, constraints_availability)
                    # exit

    else:
        # It is from different island so just add current constraint
        current_supply = sum([supplies[i] for i in list(current_request)])
        existing_constraints, constraints_supply, constraints_demand, constraints_availability = add_constraint(
            current_request, current_demand, current_supply, existing_constraints, constraints_supply,
            constraints_demand, constraints_availability)
        # exit

    existing_constraints, constraints_supply, constraints_demand, constraints_availability = remove_redundancy_type_1(
        existing_constraints, constraints_supply, constraints_demand, constraints_availability)
    existing_constraints, constraints_supply, constraints_demand, constraints_availability = remove_redundancy_type_2(
        existing_constraints, constraints_supply, constraints_demand, constraints_availability)

    return existing_constraints, constraints_supply, constraints_demand, constraints_availability
