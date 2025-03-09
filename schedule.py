def serial_SGS_for_activity_lists(activity_list: list,
                                  rcpsp: list, resource_capacity: int):
    schedule = {activity_list[0]: 0}
    acts_finish_time = 0
    for act in activity_list[1:len(activity_list)]:
        duration_of_act = rcpsp[act][0]
        predecessors_finish_times = []
        considered_acts = []
        for pred in rcpsp[act][2]:
            predecessors_finish_times.append(schedule[pred])
        earliest_start_time = max(predecessors_finish_times)
        possible_start_times = list([earliest_start_time])
        for finish_time in sorted(schedule.values()):
            if earliest_start_time < finish_time:
                possible_start_times.append(finish_time)
        for time in possible_start_times:
            free_capacity = True
            if time == possible_start_times[len(possible_start_times) - 1]:
                acts_finish_time = time + duration_of_act
                break
            time_period = list(range(time, (time + duration_of_act)))
            considered_times = filter(
                lambda t: t in possible_start_times, time_period)
            for time_instant in considered_times:
                for planned_act in schedule.keys():
                    if ((schedule[planned_act] - rcpsp[planned_act][0])
                            <= time_instant < schedule[planned_act]):
                        considered_acts.append(planned_act)
                used_resources = 0
                for active_act_at_time_instant in considered_acts:
                    used_resources += rcpsp[active_act_at_time_instant][1]
                free_resources = resource_capacity - used_resources
                acts_resource_needs = rcpsp[act][1]
                considered_acts = []
                if acts_resource_needs > free_resources:
                    free_capacity = False
            if free_capacity:
                acts_finish_time = time + duration_of_act
                break
        schedule.update({act: acts_finish_time})
    last_act = len(rcpsp) - 1
    project_duration = schedule[last_act]
    return schedule, project_duration

