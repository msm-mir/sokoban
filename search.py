import heapq
from collections import deque

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

            if (next_state not in explored) and (next_state not in frontier):
                explored.add(next_state)
                node_solution[next_state] = solution + [action]

                if game.is_goal(next_state):
                    return node_solution[next_state]

                frontier.append(next_state)
    return None


def ids_solve(game):
    def dls_solve(game, max_depth):
        start_state = game.get_initial_state()

    # Implement the algorithm here
    # this function should return actions


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
    def heuristic():
        pass

    start_state = game.get_initial_state()

    # Your code goes here
    # this function should return actions