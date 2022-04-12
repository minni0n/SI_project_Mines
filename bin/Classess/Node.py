from resources.Globals import *

images_coord_list = []
cell_expense_list = []


class Node:
    def __init__(self):
        self.state = State()
        self.parent = []
        self.action = ""
        self.priority = 0


class State:
    def __init__(self):
        self.coord = []
        self.direction = ""


def init_data(coord_list, expense_list):
    global images_coord_list
    global cell_expense_list

    images_coord_list = coord_list
    cell_expense_list = expense_list


def successor(state):

    node_state_left = Node()
    node_state_right = Node()
    node_state_forward = Node()

    if state.direction == "east":

        node_state_left.state = State()
        node_state_left.state.coord = state.coord
        node_state_left.state.direction = "north"
        node_state_left.action = "Left"

        node_state_right.state = State()
        node_state_right.state.coord = state.coord
        node_state_right.state.direction = "south"
        node_state_right.action = "Right"

        if state.coord[0] + STEP < FRAME_WIDTH:
            node_state_forward.state = State()
            node_state_forward.state.coord = [state.coord[0] + STEP, state.coord[1]]
            node_state_forward.state.direction = state.direction
            node_state_forward.action = "Up"

    elif state.direction == "west":

        node_state_left.state = State()
        node_state_left.state.coord = state.coord
        node_state_left.state.direction = "south"
        node_state_left.action = "Left"

        node_state_right.state = State()
        node_state_right.state.coord = state.coord
        node_state_right.state.direction = "north"
        node_state_right.action = "Right"

        if state.coord[0] > x_start:
            node_state_forward.state = State()
            node_state_forward.state.coord = [state.coord[0] - STEP, state.coord[1]]
            node_state_forward.state.direction = state.direction
            node_state_forward.action = "Up"

    elif state.direction == "north":

        node_state_left.state = State()
        node_state_left.state.coord = state.coord
        node_state_left.state.direction = "west"
        node_state_left.action = "Left"

        node_state_right.state = State()
        node_state_right.state.coord = state.coord
        node_state_right.state.direction = "east"
        node_state_right.action = "Right"

        if state.coord[1] > x_start:
            node_state_forward.state = State()
            node_state_forward.state.coord = [state.coord[0], state.coord[1] - STEP]
            node_state_forward.state.direction = state.direction
            node_state_forward.action = "Up"

    elif state.direction == "south":

        node_state_left.state = State()
        node_state_left.state.coord = state.coord
        node_state_left.state.direction = "east"
        node_state_left.action = "Left"

        node_state_right.state = State()
        node_state_right.state.coord = state.coord
        node_state_right.state.direction = "west"
        node_state_right.action = "Right"

        if state.coord[1] + STEP < FRAME_HEIGHT:
            node_state_forward.state = State()
            node_state_forward.state.coord = [state.coord[0], state.coord[1] + STEP]
            node_state_forward.state.direction = state.direction
            node_state_forward.action = "Up"

    if len(node_state_forward.state.coord) != 0:
        return [node_state_left, node_state_right, node_state_forward]
    else:
        return [node_state_left, node_state_right]


def get_cell_expense(node):
    global images_coord_list
    global cell_expense_list

    for i in range(0, len(images_coord_list)):
        if (images_coord_list[i][0] <= node.state.coord[0] and node.state.coord[0] <= images_coord_list[i][0] + IMAGE_SIZE) and (images_coord_list[i][1] <= node.state.coord[1] and node.state.coord[1] <= images_coord_list[i][1] + IMAGE_SIZE):
            return cell_expense_list[i]


def heurystyka(node_now):

    if node_now.action == "Left" or node_now.action == "Right":
        return node_now.parent[2] + (get_cell_expense(node_now) / 2)
    elif node_now.action == "Up":
        return node_now.parent[2] + (get_cell_expense(node_now) * 2)
    elif node_now.action == "":
        return get_cell_expense(node_now)


# def graph_search(fringe, explored, start_state, end_state_coord):
#
#     node = Node()
#     node.state = start_state
#     node.parent = node.state
#     fringe.append(node)
#     iterator = 0
#
#     end_loop = True
#     while end_loop:
#         if len(fringe) == 0:
#             end_loop = False
#             #return False
#
#         elem = fringe[iterator]
#
#         if elem.state.coord == end_state_coord:
#             return fringe
#
#         explored.append(elem)
#
#         another_states = successor(elem.state)
#         for i in range(0, len(another_states)):
#             n = len(fringe)
#             for j in range(0, n):
#                 if another_states[i].state.coord[0] == fringe[j].state.coord[0] and another_states[i].state.coord[1] == fringe[j].state.coord[1]:
#                     if another_states[i].state.direction == fringe[j].state.direction:
#                         break
#                     else:
#                         states = []
#                         for k in range(0, len(fringe)):
#                             new_state = [fringe[k].state.coord, fringe[k].state.direction]
#                             states.append(new_state)
#                         now_state = [another_states[i].state.coord, another_states[i].state.direction]
#                         if now_state in states:
#                             break
#
#                         another_states[i].parent = elem.state
#                         fringe.append(another_states[i])
#                 else:
#                     states = []
#                     for k in range(0, len(fringe)):
#                         new_state = [fringe[k].state.coord, fringe[k].state.direction]
#                         states.append(new_state)
#                     now_state = [another_states[i].state.coord, another_states[i].state.direction]
#
#                     if now_state in states:
#                         break
#
#                     if another_states[i].state.direction == fringe[j].state.direction:
#                         another_states[i].parent = elem.state
#                         fringe.append(another_states[i])
#         iterator += 1


def graph_search_A(fringe, explored, start_state, end_state_coord):
    node = Node()
    node.state = start_state
    node.priority = heurystyka(node)
    node.parent = [node.state.coord, node.state.direction, node.priority]

    fringe.append(node)
    iterator = 0

    end_loop = True
    while end_loop:
        if len(fringe) == 0:
            end_loop = False
            # return False

        elem = fringe[iterator]

        if elem.state.coord == end_state_coord:
            return fringe

        explored.append(elem)

        another_states = successor(elem.state)
        for i in range(0, len(another_states)):
            another_states[i].parent = [elem.state.coord, elem.state.direction, elem.priority]
            p = heurystyka(another_states[i])

            n = len(fringe)
            for j in range(0, n):
                if another_states[i].state.coord[0] == fringe[j].state.coord[0] and another_states[i].state.coord[1] == fringe[j].state.coord[1]:
                    if another_states[i].state.direction == fringe[j].state.direction and p < fringe[j].priority:
                        another_states[i].priority = p
                        fringe[j] = another_states[i]
                        break
                    else:
                        states = []
                        for k in range(0, len(fringe)):
                            new_state = [fringe[k].state.coord, fringe[k].state.direction]
                            states.append(new_state)
                        now_state = [another_states[i].state.coord, another_states[i].state.direction]
                        if now_state in states:
                            index = states.index(now_state)
                            if p < fringe[index].priority:
                                another_states[i].priority = p
                                fringe[index] = another_states[i]
                                break
                            else:
                                break

                        another_states[i].priority = p
                        fringe.append(another_states[i])

                        n1 = len(fringe)

                        while n1 > 1:
                            change = False
                            for l in range(0, n1 - 1):
                                if fringe[l].priority > fringe[l + 1].priority:
                                    fringe[l], fringe[l + 1] = fringe[l + 1], fringe[l]
                                    change = True

                            n1 -= 1

                            if not change:
                                break
                else:
                    states = []
                    for k in range(0, len(fringe)):
                        new_state = [fringe[k].state.coord, fringe[k].state.direction]
                        states.append(new_state)
                    now_state = [another_states[i].state.coord, another_states[i].state.direction]

                    if now_state in states:
                        index = states.index(now_state)
                        if p < fringe[index].priority:
                            another_states[i].priority = p
                            fringe[index] = another_states[i]
                            break
                        else:
                            break

                    if another_states[i].state.direction == fringe[j].state.direction:
                        another_states[i].priority = p
                        fringe.append(another_states[i])

                        n2 = len(fringe)

                        while n2 > 1:
                            change = False
                            for h in range(0, n2 - 1):
                                if fringe[h].priority > fringe[h + 1].priority:
                                    fringe[h], fringe[h + 1] = fringe[h + 1], fringe[h]
                                    change = True

                            n2 -= 1

                            if not change:
                                break
        iterator += 1
