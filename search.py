import heapq
from collections import deque
from itertools import permutations

def bfs_solve(game):
    start_state = game.get_initial_state()
    node_solution = {start_state: []}

    if game.is_goal(start_state):
        return node_solution[start_state]

    frontier = deque()
    frontier.append(start_state)
    explored = set()
    explored.add(start_state)

    while frontier:
        current_state = frontier.popleft()

        for action, next_state, cost in game.get_successors(current_state):
            solution = node_solution[current_state]

            if next_state not in explored:
                explored.add(next_state)
                node_solution[next_state] = solution + [action]

                if game.is_goal(next_state):
                    return node_solution[next_state]

                frontier.append(next_state)
    return None


def ids_solve(game):
    def dls_solve(game_dls, max_depth):
        start_state = game_dls.get_initial_state()
        node_solution = {start_state: []}

        if game.is_goal(start_state):
            return node_solution[start_state]

        path = deque()
        path.append(start_state)
        explored = set()
        explored.add(start_state)

        while path:
            current_state = path.pop()
            solution = node_solution[current_state]

            if len(solution) >= max_depth:
                continue

            for action, next_state, cost in game_dls.get_successors(current_state):
                if next_state not in explored:
                    explored.add(next_state)
                    node_solution[next_state] = solution + [action]

                    if next_state not in path:
                        path.append(next_state)

                elif len(node_solution[next_state]) > len(solution) + 1:
                    node_solution[next_state] = solution + [action]

                    if next_state not in path:
                        path.append(next_state)

                if game.is_goal(next_state):
                    return node_solution[next_state]
        return None

    max_depth = 70
    for i in range(max_depth):
        answer = dls_solve(game, i)
        if answer:
            return answer
    return None


def ucs_solve(game):
    start_state = game.get_initial_state()
    node_solution = {start_state: []}

    if game.is_goal(start_state):
        return node_solution[start_state]

    frontier = []
    unique_str = str(start_state.player) + str(start_state.boxes)
    heapq.heappush(frontier, (0, 0, unique_str, start_state))
    explored = set()
    explored.add(start_state)

    while frontier:
        current_cost, current_step, current_unique_str, current_state = heapq.heappop(frontier)

        for action, next_state, next_cost in game.get_successors(current_state):
            solution = node_solution[current_state]
            next_cost += current_cost
            next_step = current_step + 1

            if next_state not in explored:
                explored.add(next_state)
                node_solution[next_state] = solution + [action]

                if game.is_goal(next_state):
                    return node_solution[next_state]

                unique_str = str(next_state.player) + str(next_state.boxes)
                heapq.heappush(frontier, (next_cost, next_step, unique_str, next_state))
    return None


def astar_solve(game):
    def heuristic(state):
        def manhattan(start_pos, end_pos):
            return abs(start_pos[0] - end_pos[0]) + abs(start_pos[1] - end_pos[1])

        def distance_sum(list1, list2):
            sum = 0
            for i in range(min(len(list1), len(list2))):
                sum += manhattan(list1[i], list2[i])
            return sum

        def is_wall(game, direction, box):
            match direction:
                case 'd':
                    return game.is_wall((box[0], box[1] + 1))
                case 'u':
                    return game.is_wall((box[0], box[1] - 1))
                case 'r':
                    return game.is_wall((box[0] + 1, box[1]))
                case 'l':
                    return game.is_wall((box[0] - 1, box[1]))
                case _:
                    return None

        def get_target_pos_from_box(box, target):
            x_distance_box_target = box[0] - target[0]
            y_distance_box_target = box[1] - target[1]
            directions = ''

            if y_distance_box_target > 0:
                directions += 'u'
            if y_distance_box_target < 0:
                directions += 'd'
            if x_distance_box_target > 0:
                directions += 'l'
            if x_distance_box_target < 0:
                directions += 'r'

            return directions

        def box_move_dir_u(g, box):
            move_right_cnt = 0
            move_left_cnt = 0

            x, y = box[0], box[1] + 1
            while g.is_wall((x, y)):
                move_right_cnt += 1
                x += 1

            x, y = box[0], box[1] + 1
            while g.is_wall((x, y)):
                move_left_cnt += 1
                x -= 1

            min_move = min(move_right_cnt, move_left_cnt)
            if min_move == move_right_cnt:
                return 'r', min_move, move_left_cnt
            else:
                return 'l', min_move, move_right_cnt

        def box_move_dir_d(g, box):
            move_right_cnt = 0
            move_left_cnt = 0

            x, y = box[0], box[1] - 1
            while g.is_wall((x, y)):
                move_right_cnt += 1
                x += 1

            x, y = box[0], box[1] - 1
            while g.is_wall((x, y)):
                move_left_cnt += 1
                x -= 1

            min_move = min(move_right_cnt, move_left_cnt)
            if min_move == move_right_cnt:
                return 'r', min_move, move_left_cnt
            else:
                return 'l', min_move, move_right_cnt

        def box_move_dir_l(g, box):
            move_down_cnt = 0
            move_up_cnt = 0

            x, y = box[0] + 1, box[1]
            while g.is_wall((x, y)):
                move_down_cnt += 1
                y += 1

            x, y = box[0] + 1, box[1]
            while g.is_wall((x, y)):
                move_up_cnt += 1
                y -= 1

            min_move = min(move_down_cnt, move_up_cnt)
            if min_move == move_down_cnt:
                return 'd', min_move, move_up_cnt
            else:
                return 'u', min_move, move_down_cnt

        def box_move_dir_r(g, box):
            move_down_cnt = 0
            move_up_cnt = 0

            x, y = box[0] - 1, box[1]
            while g.is_wall((x, y)):
                move_down_cnt += 1
                y += 1

            x, y = box[0] - 1, box[1]
            while g.is_wall((x, y)):
                move_up_cnt += 1
                y -= 1

            min_move = min(move_down_cnt, move_up_cnt)
            if min_move == move_down_cnt:
                return 'd', min_move, move_up_cnt
            else:
                return 'u', min_move, move_down_cnt

        def wall_penalty(game, box, target):
            if box == target:
                return 0

            target_dir = get_target_pos_from_box(box, target)
            min_move = 0

            # box should move up but there are walls below
            if 'u' in target_dir and is_wall(game, 'd', box):
                move_dir, min_move, other_move = box_move_dir_u(game, box)

                if (('l' in target_dir and move_dir == 'r')
                        or ('r' in target_dir and move_dir == 'l')):
                    min_move = min(2 * min_move, other_move)

            # box should move down but there are walls above
            if 'd' in target_dir and is_wall(game, 'u', box):
                move_dir, min_move, other_move = box_move_dir_d(game, box)

                if (('l' in target_dir and move_dir == 'r')
                        or ('r' in target_dir and move_dir == 'l')):
                    min_move = min(2 * min_move, other_move)

            # box should move left but there are walls on the right
            if 'l' in target_dir and is_wall(game, 'r', box):
                move_dir, min_move, other_move = box_move_dir_l(game, box)

                if (('u' in target_dir and move_dir == 'd')
                        or ('d' in target_dir and move_dir == 'u')):
                    min_move = min(2 * min_move, other_move)

            # box should move right but there are walls on the left
            if 'r' in target_dir and is_wall(game, 'l', box):
                move_dir, min_move, other_move = box_move_dir_r(game, box)

                if (('u' in target_dir and move_dir == 'd')
                        or ('d' in target_dir and move_dir == 'u')):
                    min_move = min(2 * min_move, other_move)

            if min_move > 0:
                return min_move * 5 + 6
            else:
                return 0

        # heuristic starts here
        # config
        targets = list(game.get_targets())
        boxes = list(state.boxes)
        player = tuple(state.player)

        # find the closest box to player
        distance_player_box = list()
        for box in boxes:
            distance_player_box.append(manhattan(player, box))
        min_player_dis = min(distance_player_box)

        # find correct target for each box by min distance between them
        box_target_per = {}
        for box_per in permutations(boxes):
            box_target_per[box_per] = distance_sum(box_per, targets)
        correct_box_target_per, min_dis_box_target = min(box_target_per.items(), key=lambda x: x[1])

        # calculate wall penalty for the founded permutation of boxes and targets
        penalty = 0
        for i in range(len(targets)):
            penalty += wall_penalty(game, correct_box_target_per[i], targets[i])

        return (5 * min_dis_box_target) + (min_player_dis - 1) + penalty

    # astar starts here
    start_state = game.get_initial_state()
    node_solution = {start_state: []}

    if game.is_goal(start_state):
        return node_solution[start_state]

    counter = 0
    start_h = heuristic(start_state)

    frontier = []
    heapq.heappush(frontier, (start_h, counter, start_state))
    frontier_set = set()
    frontier_set.add(start_state)

    explored = set()
    explored.add(start_state)

    node_g = {start_state: 0}

    while frontier:
        current_f, current_count, current_state = heapq.heappop(frontier)
        frontier_set.remove(current_state)

        for action, next_state, next_cost in game.get_successors(current_state):
            solution = node_solution[current_state]
            next_g = node_g[current_state] + next_cost
            next_h = heuristic(next_state)
            next_f = next_g + next_h

            if next_state not in explored:
                counter += 1
                explored.add(next_state)
                node_solution[next_state] = solution + [action]
                node_g[next_state] = next_g

                heapq.heappush(frontier, (next_f, counter, next_state))
                frontier_set.add(next_state)
            elif node_g[next_state] > next_g:
                node_solution[next_state] = solution + [action]
                node_g[next_state] = next_g

                if next_state not in frontier_set:
                    counter += 1
                    heapq.heappush(frontier, (next_f, counter, next_state))
                    frontier_set.add(next_state)

            if game.is_goal(next_state):
                return node_solution[next_state]
    return None