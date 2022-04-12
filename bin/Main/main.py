import os
import random
import time
from tkinter import *
import pandas as pd

from bin.Classess.Field import Field
from bin.Classess.Mine import Mine
from bin.Classess.Travel import Travel
from bin.Classess.Player import Player
from bin.Classess.NeuralNetwork import NeuralNetwork
import bin.Classess.Node as nd
import bin.Classess.Travel as tr
from resources.Globals import *
from bin.Classess.DecisionTree import DecisionTree

# Creating objects
player = Player()
field = Field()
travel = Travel()
decision_tree = DecisionTree()
neural_network = NeuralNetwork()

# Globals
fringe = []
explored = []
action_list = []
images_coord = []

label = None


def Arrow(direction):
    image = ""
    if direction == "north":
        image = player.arrow_north_image
    elif direction == "south":
        image = player.arrow_south_image
    elif direction == "west":
        image = player.arrow_west_image
    elif direction == "east":
        image = player.arrow_east_image

    field.small_field_canvas.itemconfig(player.image_canvas_id, image=image)


# Putting images
def Fill(bool):
    global images_coord
    if bool:
        field.PuttingSmallImages()

        travel.points_coord.append(field.small_field_canvas.coords(field.canvas_small_images[0]))
        travel.points_coord.extend(field.mines_coord)

        for i in range(0, len(travel.points_coord)):
            travel.points_map[i + 1] = travel.points_coord[i]

        print(travel.points_map)

        for i in range(0, len(field.canvas_small_images)):
            images_coord.append(field.small_field_canvas.coords(field.canvas_small_images[i]))

        nd.init_data(images_coord, field.cell_expense)

    DrawingLargeImage()


def DrawingLargeImage():
    large_img_name = field.large_image_array[player.current_array_x][player.current_array_y]  # ToDo change positions?

    # print(
    #     f'large image path[{player.current_array_x}][{player.current_array_y}]: {field.large_image_array_filepath[player.current_array_x][player.current_array_y]}')

    field.PuttingLargeImage(large_img_name)


def NextDirection(action):
    # Define next direction
    current_direction = player.direction
    t = -1
    for i in range(4):
        if player.directions[i] == current_direction:
            t = i
            break

    # Write next direction to Player
    if action == "Right":
        player.direction = player.directions[(t + 1) % 4]
    elif action == "Left":
        player.direction = player.directions[(t - 1) % 4]

    return player.direction


def MovingForward():
    if player.direction == "east" and field.small_field_canvas.coords(player.image_canvas_id)[
        0] + player.step < FRAME_WIDTH:
        field.small_field_canvas.move(player.image_canvas_id, player.step, 0)
    elif player.direction == "west" and field.small_field_canvas.coords(player.image_canvas_id)[0] > player.x_start:
        field.small_field_canvas.move(player.image_canvas_id, -player.step, 0)
    elif player.direction == "north" and field.small_field_canvas.coords(player.image_canvas_id)[1] > player.y_start:
        field.small_field_canvas.move(player.image_canvas_id, 0, -player.step)
    elif player.direction == "south" and field.small_field_canvas.coords(player.image_canvas_id)[
        1] + player.step < FRAME_HEIGHT:
        field.small_field_canvas.move(player.image_canvas_id, 0, player.step)


def Moving(action):
    # Moving
    if action == "Right":
        # player.MovingRight()
        field.Moving()
        Fill(False)
        next_direction = NextDirection(action)
        Arrow(next_direction)
    elif action == "Left":
        # player.MovingLeft()
        field.Moving()
        Fill(False)
        next_direction = NextDirection(action)
        Arrow(next_direction)
    elif action == "Up":
        player.Moving()
        field.Moving()
        Fill(False)
        MovingForward()
        Arrow(player.direction)


def ImagesInArray(images_array, array, paths_array, switch):
    # Filling array from directory
    row = column = 0

    for i in range(len(images_array)):
        is_done = False
        while not is_done:
            if array[row][column] == 0:
                array[row][column] = images_array[i]
                if switch:
                    field.large_image_array_filepath[row][column] = paths_array[i]
                is_done = True
            else:
                column += 1
                if column == 10:
                    column = 0
                    row += 1
                if row == 10:
                    break

        column += 1
        if column == 10:
            column = 0
            row += 1
        if row == 10:
            break

    # for el in images_array:
    #     is_done = False
    #     while not is_done:
    #         if array[row][column] == 0:
    #             array[row][column] = el
    #             is_done = True
    #         else:
    #             column += 1
    #             if column == 10:
    #                 column = 0
    #                 row += 1
    #             if row == 10:
    #                 break
    #
    #     column += 1
    #     if column == 10:
    #         column = 0
    #         row += 1
    #     if row == 10:
    #         break


def CellDesignation(array, color):
    for element in array:
        if element[0] == 0:
            element[0] = player.current_x
            element[1] = player.current_y
            element[2] = color
            break


def Action(action):
    if action in ["Right", "Left", "Up", "space"]:
        Moving(action)
    # elif action in ["1", "2"]:
    #     if action == "1":
    #         CellDesignation(field.state_of_cell_array, "red")
    #     else:
    #         CellDesignation(field.state_of_cell_array, "green")


# Modified by Artem to search in the status area
def create_action_list(states, index):
    global fringe
    global action_list

    if index == 0:
        action_list.reverse()
        return True
    action_list.append(fringe[index].action)
    state_parent = [fringe[index].parent[0], fringe[index].parent[1]]
    create_action_list(states, states.index(state_parent))


def MakeDecision():
    if player.current_array_x != 0 or player.current_array_y != 0:
        mine = field.state_of_cell_array[player.current_array_x][player.current_array_y]
        # print(field.state_of_cell_array)
        # print(mine)
        attributes_dict = {'known': [mine.known], 'power': [mine.power], 'new': [mine.new], 'location': [mine.location],
                           'stable': [mine.stable], 'chain_reaction': [mine.chain_reaction]}

        attributes = f'{mine.known}; {mine.power}; {mine.new}; {mine.location}; {mine.stable}; {mine.chain_reaction}'

        global label_text
        label_text += attributes + '\n'

        global label
        label.config(text=label_text)
        field.win.update()

        data_frame = pd.DataFrame.from_dict(attributes_dict)
        predict = decision_tree.classifier.predict(data_frame)

        return predict


def MarkMine(prediction):
    if prediction == 0:
        DrawFlag(field.flag_green_img)
    if prediction == 1:
        DrawFlag(field.flag_yellow_img)
    if prediction == 2:
        DrawFlag(field.flag_red_img)
    if prediction == 3:
        DrawFlag(field.flag_bleu_img)

    field.win.update()


def ChangeChainReactionParameter(prediction, source_x, source_y, x, y):
    if prediction == 0:
        # print(f"x: {source_x}; y: {source_y}")
        # print(f'state of cell: {field.state_of_cell_array[source_x][source_y]}')
        # print(f'img path: {field.large_image_array_filepath}')
        field.state_of_cell_array[source_x][source_y].chain_reaction = 1
        field.state_of_cell_array[x][y] = "House"


def CheckIfItIsHouse(x, y):
    prediction = NeuralNetwork.Prediction(neural_network, x, y, field)

    house = prediction[0][0]
    other = prediction[0][1]

    print(f'prediction: {prediction}')

    if house > other:
        prediction = 0
    else:
        prediction = 1

    print(f'Prediction: {prediction}')

    return prediction


def CheckForHouses():
    if player.current_array_x > 0 and field.state_of_cell_array[player.current_array_x - 1][
        player.current_array_y] == "None":
        prediction = CheckIfItIsHouse(player.current_array_x - 1, player.current_array_y)
        ChangeChainReactionParameter(prediction, player.current_array_x, player.current_array_y,
                                     player.current_array_x - 1, player.current_array_y)
    if player.current_array_x < 9 and field.state_of_cell_array[player.current_array_x + 1][
        player.current_array_y] == "None":
        prediction = CheckIfItIsHouse(player.current_array_x + 1, player.current_array_y)
        ChangeChainReactionParameter(prediction, player.current_array_x, player.current_array_y,
                                     player.current_array_x + 1, player.current_array_y)
    if player.current_array_y > 0 and field.state_of_cell_array[player.current_array_x][
        player.current_array_y - 1] == "None":
        prediction = CheckIfItIsHouse(player.current_array_x, player.current_array_y - 1)
        ChangeChainReactionParameter(prediction, player.current_array_x, player.current_array_y,
                                     player.current_array_x, player.current_array_y - 1)
    if player.current_array_y < 9 and field.state_of_cell_array[player.current_array_x][
        player.current_array_y + 1] == "None":
        prediction = CheckIfItIsHouse(player.current_array_x, player.current_array_y + 1)
        ChangeChainReactionParameter(prediction, player.current_array_x, player.current_array_y,
                                     player.current_array_x, player.current_array_y + 1)


def MouseClickEvent(track):
    global fringe
    global explored
    global action_list

    print("The best individual is: {} {}".format(track[1], track[0]))
    for point in range(0, len(track[1]) + 1):
        start_position = field.small_field_canvas.coords(player.image_canvas_id)
        if point == len(track[1]):
            end_position = travel.points_map[1]
        else:
            end_position = travel.points_map[track[1][point]]

        node = nd.Node()
        if len(fringe) == 0:
            node.state.coord = start_position
            node.state.direction = "east"
        else:
            states = []
            for k in range(0, len(fringe)):
                new_state = fringe[k].state.coord
                states.append(new_state)
            start_node = fringe[-1]

            node.state.coord = start_node.state.coord
            node.state.direction = start_node.state.direction

        fringe.clear()
        explored.clear()
        action_list.clear()
        fringe = nd.graph_search_A(fringe, explored, node.state, end_position)

        states = []
        goal_all = []
        for i in range(0, len(fringe)):
            new_state = [fringe[i].state.coord, fringe[i].state.direction]
            states.append(new_state)
            if end_position[0] == fringe[i].state.coord[0] and end_position[1] == fringe[i].state.coord[1]:
                goal_all.append(fringe[i])

        elem_min = goal_all[0]
        for i in range(1, len(goal_all)):
            if elem_min.priority > goal_all[i].priority:
                elem_min = goal_all[i]
        index = fringe.index(elem_min)
        fringe = fringe[:index + 1]

        create_action_list(states, -1)

        # Start moving
        AutoMove()

        # Condition, that not allow check if in 0, 0
        if player.current_array_x > 0 and player.current_y > 0:
            # Check if there are houses nearby
            print()
            CheckForHouses()

        # Decision by tree
        prediction = MakeDecision()
        # Draw the right flag
        MarkMine(prediction)

        time.sleep(SLEEP_AFTER_CHECK_MINE)


# Check in which locations is mine
def CheckLocation(x, y):
    # Add x + y like strings that create xy number
    temp_x = str(x)
    temp_y = str(y)
    position_str = temp_x + temp_y
    position = int(position_str)

    color_number = -1
    if field.cell_expense[position] == standard_cell_cost:
        color_number = 0
    elif field.cell_expense[position] == sand_cell_cost:
        color_number = 1
    elif field.cell_expense[position] == water_cell_cost:
        color_number = 2
    elif field.cell_expense[position] == swamp_cell_cost:
        color_number = 3

    return color_number


# Add mines on the field and to arrays
def PutMines(mines_array):
    counter = 0

    while counter < AMOUNT_OF_MINES:
        x = random.randint(0, 9)
        y = random.randint(0, 9)

        is_equal = False

        for mine in mines_array:
            if mine.array_x == x and mine.array_y == y:
                is_equal = True
        if not is_equal:
            if x == 0 and y == 0:
                continue
            else:
                known = random.randint(0, 1)
                power = random.randint(1, 10)
                new = random.randint(0, 1)
                location = CheckLocation(x, y)
                stable = random.randint(0, 1)

                mine = Mine(x, y, known, power, new, location, stable)
                mines_array.append(mine)

                # Add mine to array at the right position
                field.state_of_cell_array[x][y] = mine

                field.field_state_array[x][y] = True

                counter += 1


def MinesInArrays(mines_array, directory, imgs_array, bool_mines_coord):
    counter = 0

    temp_array = []

    if directory == "../../files/small_mines_images":
        for file in os.listdir(directory):
            if counter < AMOUNT_OF_MINES:
                image_name = file
                image_path = f"{directory}/{image_name}"
                image = PhotoImage(master=field.small_field_canvas, file=image_path)

                temp_array.append(image)

                counter += 1

        for i in range(AMOUNT_OF_MINES):
            mines_array[i].small_img = temp_array[i]

            # Add images in image array
            imgs_array[mines_array[i].array_x][mines_array[i].array_y] = temp_array[i]

    elif directory == "../../files/large_mines_images":
        for file in os.listdir(directory):
            if counter < AMOUNT_OF_MINES:
                image_name = file
                image_path = f"{directory}/{image_name}"
                image = PhotoImage(master=field.large_image_canvas, file=image_path)

                temp_array.append(image)

                counter += 1

        for i in range(AMOUNT_OF_MINES):
            mines_array[i].large_img = temp_array[i]

            # Add images in image array
            imgs_array[mines_array[i].array_x][mines_array[i].array_y] = temp_array[i]

    if bool_mines_coord:
        for i in range(len(mines_array)):
            field.mines_coord.append([mines_array[i].array_x, mines_array[i].array_y])


def DrawFlag(image):
    field.small_field_canvas.create_image(player.current_x, player.current_y, anchor=NW, image=image)


# def IsItMine():
#     visited = 0     # 0 - not mine; 1 - on this mine for the first time; 2 - already been on this mine
#
#     # Checks if the player is on the mine
#     for i in field.mines_coord:
#         if i[0] == player.current_x and i[1] == player.current_y:
#             visited = 1
#             # Checks if the player has already been on this mine
#             for y in field.visited_mines:
#                 if y[0] == player.current_x and y[1] == player.current_y:
#                     visited = 2
#         if visited == 1:
#             DrawFlag()


def AutoMove():
    for action in action_list:
        # Program wait for better illustration
        time.sleep(DELAY_TIME)
        # Move once
        Action(action)
        # Check if player on mine and if yes, draw flag
        # IsItMine()
        # Update main window
        field.win.update()


# Draws rectangles that indicate type of cells
def DrawRectangle():
    x = 4
    y = 4

    color = None
    # Chose color for rectangle
    for i in range(len(field.cell_expense)):
        if field.cell_expense[i] == standard_cell_cost:
            color = "None"
        elif field.cell_expense[i] == sand_cell_cost:
            color = "yellow"
        elif field.cell_expense[i] == water_cell_cost:
            color = "dodger blue"
        elif field.cell_expense[i] == swamp_cell_cost:
            color = "green4"
        if color != "None":
            field.small_field_canvas.create_rectangle(x, y, x + IMAGE_SIZE + 2, y + IMAGE_SIZE + 2, width=2,
                                                      outline=color)
        x += player.step
        if x + IMAGE_SIZE + 2 > field.width:
            x = 4
            y += player.step


def AddCostCellsToArray(amount, cost):
    counter = 0
    while counter < amount:
        r = random.randint(0, 99)
        if field.cell_expense[r] == 0:
            field.cell_expense[r] = cost
            counter += 1


def CostingOfCells():
    AddCostCellsToArray(amount_of_sand_cells, sand_cell_cost)
    AddCostCellsToArray(amount_of_water_cells, water_cell_cost)
    AddCostCellsToArray(amount_of_swamp_cells, swamp_cell_cost)
    AddCostCellsToArray(
        field.rows * field.columns - (amount_of_sand_cells + amount_of_water_cells + amount_of_swamp_cells),
        standard_cell_cost)

    # Draw rectangles
    DrawRectangle()


def click_button():
    btn.destroy()
    global label
    label = Label(field.win, text="Wait...\nAI conquers the world...", fg='black', font="20", bg='gray')
    label.place(x=10, y=560)
    field.win.update()
    track = tr.genetic_algorithm(travel.points_map)

    track[1].remove(1)
    label.config(text=track[1])
    field.win.update()
    MouseClickEvent(track)


# Check if there mines near and if, mark it
def CheckForMinesAndHousesNear(x, y):
    if x > 0:
        if field.state_of_cell_array[x - 1][y] != "None":
            # Mark by chain reaction current mine
            field.state_of_cell_array[x][y].chain_reaction = 1
            # Mark by chain reaction mine that near
            field.state_of_cell_array[x - 1][y].chain_reaction = 1
    if x < 9:
        if field.state_of_cell_array[x + 1][y] != "None":
            # Mark by chain reaction current mine
            field.state_of_cell_array[x][y].chain_reaction = 1
            # Mark by chain reaction mine that near
            field.state_of_cell_array[x + 1][y].chain_reaction = 1
    if y > 0:
        if field.state_of_cell_array[x][y - 1] != "None":
            # Mark by chain reaction current mine
            field.state_of_cell_array[x][y].chain_reaction = 1
            # Mark by chain reaction mine that near
            field.state_of_cell_array[x][y - 1].chain_reaction = 1
    if y < 9:
        if field.state_of_cell_array[x][y + 1] != "None":
            # Mark by chain reaction current mine
            field.state_of_cell_array[x][y].chain_reaction = 1
            # Mark by chain reaction mine that near
            field.state_of_cell_array[x][y + 1].chain_reaction = 1


def CheckForChainReaction():
    for x in range(field.columns):
        for y in range(field.rows):
            if field.state_of_cell_array[x][y] != "None":
                CheckForMinesAndHousesNear(x, y)


def LoadAndMixImages(directory_small_images, directory_large_images):
    small_images_array = []
    large_images_array = []
    large_image_array_filepath = []

    for filename in os.listdir(directory_small_images):
        image_path = f"{directory_small_images}/{filename}"
        image = PhotoImage(master=field.small_field_canvas, file=image_path)

        small_images_array.append(image)

    for filename in os.listdir(directory_large_images):
        image_path = f"{directory_large_images}/{filename}"
        image = PhotoImage(master=field.large_image_canvas, file=image_path)

        large_images_array.append(image)
        large_image_array_filepath.append(f'{directory_large_images}/{filename}')

    zip_array = list(zip(small_images_array, large_images_array, large_image_array_filepath))

    random.shuffle(zip_array)

    small_images_array, large_images_array, large_image_array_filepath = zip(*zip_array)

    return small_images_array, large_images_array, large_image_array_filepath


def HousesImagesInArray(images_array, array_for_images, array_of_paths, is_large_images):
    i = 0
    while i < AMOUNT_OF_HOUSES:
        x = random.randint(0, 9)
        y = random.randint(0, 9)

        if array_for_images[x][y] == 0:
            array_for_images[x][y] = images_array[i]
            if is_large_images:
                field.large_image_array_filepath[x][y] = array_of_paths[i]
            i += 1


def funct(small_images_of_houses_array, large_images_of_houses_array, large_image_array_filepath):
    i = 0
    while i < AMOUNT_OF_HOUSES:
        x = random.randint(0, 9)
        y = random.randint(0, 9)

        if field.small_image_array[x][y] == 0 and field.large_image_array[x][y] == 0:
            field.small_image_array[x][y] = small_images_of_houses_array[i]
            field.large_image_array[x][y] = large_images_of_houses_array[i]
            field.large_image_array_filepath[x][y] = large_image_array_filepath
            i += 1


def LoadImages(directory):
    array = []
    for filename in os.listdir(directory):
        image_path = f"{directory}/{filename}"
        image = PhotoImage(master=field.large_image_canvas, file=image_path)

        array.append(image)

    return array


def LoadImages_2(directory):
    array = []
    for filename in os.listdir(directory):
        image_path = f"{directory}/{filename}"
        image = PhotoImage(master=field.small_field_canvas, file=image_path)

        array.append(image)

    return array


def LoadPath(directory):
    array = []
    for filename in os.listdir(directory):
        array.append(f'{directory}/{filename}')

    return array


def LoadData(small_directory, large_directory):
    small_array = []
    large_array = []
    path_array = []

    for filename in sorted(os.listdir(small_directory)):
        image_path = f'{small_directory}/{filename}'
        image = PhotoImage(master=field.small_field_canvas, file=image_path)

        small_array.append(image)

    for filename in sorted(os.listdir(large_directory)):
        image_path = f'{large_directory}/{filename}'
        image = PhotoImage(master=field.large_image_canvas, file=image_path)

        large_array.append(image)
        path_array.append(f'{large_directory}/{filename}')

    return small_array, large_array, path_array


def LoadDataInArrays(small_images_directory, large_images_directory):
    small_images_of_houses_array = []
    large_images_of_houses_array = []
    large_image_array_filepath = []

    is_equal_len = False

    small_images_dir = sorted(os.listdir(small_images_directory))
    large_images_dir = sorted(os.listdir(large_images_directory))
    large_image_array_filepath = large_images_dir.copy()

    # print(large_image_array_filepath)

    for i in range(len(large_image_array_filepath)):
        filename = large_image_array_filepath[i]
        path = f'{large_images_directory}/{filename}'
        large_image_array_filepath[i] = path

    # print(large_image_array_filepath)

    if len(small_images_dir) == len(large_images_dir) == len(large_image_array_filepath):
        is_equal_len = True

    if is_equal_len:
        for i in range(len(small_images_dir)):
            is_path_good = False
            small_image_path = f'{small_images_directory}/{small_images_dir[i]}'
            large_image_path = f'{large_images_directory}/{large_images_dir[i]}'

            if large_image_path == large_image_array_filepath[i]:
                is_path_good = True

            # print(f'large_image_path: {large_image_path}\nlarge_image_array_filepath[i]: {large_image_array_filepath[i]:}')

            if not is_path_good:
                print("path is bad\nerror!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

            small_image = PhotoImage(master=field.small_field_canvas, file=small_image_path)
            large_image = PhotoImage(master=field.large_image_canvas, file=large_image_path)

            small_images_of_houses_array.append(small_image)
            large_images_of_houses_array.append(large_image)

    return small_images_of_houses_array, large_images_of_houses_array, large_image_array_filepath


def HousesImagesInArray_2(small_images_of_houses_array, large_images_of_houses_array, large_image_array_filepath):
    i = 0
    while i < AMOUNT_OF_HOUSES:
        x = random.randint(0, 9)
        y = random.randint(0, 9)

        if field.small_image_array[x][y] == 0 and field.large_image_array[x][y] == 0:
            field.small_image_array[x][y] = small_images_of_houses_array[i]
            field.large_image_array[x][y] = large_images_of_houses_array[i]
            field.large_image_array_filepath[x][y] = large_image_array_filepath[i]
            i += 1


def ImagesInArray_2(small_images_array, large_images_array, large_image_array_filepath):
    # Filling array from directory
    x = y = 0

    # if len(small_images_array) != len(large_images_array):
    #     print(f'len(small_images_array) != len(large_images_array)\nerror!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

    for i in range(len(small_images_array)):
        is_done = False
        while not is_done:
            if field.small_image_array[x][y] == 0 and field.large_image_array[x][y] == 0:
                field.small_image_array[x][y] = small_images_array[i]
                field.large_image_array[x][y] = large_images_array[i]
                field.large_image_array_filepath[x][y] = large_image_array_filepath[i]
                is_done = True
            else:
                x += 1
                if x == 10:
                    x = 0
                    y += 1
                if y == 10:
                    break

        x += 1
        if x == 10:
            x = 0
            y += 1
        if y == 10:
            break

    # if len(small_images_array) != len(large_images_array):
    #     print(f'len(small_images_array) != len(large_images_array)\nerror!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    #
    # for i in range(len(small_images_array)):
    #     is_done = False
    #     while not is_done:
    #         if field.small_image_array[x][y] == 0 and field.large_image_array[x][y] == 0:
    #             field.small_image_array[x][y] = small_images_array[i]
    #             field.large_image_array[x][y] = large_images_array[i]
    #             is_done = True
    #         else:
    #             y += 1
    #             if y == 10:
    #                 y = 0
    #                 x += 1
    #             if x == 10:
    #                 break
    #
    #     y += 1
    #     if y == 10:
    #         y = 0
    #         x += 1
    #     if x == 10:
    #         break


def MinesInArrays_2(mines_array, small_mines_images_dir, large_mines_images_dir):
    counter = 0

    small_temp_array = []
    large_temp_array = []

    for file in os.listdir(small_mines_images_dir):
        if counter < AMOUNT_OF_MINES:
            image_name = file
            image_path = f"{small_mines_images_dir}/{image_name}"
            image = PhotoImage(master=field.small_field_canvas, file=image_path)

            small_temp_array.append(image)

            counter += 1

    # print()
    # print()
    # print()
    # print()
    # print()
    # print()
    for z in range(AMOUNT_OF_MINES):
        mines_array[z].small_img = small_temp_array[z]

        # Add images in image array
        field.small_image_array[mines_array[z].array_x][mines_array[z].array_y] = small_temp_array[z]

        # print(f'mines_array[z].array_x][mines_array[z].array_y: {mines_array[z].array_x}, {mines_array[z].array_y}')
        # print(
        #     f'small_image_array[{mines_array[z].array_x}][{mines_array[z].array_y}]: {field.small_image_array[mines_array[z].array_x][mines_array[z].array_y]}')

    for i in range(len(mines_array)):
        field.mines_coord.append([mines_array[i].array_y, mines_array[i].array_x])

    counter = 0
    for file in os.listdir(large_mines_images_dir):
        if counter < AMOUNT_OF_MINES:
            image_name = file
            image_path = f"{large_mines_images_dir}/{image_name}"
            image = PhotoImage(master=field.large_image_canvas, file=image_path)

            large_temp_array.append(image)

            counter += 1

    for i in range(AMOUNT_OF_MINES):
        mines_array[i].large_img = large_temp_array[i]

        # Add images in image array
        field.large_image_array[mines_array[i].array_x][mines_array[i].array_y] = large_temp_array[i]


def main():
    # Creating the main window of an application
    win_size = f'{WINDOW_X}x{WINDOW_Y}'
    field.win.title("Sapper")
    field.win.configure(bg='gray')
    field.win.geometry(win_size)
    print(f'Amount of mines: {AMOUNT_OF_MINES}')
    print(f'Amount of houses: {AMOUNT_OF_HOUSES}')

    global btn
    btn = Button(field.win,
                 text="Search for mines",  # текст кнопки
                 background="#555",  # фоновый цвет кнопки
                 foreground="#ccc",  # цвет текста
                 padx="20",  # отступ от границ до содержимого по горизонтали
                 pady="8",  # отступ от границ до содержимого по вертикали
                 font="24",  # высота шрифта
                 command=click_button
                 )

    btn.place(x=10, y=560)

    # Create array with mines objects
    mines_array = []

    CostingOfCells()

    # Put mines on coordinates
    PutMines(mines_array)

    # # Add images of mines in arrays
    # MinesInArrays(mines_array, "../../files/small_mines_images", field.small_image_array, True)
    # MinesInArrays(mines_array, "../../files/large_mines_images", field.large_image_array, False)

    small_mines_images_dir = "E:/Projects/Pycharm Projects/sapper/files/small_mines_images"
    large_mines_images_dir = "E:/Projects/Pycharm Projects/sapper/files/large_mines_images"
    MinesInArrays_2(mines_array, small_mines_images_dir, large_mines_images_dir)

    # small_images_of_houses_array, large_images_of_houses_array, large_image_array_filepath = LoadAndMixImages(
    #     "../../files/small_images_houses",
    #     "../../files/large_images_houses")

    # small_images_of_houses_array, large_images_of_houses_array, large_image_array_filepath = LoadImages("../../files/small_images_houses", "../../files/large_images_houses")

    # small_images_of_houses_array = LoadImages("../../files/small_images_houses")
    # large_images_of_houses_array = LoadImages_2("../../files/large_images_houses")
    # large_image_array_filepath = LoadPath("../../files/large_images_houses")

    # small_images_of_houses_array, large_images_of_houses_array, large_image_array_filepath = LoadData("../../files/small_images_houses", "../../files/large_images_houses")

    small_images_of_houses_array, large_images_of_houses_array, large_image_array_filepath = LoadDataInArrays(
        "E:/Projects/Pycharm Projects/sapper/files/small_images_houses",
        "E:/Projects/Pycharm Projects/sapper/files/large_images_houses")

    # HousesImagesInArray(small_images_of_houses_array, field.small_image_array, [], False)
    # HousesImagesInArray(large_images_of_houses_array, field.large_image_array, large_image_array_filepath, True)

    HousesImagesInArray_2(small_images_of_houses_array, large_images_of_houses_array, large_image_array_filepath)

    # funct(small_images_of_houses_array, large_images_of_houses_array, large_image_array_filepath)

    # First check only for mines
    CheckForChainReaction()

    small_directory = "E:/Projects/Pycharm Projects/sapper/files/small_images"
    large_directory = "E:/Projects/Pycharm Projects/sapper/files/large_images"
    # small_images_array, large_images_array, large_image_array_filepath = LoadAndMixImages(small_directory,
    #                                                                                       large_directory)

    # small_images_array = LoadImages("../../files/small_images_houses")
    # large_images_array = LoadImages_2("../../files/large_images_houses")
    # large_image_array_filepath = LoadPath("../../files/large_images_houses")

    # small_images_array, large_images_array, large_image_array_filepath = LoadData(small_directory, large_directory)

    small_images_array, large_images_array, large_image_array_filepath = LoadDataInArrays(small_directory,
                                                                                          large_directory)

    # # Filling image arrays
    # ImagesInArray(small_images_array, field.small_image_array, [], False)
    # ImagesInArray(large_images_array, field.large_image_array, large_image_array_filepath, True)

    ImagesInArray_2(small_images_array, large_images_array, large_image_array_filepath)

    # Add arrow image to Player class
    images = []
    for file in os.listdir("../../files/arrow"):
        path = f"../../files/arrow/{file}"
        img = PhotoImage(master=field.small_field_canvas, file=path)
        images.append(img)

    player.arrow_east_image = images[0]
    player.arrow_north_image = images[1]
    player.arrow_south_image = images[2]
    player.arrow_west_image = images[3]

    # Filling window with images
    Fill(True)
    # Drawing arrow (player)
    image = player.arrow_east_image
    player.image_canvas_id = field.small_field_canvas.create_image(player.current_x, player.current_y, anchor=NW,
                                                                   image=image)

    # print("state of cell array:")
    # for el in field.state_of_cell_array:
    #     print(el)

    # for i in range(10):
    #     print(field.large_image_array_filepath[i])

    # Arrow(player.direction)
    # Rectangle(True, "None")
    # Rectangle()
    # Binding keyboard press to function
    # field.win.bind("<Key>", Action)
    # field.small_field_canvas.bind("<Button-1>", MouseClickEvent)

    # Starting mainloop for window
    field.win.mainloop()


if __name__ == '__main__':
    main()
