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
        if item[0]=="#":
            continue
        else:
            list_one_item = item.replace(' ', '').strip('()').split(',')
            dict_name[list_one_item[0]] = list_one_item[1:]

def sort_dict_car(dict_car):
    return sorted(dict_car.items(), key = lambda x: (-int(x[1][2]), x[1][3], x[0]))#, x[1][1]#

def get_total_lanes(dict_road):
    total_lanes = 0
    for road_id in dict_road:
        total_lanes += int(dict_road[road_id][2])
    return total_lanes

def construct_road_map(dict_road_map, dict_car, dict_cross, dict_road):
    sorted_list_car = sort_dict_car(dict_car)
    zero_point_cross_id = sorted_list_car[0][1][0]
    dict_road_map[zero_point_cross_id] = (0, 0)
    
    for i in range(4):
        road_id = dict_cross[zero_point_cross_id][i]
        
        if road_id == "-1":
            continue
            
        if zero_point_cross_id == dict_road[road_id][3]:
            next_cross_id = dict_road[road_id][4]
        else:
            next_cross_id = dict_road[road_id][3]
            
        road_length = int(dict_road[road_id][0])
        
        if i == 0:
            dict_road_map[next_cross_id] = (dict_road_map[zero_point_cross_id][0], dict_road_map[zero_point_cross_id][1] + road_length)
        elif i == 1:
            dict_road_map[next_cross_id] = (dict_road_map[zero_point_cross_id][0] + road_length, dict_road_map[zero_point_cross_id][1])
        elif i == 2:
            dict_road_map[next_cross_id] = (dict_road_map[zero_point_cross_id][0], dict_road_map[zero_point_cross_id][1] - road_length)
        elif i == 3:
            dict_road_map[next_cross_id] = (dict_road_map[zero_point_cross_id][0] - road_length, dict_road_map[zero_point_cross_id][1])
            
        update_road_map(dict_road_map, dict_cross, dict_road, road_id, next_cross_id, i)
    
def update_road_map(dict_road_map, dict_cross, dict_road, original_road_id, cross_id, direction_index):
    for i in range(4):
        road_id = dict_cross[cross_id][i]

        if road_id == "-1" or road_id == original_road_id:
            continue
        
        if cross_id == dict_road[road_id][3]:
            next_cross_id = dict_road[road_id][4]
        else:
            next_cross_id = dict_road[road_id][3]
        
        if next_cross_id in dict_road_map:
            continue
        
        direction = judge_direction(dict_cross, cross_id, original_road_id, road_id)
        
        if direction == "straight":
            new_direction_index = direction_index
        elif direction == "left":
            new_direction_index = (direction_index + 3) % 4
        else:
            new_direction_index = (direction_index + 1) % 4
        
        road_length = int(dict_road[road_id][0])
        
        if new_direction_index == 0:
            dict_road_map[next_cross_id] = (dict_road_map[cross_id][0], dict_road_map[cross_id][1] + road_length)
        elif new_direction_index == 1:
            dict_road_map[next_cross_id] = (dict_road_map[cross_id][0] + road_length, dict_road_map[cross_id][1])
        elif new_direction_index == 2:
            dict_road_map[next_cross_id] = (dict_road_map[cross_id][0], dict_road_map[cross_id][1] - road_length)
        elif new_direction_index == 3:
            dict_road_map[next_cross_id] = (dict_road_map[cross_id][0] - road_length, dict_road_map[cross_id][1])
            
        update_road_map(dict_road_map, dict_cross, dict_road, road_id, next_cross_id, new_direction_index)

def get_start_time(dict_road, dict_car, dict_answer):
    sorted_list_car = sort_dict_car(dict_car)
    total_lanes = get_total_lanes(dict_road)
    total_lanes /= 20
    t = 1
    i = 0
    
    if len(dict_road) < 250:
        for car_id in sorted_list_car:
            original_start_time = int(dict_car[car_id[0]][3])
            dict_answer[car_id[0]] = max(t, original_start_time)
            i += 1
            if i >= (55.8 - t / 60) * (1 + 0.3 * math.cos(t)):
                i = 0
                t += 1
    else:
        for car_id in sorted_list_car:
            original_start_time = int(dict_car[car_id[0]][3])
            dict_answer[car_id[0]] = max(t, original_start_time)
            i += 1
            if i >= (52.75 - t / 69) * (1 + 0.3 * math.cos(t)):
                i = 0
                t += 1

def get_start_time_angle(dict_road, dict_car, dict_cross, dict_answer):
    dict_road_map = dict()
    dict_road_map = collections.OrderedDict()
    construct_road_map(dict_road_map, dict_car, dict_cross, dict_road)
    
    dict_route_angle = dict()
    dict_route_angle = collections.OrderedDict()
    for car_id in dict_car:
        start_cross_id = dict_car[car_id][0]
        end_cross_id = dict_car[car_id][1]
        x = dict_road_map[end_cross_id][0] - dict_road_map[start_cross_id][0]
        y = dict_road_map[end_cross_id][1] - dict_road_map[start_cross_id][1]
        #if x >= 0:
        #    dict_route_angle[car_id] = math.atan2(x, y) * 180 / math.pi
        #else:
        #    dict_route_angle[car_id] = math.atan2(x, y) * 180 / math.pi + 360
        dict_route_angle[car_id] = math.atan2(x, y)
            #if dict_route_angle[car_id] > 90:
            #dict_route_angle[car_id] = dict_route_angle[car_id] - 90
        
    total_lanes = get_total_lanes(dict_road)
    total_lanes /= 20
    t = 1
    i = 0
    
    sorted_list_car = sorted(dict_car.items(), key = lambda x: (-int(x[1][2]), x[1][3], dict_route_angle[x[0]]))
    
    for car_id in sorted_list_car:
        original_start_time = int(dict_car[car_id[0]][3])
        dict_answer[car_id[0]] = max(t, original_start_time)
        i += 1
        if i >= total_lanes * (1 + 2 * math.cos(0.92 * t) + 1.2 / math.sqrt(t)):
        #if i >= total_lanes * (1 + (5 - math.pow((t / 100), 1.1)) * math.cos(t) + 1.2 / math.sqrt(t)):
            i = 0
            t += 1

def update_dict_real_time_road_information(dict_real_time_road_information, dict_path_vector, real_start_time):
    s = real_start_time
    
    for path_vector in dict_path_vector:
        t = dict_path_vector[path_vector]
        start_cross_id = path_vector[0]
        end_cross_id = path_vector[1]
        
        '''
        while s <= t:
            for i in range(6):
                if s + i not in dict_real_time_road_information:
                    dict_real_time_road_information[s + i] = dict()
                    dict_real_time_road_information[s + i] = collections.OrderedDict()
                if start_cross_id not in dict_real_time_road_information[s + i]:
                    dict_real_time_road_information[s + i][start_cross_id] = dict()
                    dict_real_time_road_information[s + i][start_cross_id] = collections.OrderedDict()
                if end_cross_id not in dict_real_time_road_information[s + i][start_cross_id]:
                    dict_real_time_road_information[s + i][start_cross_id][end_cross_id] = 0
                dict_real_time_road_information[s + i][start_cross_id][end_cross_id] = dict_real_time_road_information[s + i][start_cross_id][end_cross_id] + 0#math.pow(1 / 1.7, i)
            s += 1
        '''
        while s <= t:
            if s not in dict_real_time_road_information:
                dict_real_time_road_information[s] = dict()
                dict_real_time_road_information[s] = collections.OrderedDict()
            if start_cross_id not in dict_real_time_road_information[s]:
                dict_real_time_road_information[s][start_cross_id] = dict()
                dict_real_time_road_information[s][start_cross_id] = collections.OrderedDict()
            if end_cross_id not in dict_real_time_road_information[s][start_cross_id]:
                dict_real_time_road_information[s][start_cross_id][end_cross_id] = 0
            dict_real_time_road_information[s][start_cross_id][end_cross_id] = dict_real_time_road_information[s][start_cross_id][end_cross_id] + 1
            s += 1

def get_real_time_dict_road(dict_road, real_time_road_information):
    real_time_dict_road = dict()
    real_time_dict_road = collections.OrderedDict()
    for road_id in real_time_road_information:
        real_time_dict_road[road_id] = int(dict_road[road_id][0]) + real_time_road_information[road_id]
    return real_time_dict_road

def construct_graph(dict_cross, dict_road, car_speed, start_time, dict_real_time_road_information, first_car):
    G = dict()
    G = collections.OrderedDict()
    
    for road_id in dict_road:
        start_cross_id = dict_road[road_id][3]
        end_cross_id = dict_road[road_id][4]
        road_speed_limit = int(dict_road[road_id][1])
        road_length = int(dict_road[road_id][0])
        road_width = int(dict_road[road_id][2])
        real_speed = min(car_speed, road_speed_limit)
        
        if start_cross_id not in G:
            G[start_cross_id] = dict()
            G[start_cross_id] = collections.OrderedDict()
        if end_cross_id not in G[start_cross_id]:
            G[start_cross_id][end_cross_id] = [road_id, 0]
    
        G[start_cross_id][end_cross_id][1] = road_length / real_speed / math.pow(road_width, 0)
        
        if dict_road[road_id][5] == "1":
            if end_cross_id not in G:
                G[end_cross_id] = dict()
                G[end_cross_id] = collections.OrderedDict()
            if start_cross_id not in G[end_cross_id]:
                G[end_cross_id][start_cross_id] = [road_id, 0]
            
            G[end_cross_id][start_cross_id][1] = road_length / real_speed

    if not first_car:
        if road_width <= 2:
            for start_cross_id in dict_real_time_road_information[start_time]:
                for end_cross_id in dict_real_time_road_information[start_time][start_cross_id]:
                    if dict_real_time_road_information[start_time][start_cross_id][end_cross_id] >= road_length * road_width - start_time / 375:
                        G[start_cross_id][end_cross_id][1] = 9999
                    elif dict_real_time_road_information[start_time][start_cross_id][end_cross_id] >= road_length * road_width * (0.6 - start_time / 5000):
                        G[start_cross_id][end_cross_id][1] = G[start_cross_id][end_cross_id][1] + 17
                    #else:
#                       G[start_cross_id][end_cross_id][1] = G[start_cross_id][end_cross_id][1] + dict_real_time_road_information[start_time][start_cross_id][end_cross_id] / math.pow(road_width, 0) / real_speed

    return G

def get_shortest_path_last_cross_Dijkstra(G, start_cross_id, end_cross_id, dict_cross):
    distance = dict()
    distance = collections.OrderedDict()
    last_cross = dict()
    last_cross = collections.OrderedDict()
    confirmed = []
    
    for cross_id in G[start_cross_id]:
        distance[cross_id] = get_road_value(G, start_cross_id, cross_id)
        last_cross[cross_id] = start_cross_id
    confirmed.append(start_cross_id)
    
    if end_cross_id in confirmed:
        return last_cross

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
                distance[cross_id] = distance[next_corss_to_confirm] + direction_value + get_road_value(G, next_corss_to_confirm, cross_id)
                last_cross[cross_id] = next_corss_to_confirm
            elif distance[cross_id] > distance[next_corss_to_confirm] + direction_value + get_road_value(G, next_corss_to_confirm, cross_id):
                distance[cross_id] = distance[next_corss_to_confirm] + direction_value + get_road_value(G, next_corss_to_confirm, cross_id)
                last_cross[cross_id] = next_corss_to_confirm
        confirmed.append(next_corss_to_confirm)

        if end_cross_id in confirmed:
            return last_cross
        
        distance.pop(next_corss_to_confirm)

def get_road_id(G, start_cross_id, end_cross_id):
    return G[start_cross_id][end_cross_id][0]

def get_road_value(G, start_cross_id, end_cross_id):
    return int(G[start_cross_id][end_cross_id][1])

def judge_direction(dict_cross, cross_id, present_road_id, next_road_id):
    list_road = dict_cross[cross_id]
    if (present_road_id == list_road[0] and next_road_id == list_road[2]) or (present_road_id == list_road[1] and next_road_id == list_road[3]) or (present_road_id == list_road[2] and next_road_id == list_road[0]) or (present_road_id == list_road[3] and next_road_id == list_road[1]):
        return "straight"
    if (present_road_id == list_road[0] and next_road_id == list_road[1]) or (present_road_id == list_road[1] and next_road_id == list_road[2]) or (present_road_id == list_road[2] and next_road_id == list_road[3]) or (present_road_id == list_road[3] and next_road_id == list_road[0]):
        return "left"
    if (present_road_id == list_road[0] and next_road_id == list_road[3]) or (present_road_id == list_road[1] and next_road_id == list_road[0]) or (present_road_id == list_road[2] and next_road_id == list_road[1]) or (present_road_id == list_road[3] and next_road_id == list_road[2]):
        return "right"

def retrieve_shortest_path_and_vector(G, last_cross, end_cross_id, car_speed, real_start_time, dict_road):
    list_path = []
    dict_path_vector = dict()
    dict_path_vector = collections.OrderedDict()
    while end_cross_id in last_cross:
        road_id = get_road_id(G, last_cross[end_cross_id], end_cross_id)
        list_path = [road_id] + list_path
        dict_path_vector[(last_cross[end_cross_id], end_cross_id)] = real_start_time
        t = math.ceil(int(dict_road[road_id][0])) / max(car_speed, int(dict_road[road_id][2]))
        for item in dict_path_vector:
            dict_path_vector[item] = dict_path_vector[item] + t
        end_cross_id = last_cross[end_cross_id]
    return list_path, dict_path_vector

def write_to_txt(file_path, dict_answer):
    with open(file_path, 'w') as f:
        f.write("#(carId, StartTime, RoadId, ...)\n")
        for car_id in dict_answer:
            f.write("(" + car_id + ", ")
            f.write(", ".join(str(road_id) for road_id in dict_answer[car_id]))
            f.write(")\n")

def main():
    if len(sys.argv) != 5:
        logging.info('please input args: car_path, road_path, cross_path, answerPath')
        exit(1)

    car_path = sys.argv[1]
    road_path = sys.argv[2]
    cross_path = sys.argv[3]
    answer_path = sys.argv[4]

    logging.info("car_path is %s" % (car_path))
    logging.info("road_path is %s" % (road_path))
    logging.info("cross_path is %s" % (cross_path))
    logging.info("answer_path is %s" % (answer_path))

    dict_car = dict()
    dict_car = collections.OrderedDict()
    dict_road = dict()
    dict_road = collections.OrderedDict()
    dict_cross = dict()
    dict_cross = collections.OrderedDict()

    add_to_dict(car_path, dict_car)
    add_to_dict(road_path, dict_road)
    add_to_dict(cross_path, dict_cross)

    dict_answer = dict()
    dict_answer = collections.OrderedDict()

    get_start_time(dict_road, dict_car, dict_answer)
    #get_start_time_angle(dict_road, dict_car, dict_cross, dict_answer)

    dict_real_time_road_information = dict()
    dict_real_time_road_information = collections.OrderedDict()

    first_car = True

    #sorted_list_car = sort_dict_car(dict_car)

    for car_id in dict_answer:
    #for car_tuple in sorted_list_car:
        #car_id = car_tuple[0]
        real_start_time = int(dict_answer[car_id])
        car_speed = int(dict_car[car_id][2])
        start_cross_id = dict_car[car_id][0]
        end_cross_id = dict_car[car_id][1]
    
        # calculate graph
        G = construct_graph(dict_cross, dict_road, car_speed, real_start_time, dict_real_time_road_information, first_car)
    
        # calculate shortest path
        last_cross = get_shortest_path_last_cross_Dijkstra(G, start_cross_id, end_cross_id, dict_cross)
        list_path, dict_path_vector = retrieve_shortest_path_and_vector(G, last_cross, end_cross_id, car_speed, real_start_time, dict_road)
    
        # update dict_real_time_road_information
        update_dict_real_time_road_information(dict_real_time_road_information, dict_path_vector, real_start_time)
    
        # update answer
        dict_answer[car_id] = [str(dict_answer[car_id])] + list_path
    
        first_car = False

    write_to_txt(answer_path, dict_answer)

if __name__ == "__main__":
    main()
