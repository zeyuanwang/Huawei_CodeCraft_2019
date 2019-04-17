import logging
import sys
import math
import collections

logging.basicConfig(level=logging.DEBUG,
                    filename='../logs/CodeCraft-2019.log',
                    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='a')

def add_to_dict(file_path, dict_name):
    with open(file_path, 'r') as file:
        text = file.read()
    list_file = text.split("\n")
    for item in list_file:
        if item[0] == "#":
            continue
        else:
            list_one_item = item.replace(' ', '').strip('()').split(',')
            dict_name[list_one_item[0]] = list_one_item[1:]

def write_to_txt(file_path, dict_answer):
    with open(file_path, 'w') as f:
        f.write("#(carId, StartTime, RoadId, ...)\n")
        for car_id in dict_answer:
            f.write("(" + car_id + ", ")
            f.write(", ".join(str(road_id) for road_id in dict_answer[car_id]))
            f.write(")\n")
            
def get_average_occupancy(car_id, dict_car, dict_road, dict_road_occupancy, dict_shortest_path):
    average_occupancy = 0
    route_length = len(dict_shortest_path[car_id]) - 1
        
    for i in range(route_length):
        if i == 0:
            direction = dict_car[car_id][0]
        else:
            if direction == dict_road[road_id][3]:
                direction = dict_road[road_id][4]
            else:
                direction = dict_road[road_id][3]
        
        road_id = dict_shortest_path[car_id][i]
        
        average_occupancy += math.pow(dict_road_occupancy[(road_id, direction)], 3)
    
    average_occupancy /= route_length
    
    return average_occupancy

def construct_dict_G_all_speed(dict_G_all_speed, dict_car):
    for car_id in dict_car:
        if dict_car[car_id][2] not in dict_G_all_speed:
            dict_G_all_speed[dict_car[car_id][2]] = dict()
            
def construct_dict_shortest_path_last_cross(dict_shortest_path_last_cross, dict_G_all_speed):
     for car_speed in dict_G_all_speed:
        dict_shortest_path_last_cross[car_speed] = dict()
        
def get_shortest_paths(dict_G_all_speed, dict_shortest_path_last_cross, dict_shortest_path, dict_car, dict_cross):
    for car_id in dict_car:
        car_speed = dict_car[car_id][2]
        start_cross_id = dict_car[car_id][0]
        end_cross_id = dict_car[car_id][1]
        if start_cross_id not in dict_shortest_path_last_cross[car_speed]:
            dict_shortest_path_last_cross[car_speed][start_cross_id] = get_shortest_path_last_cross_Dijkstra(dict_G_all_speed[car_speed], start_cross_id, dict_cross)
        dict_shortest_path[car_id] = retrieve_shortest_path(dict_G_all_speed[car_speed], dict_shortest_path_last_cross[car_speed][start_cross_id], end_cross_id)

def judge_direction(dict_cross, cross_id, present_road_id, next_road_id):
    list_road = dict_cross[cross_id]
    if (present_road_id == list_road[0] and next_road_id == list_road[2]) or (present_road_id == list_road[1] and next_road_id == list_road[3]) or (present_road_id == list_road[2] and next_road_id == list_road[0]) or (present_road_id == list_road[3] and next_road_id == list_road[1]):
        return "straight"
    if (present_road_id == list_road[0] and next_road_id == list_road[1]) or (present_road_id == list_road[1] and next_road_id == list_road[2]) or (present_road_id == list_road[2] and next_road_id == list_road[3]) or (present_road_id == list_road[3] and next_road_id == list_road[0]):
        return "left"
    if (present_road_id == list_road[0] and next_road_id == list_road[3]) or (present_road_id == list_road[1] and next_road_id == list_road[0]) or (present_road_id == list_road[2] and next_road_id == list_road[1]) or (present_road_id == list_road[3] and next_road_id == list_road[2]):
        return "right"
    else:
        return "unknown direction"
    
def get_road_id(G, start_cross_id, end_cross_id):
    return G[start_cross_id][end_cross_id][0]

def get_road_value(G, start_cross_id, end_cross_id):
    return int(G[start_cross_id][end_cross_id][1])

def construct_graph(dict_G_all_speed, dict_cross, dict_road):
    for car_speed in dict_G_all_speed:
        for cross_id in dict_cross:
            dict_G_all_speed[car_speed][cross_id] = dict()
            dict_G_all_speed[car_speed][cross_id] = collections.OrderedDict()
    
        for road_id in dict_road:
            if dict_road[road_id][5] == "0":
                dict_G_all_speed[car_speed][dict_road[road_id][3]][dict_road[road_id][4]] = [road_id, int(dict_road[road_id][0]) / min(int(car_speed), int(dict_road[road_id][1]))]
            else:
                dict_G_all_speed[car_speed][dict_road[road_id][4]][dict_road[road_id][3]] = [road_id, int(dict_road[road_id][0]) / min(int(car_speed), int(dict_road[road_id][1]))]
                dict_G_all_speed[car_speed][dict_road[road_id][3]][dict_road[road_id][4]] = [road_id, int(dict_road[road_id][0]) / min(int(car_speed), int(dict_road[road_id][1]))]

def get_shortest_path_last_cross_Dijkstra(G, start_cross_id, dict_cross):
    distance = dict()
    distance = collections.OrderedDict()
    last_cross = dict()
    last_cross = collections.OrderedDict()
    confirmed = []
    
    for cross_id in G[start_cross_id]:
        distance[cross_id] = int(G[start_cross_id][cross_id][1])
        last_cross[cross_id] = start_cross_id
    confirmed.append(start_cross_id)

    while len(confirmed) < len(dict_cross):
        next_corss_to_confirm = min(distance, key=distance.get)
        for cross_id in G[next_corss_to_confirm]:
            if cross_id in confirmed:
                continue
            
            present_road_id = G[last_cross[next_corss_to_confirm]][next_corss_to_confirm][0]
            next_road_id = G[next_corss_to_confirm][cross_id][0]
            direction = judge_direction(dict_cross, next_corss_to_confirm, present_road_id, next_road_id)
            
            if direction == "straight":
                direction_value = 0
            elif direction == "left":
                direction_value = 16
            else:
                direction_value = 16
            
            if cross_id not in distance:
                distance[cross_id] = distance[next_corss_to_confirm] + direction_value + int(G[next_corss_to_confirm][cross_id][1])
                last_cross[cross_id] = next_corss_to_confirm
            elif distance[cross_id] > distance[next_corss_to_confirm] + direction_value + int(G[next_corss_to_confirm][cross_id][1]):
                distance[cross_id] = distance[next_corss_to_confirm] + direction_value + int(G[next_corss_to_confirm][cross_id][1])
                last_cross[cross_id] = next_corss_to_confirm
        confirmed.append(next_corss_to_confirm)
        distance.pop(next_corss_to_confirm)
        
    return last_cross

def retrieve_shortest_path(G, last_cross, end_cross_id):
    list_path = []
    while end_cross_id in last_cross:
        list_path = [get_road_id(G, last_cross[end_cross_id], end_cross_id)] + list_path 
        end_cross_id = last_cross[end_cross_id]
    return list_path

def initialize_judgement(dict_preset_answer, dict_car, dict_road, dict_car_state, dict_departure_time_and_route, dict_road_state_map, dict_road_car_in_init_list, dict_car_sequence_at_corss):
    
    for car_id in dict_preset_answer:
        dict_departure_time_and_route[car_id] = dict_preset_answer[car_id]

    for road_id in dict_road:
        start_cross_id = dict_road[road_id][3]
        end_cross_id = dict_road[road_id][4]
        road_length = int(dict_road[road_id][0])
        road_width = int(dict_road[road_id][2])
        
        dict_road_state_map[road_id] = dict()
        dict_road_state_map[road_id] = collections.OrderedDict()
        
        dict_road_car_in_init_list[road_id] = dict()
        dict_road_car_in_init_list[road_id] = collections.OrderedDict()
        
        dict_car_sequence_at_corss[road_id] = dict()
        dict_car_sequence_at_corss[road_id] = collections.OrderedDict()
        
        dict_road_state_map[road_id][start_cross_id] = dict()
        dict_road_state_map[road_id][start_cross_id] = collections.OrderedDict()
        
        dict_road_car_in_init_list[road_id][start_cross_id] = []
        
        dict_car_sequence_at_corss[road_id][start_cross_id] = []
        
        for lane in range(road_width):
            dict_road_state_map[road_id][start_cross_id][lane] = [None] * road_length
            
        if(dict_road[road_id][5] == "1"): #two-way road
            dict_road_state_map[road_id][end_cross_id] = dict()
            dict_road_state_map[road_id][end_cross_id] = collections.OrderedDict()
            
            dict_road_car_in_init_list[road_id][end_cross_id] = []
            
            dict_car_sequence_at_corss[road_id][end_cross_id] = []
        
            for lane in range(road_width):
                dict_road_state_map[road_id][end_cross_id][lane] = [None] * road_length
        
    for car_id in dict_departure_time_and_route:
        dict_car_state[car_id] = ["sleep", "garage"]
        
        start_cross_id = dict_car[car_id][0]
        first_road = dict_departure_time_and_route[car_id][1]
        
        dict_road_car_in_init_list[first_road][start_cross_id].append(car_id)
    
    for road_id in dict_road_state_map:
        for direction in dict_road_car_in_init_list[road_id]:
            dict_road_car_in_init_list[road_id][direction] = sorted(dict_road_car_in_init_list[road_id][direction], key = lambda x: (-int(dict_car[x][4]), int(dict_departure_time_and_route[x][0]), int(x)))

# drive_just_current_road: only one channel
def drive_just_current_road(road_id, direction, lane, dict_road, dict_car, dict_road_state_map, dict_car_state):
    road_length = int(dict_road[road_id][0])
    road_speed_limit = int(dict_road[road_id][1])
    
    front_car_location = None
    for location in range(road_length):
        car_id = dict_road_state_map[road_id][direction][lane][location]
        if car_id == None:
            continue
        else:
            speed = min(int(dict_car[car_id][2]), road_speed_limit)
            if front_car_location == None:
                if location - speed >= 0:
                    dict_car_state[car_id][0] = "end"
                    dict_car_state[car_id][1] = [road_id, direction, lane, location - speed]
                    dict_road_state_map[road_id][direction][lane][location] = None
                    dict_road_state_map[road_id][direction][lane][location - speed] = car_id
                    front_car_location = location - speed
                else:
                    front_car_location = location
            else:
                if location - speed > front_car_location:
                    dict_car_state[car_id][0] = "end"
                    dict_car_state[car_id][1] = [road_id, direction, lane, location - speed]
                    dict_road_state_map[road_id][direction][lane][location] = None
                    dict_road_state_map[road_id][direction][lane][location - speed] = car_id
                    front_car_location = location - speed
                elif dict_car_state[dict_road_state_map[road_id][direction][lane][front_car_location]][0] == "end":
                    dict_car_state[car_id][0] = "end"
                    dict_car_state[car_id][1] = [road_id, direction, lane, front_car_location + 1]
                    dict_road_state_map[road_id][direction][lane][location] = None
                    dict_road_state_map[road_id][direction][lane][front_car_location + 1] = car_id
                    front_car_location += 1
                else:
                    front_car_location = location

def drive_car_init_list(priority, road_id, direction, dict_road, dict_car, dict_road_car_in_init_list, dict_departure_time_and_route, dict_car_state, dict_road_state_map):
    #priority: True: only priority cars; False: all cars.
    road_length = int(dict_road[road_id][0])
    road_speed_limit = int(dict_road[road_id][1])
    
    # Now only priority cars.
    for car_id in dict_road_car_in_init_list[road_id][direction]:
        if priority == True:
            if t < int(dict_departure_time_and_route[car_id][0]) or dict_car[car_id][4] == "0":
                continue
        else:
            if t < int(dict_departure_time_and_route[car_id][0]):
                continue
        speed = min(int(dict_car[car_id][2]), road_speed_limit)
                
        end_loop = False
        for lane in dict_road_state_map[road_id][direction]:
            all_empty = True
            for j in range(speed):
                front_car_id = dict_road_state_map[road_id][direction][lane][road_length - 1 - j]
                if front_car_id == None:
                    continue
                elif dict_car_state[front_car_id][0] == "wait":
                    end_loop = True
                    break
                else: #dict_car_state[front_car_id][0] == "end":
                    if j == 0:
                        all_empty = False
                        break
                    else:
                        dict_car_state[car_id][0] = "end"
                        dict_car_state[car_id][1] = [road_id, direction, lane, road_length - j]
                        dict_road_state_map[road_id][direction][lane][road_length - j] = car_id
                        dict_road_car_in_init_list[road_id][direction].remove(car_id)
                        end_loop = True
                        break
                    
            if end_loop == True:
                break
                    
            if all_empty == True:
                dict_car_state[car_id][0] = "end"
                dict_car_state[car_id][1] = [road_id, direction, lane, road_length - speed]
                dict_road_state_map[road_id][direction][lane][road_length - speed] = car_id
                dict_road_car_in_init_list[road_id][direction].remove(car_id)
                break

def create_sequence(road_id, direction, dict_road, dict_car, dict_road_state_map, dict_car_state, dict_car_sequence_at_corss):
    
    car_sequence = []
        
    road_width = int(dict_road[road_id][2])
    road_speed_limit = int(dict_road[road_id][1])
    road_length = int(dict_road[road_id][0])
    
    list_sequence_per_lane = [0] * road_width
    
    while(True):
        if list_sequence_per_lane == [road_length] * road_width:
            break
            
        list_priority_per_lane = [False] * road_width
    
        for lane in dict_road_state_map[road_id][direction]:
            if list_sequence_per_lane[lane] == road_length:
                continue
                
            car_id = dict_road_state_map[road_id][direction][lane][list_sequence_per_lane[lane]]
            
            while(car_id == None and list_sequence_per_lane[lane] < road_length - 1):
                list_sequence_per_lane[lane] += 1
                car_id = dict_road_state_map[road_id][direction][lane][list_sequence_per_lane[lane]]
            
            if car_id == None and list_sequence_per_lane[lane] == road_length - 1:
                list_sequence_per_lane[lane] += 1
                continue
            
            if dict_car_state[car_id][0] == "end" or list_sequence_per_lane[lane] >= min(int(dict_car[car_id][2]), road_speed_limit):
                list_sequence_per_lane[lane] = road_length
                continue
            
            if dict_car[car_id][4] == "1":
                list_priority_per_lane[lane] = True
        
        if list_sequence_per_lane == [road_length] * road_width:
            break
        
        if list_priority_per_lane != [False] * road_width:
            frontest_location = road_length
            frontest_lane = None
            for lane in dict_road_state_map[road_id][direction]:
                if list_priority_per_lane[lane] == False:
                    continue
                else:
                    if list_sequence_per_lane[lane] < frontest_location:
                        frontest_location = list_sequence_per_lane[lane]
                        frontest_lane = lane
                        car_sequence = car_sequence + [dict_road_state_map[road_id][direction][lane][list_sequence_per_lane[lane]]]
                        list_sequence_per_lane[lane] += 1
                        break
                        
        else:
            frontest_location = road_length
            frontest_lane = None
            for lane in dict_road_state_map[road_id][direction]:
                if list_sequence_per_lane[lane] < frontest_location:
                    frontest_location = list_sequence_per_lane[lane]
                    frontest_lane = lane
                    car_sequence = car_sequence + [dict_road_state_map[road_id][direction][lane][list_sequence_per_lane[lane]]]
                    list_sequence_per_lane[lane] += 1
                    break
                    
    dict_car_sequence_at_corss[road_id][direction] = car_sequence

def drive_car_in_wait_state(dict_cross, dict_road, dict_car_state, dict_car_sequence_at_corss):

    while(no_car_in_wait_state(dict_car_state) == False):
        dead_lock = True
        for cross_id in dict_cross: 
            list_road = []
            for i in range(4):
                if dict_cross[cross_id][i] != "-1":
                    list_road.append(dict_cross[cross_id][i])
            list_road = sorted(list_road, key = lambda x: int(x))
            
            for road_id in list_road:
                start_cross_id = dict_road[road_id][3]
                end_cross_id = dict_road[road_id][4]
                two_way = dict_road[road_id][5]
                if cross_id == start_cross_id and two_way == "0":
                    continue
                elif cross_id == start_cross_id:
                    direction = end_cross_id
                else:
                    direction = start_cross_id
                
                while(len(dict_car_sequence_at_corss[road_id][direction]) != 0):
                    car_id = dict_car_sequence_at_corss[road_id][direction][0]
                    
                    current_lane = dict_car_state[car_id][1][2]
                    current_location = dict_car_state[car_id][1][3]
                    
                    if(conflict_at_cross(car_id, cross_id, road_id, dict_cross, dict_road, dict_car_sequence_at_corss, dict_departure_time_and_route)):
                        break
                        
                    if(move_to_next_road(car_id, road_id, direction, current_lane, current_location, cross_id, dict_road, dict_car, dict_road_state_map, dict_car_state, dict_departure_time_and_route)):
                        drive_just_current_road(road_id, direction, current_lane, dict_road, dict_car, dict_road_state_map, dict_car_state)
                        create_sequence(road_id, direction, dict_road, dict_car, dict_road_state_map, dict_car_state, dict_car_sequence_at_corss)
                        drive_car_init_list(True, road_id, direction, dict_road, dict_car, dict_road_car_in_init_list, dict_departure_time_and_route, dict_car_state, dict_road_state_map)                        
                        dead_lock = False
                    else:
                        break
        if(dead_lock):
            return False
    return True

def find_next_road_id(car_id, current_road_id, dict_departure_time_and_route):
    i = 1
    while(True):
        if dict_departure_time_and_route[car_id][i] == current_road_id:
            if i == len(dict_departure_time_and_route[car_id]) - 1:
                return "destination"
            else:
                return dict_departure_time_and_route[car_id][i + 1]
            break
        i += 1

def no_car_in_wait_state(dict_car_state):
    for car_id in dict_car_state:
        if dict_car_state[car_id][0] == "wait":
            return False
    return True

def conflict_at_cross(car_id, cross_id, current_road_id, dict_cross, dict_road, dict_car_sequence_at_corss, dict_departure_time_and_route):
    next_road_id = find_next_road_id(car_id, current_road_id, dict_departure_time_and_route)
    
    if dict_car[car_id][4] == "1":
        if next_road_id == "destination":
            return False
    
        current_car_turn = judge_direction(dict_cross, cross_id, current_road_id, next_road_id)
    
        if current_car_turn == "straight":
            return False
    
        elif current_car_turn == "left":
            right_road_id = "-1"
            for road_id in dict_cross[cross_id]:
                if road_id == "-1":
                    continue
                elif judge_direction(dict_cross, cross_id, current_road_id, road_id) == "right":
                    right_road_id = road_id
                    break
        
            if right_road_id == "-1":
                return False
        
            start_cross_id = dict_road[right_road_id][3]
            end_cross_id = dict_road[right_road_id][4]
            two_way = dict_road[right_road_id][5]
            if cross_id == start_cross_id and two_way == "0":
                return False
            elif cross_id == start_cross_id:
                right_road_direction = end_cross_id
            else:
                right_road_direction = start_cross_id
            
            if len(dict_car_sequence_at_corss[right_road_id][right_road_direction]) == 0:
                return False
            else:
                right_road_car_id = dict_car_sequence_at_corss[right_road_id][right_road_direction][0]
                if dict_car[right_road_car_id][4] == "1":
                    right_road_next_road_id = find_next_road_id(right_road_car_id, right_road_id, dict_departure_time_and_route)
                    if right_road_next_road_id == "destination":
                        return True
                    elif judge_direction(dict_cross, cross_id, right_road_id, right_road_next_road_id) == "straight":
                        return True
                    else:
                        return False
                else:
                    return False
        
        else: #current_car_turn == "right":
            # left_road: if go straight
            left_road_id = "-1"
            for road_id in dict_cross[cross_id]:
                if road_id == "-1":
                    continue
                if judge_direction(dict_cross, cross_id, current_road_id, road_id) == "left":
                    left_road_id = road_id
                    break
        
            if left_road_id == "-1":
                no_left_road = True
            else:
                no_left_road = False
                    
                start_cross_id = dict_road[left_road_id][3]
                end_cross_id = dict_road[left_road_id][4]
                two_way = dict_road[left_road_id][5]
                if cross_id == start_cross_id and two_way == "0":
                    no_left_road = True
                elif cross_id == start_cross_id:
                    left_road_direction = end_cross_id
                else:
                    left_road_direction = start_cross_id
        
            if not no_left_road:
                if len(dict_car_sequence_at_corss[left_road_id][left_road_direction]) != 0:
                    left_road_car_id = dict_car_sequence_at_corss[left_road_id][left_road_direction][0]
                    if dict_car[left_road_car_id][4] == "1":
                        left_road_next_road_id = find_next_road_id(left_road_car_id, left_road_id, dict_departure_time_and_route)
                        if left_road_next_road_id == "destination":
                            return True
                        elif judge_direction(dict_cross, cross_id, left_road_id, left_road_next_road_id) == "straight":
                            return True
        
            #straight_road: if go left
            straight_road_id = "-1"
            for road_id in dict_cross[cross_id]:
                if road_id == "-1":
                    continue
                if judge_direction(dict_cross, cross_id, current_road_id, road_id) == "straight":
                    straight_road_id = road_id
                    break
                
            if straight_road_id == "-1":
                return False
        
            start_cross_id = dict_road[straight_road_id][3]
            end_cross_id = dict_road[straight_road_id][4]
            two_way = dict_road[straight_road_id][5]
            if cross_id == start_cross_id and two_way == "0":
                return False
            elif cross_id == start_cross_id:
                straight_road_direction = end_cross_id
            else:
                straight_road_direction = start_cross_id
            
            if len(dict_car_sequence_at_corss[straight_road_id][straight_road_direction]) == 0:
                return False
            else:
                straight_road_car_id = dict_car_sequence_at_corss[straight_road_id][straight_road_direction][0]
                if dict_car[straight_road_car_id][4] == "1":
                    straight_road_next_road_id = find_next_road_id(straight_road_car_id, straight_road_id, dict_departure_time_and_route)
                    if judge_direction(dict_cross, cross_id, straight_road_id, straight_road_next_road_id) == "left":
                        return True
                    else:
                        return False
                else:
                    return False
                
    else:
        right_road_id = "-1"
        for road_id in dict_cross[cross_id]:
            if road_id == "-1":
                continue
            elif judge_direction(dict_cross, cross_id, current_road_id, road_id) == "right":
                right_road_id = road_id
                break
                
        straight_road_id = "-1"
        for road_id in dict_cross[cross_id]:
            if road_id == "-1":
                continue
            if judge_direction(dict_cross, cross_id, current_road_id, road_id) == "straight":
                straight_road_id = road_id
                break
        
        left_road_id = "-1"
        for road_id in dict_cross[cross_id]:
            if road_id == "-1":
                continue
            if judge_direction(dict_cross, cross_id, current_road_id, road_id) == "left":
                left_road_id = road_id
                break
                
        for direction_road_id in [right_road_id, straight_road_id, left_road_id]:
            if direction_road_id == "-1":
                continue
            else:
                start_cross_id = dict_road[direction_road_id][3]
                end_cross_id = dict_road[direction_road_id][4]
                two_way = dict_road[direction_road_id][5]
                if cross_id == start_cross_id and two_way == "0":
                    continue
                elif cross_id == start_cross_id:
                    direction_road_direction = end_cross_id
                else:
                    direction_road_direction = start_cross_id
            
                if len(dict_car_sequence_at_corss[direction_road_id][direction_road_direction]) == 0:
                    continue
                else:
                    direction_road_car_id = dict_car_sequence_at_corss[direction_road_id][direction_road_direction][0]
                    if dict_car[direction_road_car_id][4] == "1":
                        return True
                    else:
                        continue
            
        if next_road_id == "destination":
            return False
    
        current_car_turn = judge_direction(dict_cross, cross_id, current_road_id, next_road_id)
    
        if current_car_turn == "straight":
            return False
    
        elif current_car_turn == "left":
            if right_road_id == "-1":
                return False
        
            start_cross_id = dict_road[right_road_id][3]
            end_cross_id = dict_road[right_road_id][4]
            two_way = dict_road[right_road_id][5]
            if cross_id == start_cross_id and two_way == "0":
                return False
            elif cross_id == start_cross_id:
                right_road_direction = end_cross_id
            else:
                right_road_direction = start_cross_id
            
            if len(dict_car_sequence_at_corss[right_road_id][right_road_direction]) == 0:
                return False
            else:
                right_road_car_id = dict_car_sequence_at_corss[right_road_id][right_road_direction][0]
                right_road_next_road_id = find_next_road_id(right_road_car_id, right_road_id, dict_departure_time_and_route)
                if right_road_next_road_id == "destination":
                    return True
                elif judge_direction(dict_cross, cross_id, right_road_id, right_road_next_road_id) == "straight":
                    return True
                else:
                    return False
        
        else: #current_car_turn == "right":
            # left_road: if go straight        
            if left_road_id == "-1":
                no_left_road = True
            else:
                no_left_road = False
                    
                start_cross_id = dict_road[left_road_id][3]
                end_cross_id = dict_road[left_road_id][4]
                two_way = dict_road[left_road_id][5]
                if cross_id == start_cross_id and two_way == "0":
                    no_left_road = True
                elif cross_id == start_cross_id:
                    left_road_direction = end_cross_id
                else:
                    left_road_direction = start_cross_id
        
            if not no_left_road:
                if len(dict_car_sequence_at_corss[left_road_id][left_road_direction]) != 0:
                    left_road_car_id = dict_car_sequence_at_corss[left_road_id][left_road_direction][0]
                    left_road_next_road_id = find_next_road_id(left_road_car_id, left_road_id, dict_departure_time_and_route)
                    if left_road_next_road_id == "destination":
                        return True
                    elif judge_direction(dict_cross, cross_id, left_road_id, left_road_next_road_id) == "straight":
                        return True
        
            #straight_road: if go left
            if straight_road_id == "-1":
                return False
        
            start_cross_id = dict_road[straight_road_id][3]
            end_cross_id = dict_road[straight_road_id][4]
            two_way = dict_road[straight_road_id][5]
            if cross_id == start_cross_id and two_way == "0":
                return False
            elif cross_id == start_cross_id:
                straight_road_direction = end_cross_id
            else:
                straight_road_direction = start_cross_id
            
            if len(dict_car_sequence_at_corss[straight_road_id][straight_road_direction]) == 0:
                return False
            else:
                straight_road_car_id = dict_car_sequence_at_corss[straight_road_id][straight_road_direction][0]
                straight_road_next_road_id = find_next_road_id(straight_road_car_id, straight_road_id, dict_departure_time_and_route)
                if judge_direction(dict_cross, cross_id, straight_road_id, straight_road_next_road_id) == "left":
                    return True
                else:
                    return False

def move_to_next_road(car_id, current_road_id, current_direction, current_lane, current_location, cross_id, dict_road, dict_car, dict_road_state_map, dict_car_state, dict_departure_time_and_route):
    
    next_road_id = find_next_road_id(car_id, current_road_id, dict_departure_time_and_route)
    
    if next_road_id == "destination":
        dict_car_state[car_id][0] = "finished"
        dict_car_state[car_id][1] = "garage"
        dict_road_state_map[current_road_id][current_direction][current_lane][current_location] = None
        return True
    
    next_road_length = int(dict_road[next_road_id][0])
    current_speed = min(int(dict_car[car_id][2]), int(dict_road[current_road_id][1]))
    future_speed = min(int(dict_car[car_id][2]), int(dict_road[next_road_id][1]))
    future_max_displacement = future_speed - current_location
    if future_max_displacement < 0:
        future_max_displacement = 0
        
    # next_road_all_full or future_max_displacement == 0:
    all_full = True
    for lane in dict_road_state_map[next_road_id][cross_id]:
        if dict_road_state_map[next_road_id][cross_id][lane][next_road_length - 1] == None:
            all_full = False
        elif dict_car_state[dict_road_state_map[next_road_id][cross_id][lane][next_road_length - 1]][0] == "wait":
            all_full = False
            
    if all_full or future_max_displacement == 0:
        if current_location == 0:
            dict_car_state[car_id][0] = "end"
            return True
        else:
            dict_car_state[car_id][0] = "end"
            dict_car_state[car_id][1] = [current_road_id, current_direction, current_lane, 0]
            dict_road_state_map[current_road_id][current_direction][current_lane][current_location] = None
            dict_road_state_map[current_road_id][current_direction][current_lane][0] = car_id
            return True
 
    # can enter the next road, no car in front or all the front car is in "end" state
    # or can enter the next road, the front car is in "wait" state
    for lane in dict_road_state_map[next_road_id][cross_id]:
        if dict_road_state_map[next_road_id][cross_id][lane][next_road_length - 1] != None:
            if dict_car_state[dict_road_state_map[next_road_id][cross_id][lane][next_road_length - 1]][0] == "end":
                continue
            elif dict_car_state[dict_road_state_map[next_road_id][cross_id][lane][next_road_length - 1]][0] == "wait":
                return False
        
        for j in range(future_max_displacement):
            if dict_road_state_map[next_road_id][cross_id][lane][next_road_length - 1 - j] == None:
                next_location = next_road_length - 1 - j
                if j != future_max_displacement - 1:
                    continue
                elif j == future_max_displacement - 1:
                    dict_car_state[car_id][0] = "end"
                    dict_car_state[car_id][1] = [next_road_id, cross_id, lane, next_location]
                    dict_road_state_map[current_road_id][current_direction][current_lane][current_location] = None
                    dict_road_state_map[next_road_id][cross_id][lane][next_location] = car_id
                    return True
            elif dict_car_state[dict_road_state_map[next_road_id][cross_id][lane][next_road_length - 1 - j]][0] == "wait":
                return False
            elif dict_car_state[dict_road_state_map[next_road_id][cross_id][lane][next_road_length - 1 - j]][0] == "end":
                next_location = next_road_length - j
                dict_car_state[car_id][0] = "end"
                dict_car_state[car_id][1] = [next_road_id, cross_id, lane, next_location]
                dict_road_state_map[current_road_id][current_direction][current_lane][current_location] = None
                dict_road_state_map[next_road_id][cross_id][lane][next_location] = car_id
                return True

def is_finish(dict_car_state):
    for car_id in dict_car_state:
        if dict_car_state[car_id][0] != "finished":
            return False
    return True

def get_finish_car(dict_car_state):
    num = 0
    for car_id in dict_car_state:
        if dict_car_state[car_id][0] == "finished":
            num += 1
    return num

def choose_preset_car_to_update(dict_preset_answer, dict_shortest_path, dict_car, dict_road, dict_G_all_speed, num_to_update_preset):
    dict_value_difference = dict()
    dict_value_difference = collections.OrderedDict()
    
    for car_id in dict_preset_answer:
        car_speed = dict_car[car_id][2]
        car_start_cross_id = dict_car[car_id][0]
        #end_cross_id = dict_car[car_id][1]
        
        preset_path = dict_preset_answer[car_id][1:]
        shortest_path = dict_shortest_path[car_id]
        
        preset_road_value = 0
        shortest_path_road_value = 0
        
        for i in range(len(preset_path)):
            road_id = preset_path[i]
            if i == 0:
                start_cross_id = car_start_cross_id
            else:
                start_cross_id = end_cross_id
                
            if start_cross_id == dict_road[road_id][3]:
                end_cross_id = dict_road[road_id][4]
            else:
                end_cross_id = dict_road[road_id][3]
            preset_road_value += get_road_value(dict_G_all_speed[car_speed], start_cross_id, end_cross_id)
            
            if i < len(preset_path) - 1:
                next_road_id = preset_path[i + 1]
                
                direction = judge_direction(dict_cross, end_cross_id, road_id, next_road_id)
                
                if direction == "left" or direction == "right":
                    preset_road_value += 16
                    
        for i in range(len(shortest_path)):
            road_id = shortest_path[i]
            if i == 0:
                start_cross_id = car_start_cross_id
            else:
                start_cross_id = end_cross_id
                
            if start_cross_id == dict_road[road_id][3]:
                end_cross_id = dict_road[road_id][4]
            else:
                end_cross_id = dict_road[road_id][3]
            shortest_path_road_value += get_road_value(dict_G_all_speed[car_speed], start_cross_id, end_cross_id)
            
            if i < len(preset_path) - 1:
                next_road_id = preset_path[i + 1]
                
                direction = judge_direction(dict_cross, end_cross_id, road_id, next_road_id)
                
                if direction == "left" or direction == "right":
                    shortest_path_road_value += 16
        
        dict_value_difference[car_id] = shortest_path_road_value - preset_road_value

    list_sorted_dict_value_difference = sorted(dict_value_difference.items(), key = lambda x: int(x[1]))
    
    cars_to_update_in_preset = []
                    
    for j in range(num_to_update_preset):
        cars_to_update_in_preset.append(list_sorted_dict_value_difference[j][0])
    
    return cars_to_update_in_preset
        

def main():
    global dict_car
    global dict_road
    global dict_cross
    global dict_preset_answer
    global dict_G_all_speed
    global dict_shortest_path_last_cross
    global dict_shortest_path
    global dict_shortest_path
    global dict_answer
    global list_unstarted_car
    global num_to_update_preset
    global list_cars_to_update_in_preset
    global dict_car_state
    global dict_departure_time_and_route
    global dict_road_state_map
    global dict_road_car_in_init_list
    global dict_car_sequence_at_corss
    global t

    if len(sys.argv) != 6:
        logging.info('please input args: car_path, road_path, cross_path, answerPath')
        exit(1)

    car_path = sys.argv[1]
    road_path = sys.argv[2]
    cross_path = sys.argv[3]
    preset_answer_path = sys.argv[4]
    answer_path = sys.argv[5]

    logging.info("car_path is %s" % (car_path))
    logging.info("road_path is %s" % (road_path))
    logging.info("cross_path is %s" % (cross_path))
    logging.info("preset_answer_path is %s" % (preset_answer_path))
    logging.info("answer_path is %s" % (answer_path))

    add_to_dict(car_path, dict_car)
    add_to_dict(road_path, dict_road)
    add_to_dict(cross_path, dict_cross)
    add_to_dict(preset_answer_path, dict_preset_answer)
    
    sorted_list_dict_cross = sorted(dict_cross.items(), key = lambda x: int(x[0]))
    dict_cross = dict()
    dict_cross = collections.OrderedDict()
    for item in sorted_list_dict_cross:
        dict_cross[item[0]] = item[1]
    
    construct_dict_G_all_speed(dict_G_all_speed, dict_car)
    construct_graph(dict_G_all_speed, dict_cross, dict_road)
    
    construct_dict_shortest_path_last_cross(dict_shortest_path_last_cross, dict_G_all_speed)
    
    get_shortest_paths(dict_G_all_speed, dict_shortest_path_last_cross, dict_shortest_path, dict_car, dict_cross)

    num_to_update_preset = math.floor(len(dict_preset_answer) * 0.1)

    list_cars_to_update_in_preset = choose_preset_car_to_update(dict_preset_answer, dict_shortest_path, dict_car, dict_road, dict_G_all_speed, num_to_update_preset)

    for car_id in dict_car:
        if dict_car[car_id][5] == "0":
            list_unstarted_car.append(car_id)
    
    for car_id in list_cars_to_update_in_preset:
        dict_preset_answer[car_id] = [dict_preset_answer[car_id][0]] + dict_shortest_path[car_id]
        dict_answer[car_id] = dict_preset_answer[car_id]

    initialize_judgement(dict_preset_answer, dict_car, dict_road, dict_car_state, dict_departure_time_and_route, dict_road_state_map, dict_road_car_in_init_list, dict_car_sequence_at_corss)

    while(True):
        t += 1
    
        num_car_in_preset_answer = 0
        if t < 340:
            for car_id in dict_preset_answer:
                if int(dict_preset_answer[car_id][0]) == t:
                    num_car_in_preset_answer += 1
    
        num_car_on_road = 0
        for car_id in dict_car_state:
            if dict_car_state[car_id][0] == "end":
                num_car_on_road += 1
    
        if len(dict_preset_answer) < 3300:
            if t < 100:
                num_car_to_start = min(min(t * 12, 1200) - num_car_in_preset_answer - num_car_on_road, 30 + math.sin(t))
            elif t < 180:
                num_car_to_start = min(1200 - num_car_in_preset_answer - num_car_on_road, 20 + math.sin(t))
            elif t < 255:
                num_car_to_start = 1800 - (255 - t) * 8 - num_car_in_preset_answer - num_car_on_road
            else:
                num_car_to_start = min(1800 - num_car_on_road, 50)
        else:
            if t < 100:
                num_car_to_start = min(min(t * 12, 1200) - num_car_in_preset_answer - num_car_on_road, 30 + math.sin(t))
            elif t < 320:
                num_car_to_start = min(1200 - num_car_in_preset_answer - num_car_on_road, 20 + math.sin(t))
            elif t < 395:
                num_car_to_start = 1800 - (395 - t) * 8 - num_car_in_preset_answer - num_car_on_road
            else:
                num_car_to_start = min(1800 - num_car_on_road, 50)
    
        dict_road_occupancy = dict()
        dict_road_occupancy = collections.OrderedDict()
    
        for road_id in dict_road_state_map:
            road_length = int(dict_road[road_id][0])
            road_width = int(dict_road[road_id][2])
            for direction in dict_road_state_map[road_id]:
                num_car_on_this_road = 0
                for lane in dict_road_state_map[road_id][direction]:
                    for car_id in dict_road_state_map[road_id][direction][lane]:
                        if car_id != None:
                            num_car_on_this_road += 1
                dict_road_occupancy[(road_id, direction)] = num_car_on_this_road / road_length / road_width
        
        if (t <= 400 or (t > 400 and t % 2 == 1)) and num_car_to_start > 0:
            if t <= 400:
                list_unstarted_car = sorted(list_unstarted_car, key = lambda x: (-int(dict_car[x][4]), get_average_occupancy(x, dict_car, dict_road, dict_road_occupancy, dict_shortest_path), int(x)))#int(dict_car[x][2]), 
            else:
                list_unstarted_car = sorted(list_unstarted_car, key = lambda x: (-int(dict_car[x][4]), -int(dict_car[x][2]), get_average_occupancy(x, dict_car, dict_road, dict_road_occupancy, dict_shortest_path), int(x)))# 
    
        list_car_to_start = []
    
        dict_car_start_at_this_second = dict()
        dict_car_start_at_this_second = collections.OrderedDict()
    
        for item in dict_road_occupancy:
            dict_car_start_at_this_second[item] = 0
    
        for car_id in list_unstarted_car:
            if num_car_to_start <= 0:
                break
            
            if t <= 300:
                if dict_car_start_at_this_second[(dict_shortest_path[car_id][0], dict_car[car_id][0])] > 1:
                    continue
            else:
                if dict_car_start_at_this_second[(dict_shortest_path[car_id][0], dict_car[car_id][0])] > 2 * int(dict_road[dict_shortest_path[car_id][0]][2]):
                    continue
        
            if t < int(dict_car[car_id][3]):
                continue
            
            dict_car_start_at_this_second[(dict_shortest_path[car_id][0], dict_car[car_id][0])] += 1
            list_car_to_start.append(car_id)
            num_car_to_start -= 1
        
        for car_id in list_car_to_start:
            list_unstarted_car.remove(car_id)
        
            dict_answer[car_id] = [str(t)] + dict_shortest_path[car_id]
            dict_departure_time_and_route[car_id] = [str(t)] + dict_shortest_path[car_id]
        
            dict_car_state[car_id] = ["sleep", "garage"]
            dict_road_car_in_init_list[dict_shortest_path[car_id][0]][dict_car[car_id][0]].append(car_id)
        
        for road_id in dict_road_state_map:
            for direction in dict_road_car_in_init_list[road_id]:
                dict_road_car_in_init_list[road_id][direction] = sorted(dict_road_car_in_init_list[road_id][direction], key = lambda x: (-int(dict_car[x][4]), int(dict_departure_time_and_route[x][0]), int(x)))
    
        for car_id in dict_car_state:
            if dict_car_state[car_id][0] == "end":
                dict_car_state[car_id][0] = "wait"
        
        for road_id in dict_road_state_map:
            for direction in dict_road_state_map[road_id]:
                for lane in dict_road_state_map[road_id][direction]:
                    drive_just_current_road(road_id, direction, lane, dict_road, dict_car, dict_road_state_map, dict_car_state)

        for road_id in dict_road_car_in_init_list:
            for direction in dict_road_car_in_init_list[road_id]:
                drive_car_init_list(True, road_id, direction, dict_road, dict_car, dict_road_car_in_init_list, dict_departure_time_and_route, dict_car_state, dict_road_state_map) 

        for road_id in dict_road_state_map:
            for direction in dict_road_state_map[road_id]:
                create_sequence(road_id, direction, dict_road, dict_car, dict_road_state_map, dict_car_state, dict_car_sequence_at_corss)
        
        if(not drive_car_in_wait_state(dict_cross, dict_road, dict_car_state, dict_car_sequence_at_corss)):
            #print(t, "deadlock")
            break
    
        for road_id in dict_road_car_in_init_list:
            for direction in dict_road_car_in_init_list[road_id]:
                drive_car_init_list(False, road_id, direction, dict_road, dict_car, dict_road_car_in_init_list, dict_departure_time_and_route, dict_car_state, dict_road_state_map) 

        #print(t, len(list_car_to_start), num_car_in_preset_answer, num_car_on_road, len(list_unstarted_car), get_finish_car(dict_car_state))
    
        if(len(list_unstarted_car) == 0): # and is_finish(dict_car_state)
            #print(t, "finish")
            break
        
    write_to_txt(answer_path, dict_answer)

# to read input file
# process
# to write output file

dict_car = dict()
dict_car = collections.OrderedDict()
dict_road = dict()
dict_road = collections.OrderedDict()
dict_cross = dict()
dict_cross = collections.OrderedDict()
dict_preset_answer = dict()
dict_preset_answer = collections.OrderedDict()

dict_G_all_speed = dict()
dict_G_all_speed = collections.OrderedDict()

dict_shortest_path_last_cross = dict()
dict_shortest_path_last_cross = collections.OrderedDict()

dict_shortest_path = dict()
dict_shortest_path = collections.OrderedDict()

dict_answer = dict()
dict_answer = collections.OrderedDict()

list_unstarted_car = []

num_to_update_preset = 0

list_cars_to_update_in_preset = []

dict_car_state = dict()
dict_car_state = collections.OrderedDict()
    
dict_departure_time_and_route = dict()
dict_departure_time_and_route = collections.OrderedDict()
    
dict_road_state_map = dict()
dict_road_state_map = collections.OrderedDict()
    
dict_road_car_in_init_list = dict()
dict_road_car_in_init_list = collections.OrderedDict()
    
dict_car_sequence_at_corss = dict()
dict_car_sequence_at_corss = collections.OrderedDict()

t = 0

if __name__ == "__main__":
    main()
