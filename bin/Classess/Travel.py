import queue
from itertools import permutations, islice
from math import sqrt
import random

from resources.Globals import NUMBER_OF_INDIVIDUALS_FOR_DUEL, NUMBER_OF_POINTS_PERMUTATION, PERCENT_OF_MUTATION, \
    PERCENT_OF_OUTGOING_INDIVIDUALS


class Travel:
    def __init__(self):
        self.points_coord = []
        self.points_map = {}


def genetic_algorithm(travel_map):
    population = []
    road_map = list(travel_map.keys())
    points_permutation = list(map(list, islice(permutations(road_map), NUMBER_OF_POINTS_PERMUTATION)))
    # Generate the first population
    for i in range(0, len(points_permutation)):
        road = points_permutation[i]
        priority = adaptation_function(points_permutation[i], travel_map)

        population.append((priority, road))

    while len(population) < 10000:
        parent1, parent2 = tournament_selection(population)

        child = edge_recombination_crossover(parent1[1], parent2[1])
        child_priority = adaptation_function(child, travel_map)

        population.append((child_priority, child))

        mutation_function(population, travel_map)
        population.sort(key=lambda x: x[0], reverse=True)

    return population[0]


def adaptation_function(list_points, travel_map):
    index_of_point = 0
    distance = 0
    while True:

        if index_of_point < (-len(list_points)):
            return round((1 / distance) * 1000000)

        if index_of_point == (len(list_points) - 1):
            x1 = travel_map.get(list_points[index_of_point])[0]
            y1 = travel_map.get(list_points[index_of_point])[1]

            x2 = travel_map.get(list_points[-len(list_points)])[0]
            y2 = travel_map.get(list_points[-len(list_points)])[1]

            index_of_point = -len(list_points) - 1
        else:
            x1 = travel_map.get(list_points[index_of_point])[0]
            y1 = travel_map.get(list_points[index_of_point])[1]

            x2 = travel_map.get(list_points[index_of_point + 1])[0]
            y2 = travel_map.get(list_points[index_of_point + 1])[1]

            index_of_point += 1

        distance += sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def tournament_selection(population):
    individuals_for_duel1 = []
    individuals_for_duel2 = []
    population_length = len(population)

    while True:

        if len(individuals_for_duel1) == NUMBER_OF_INDIVIDUALS_FOR_DUEL and len(individuals_for_duel2) == NUMBER_OF_INDIVIDUALS_FOR_DUEL:
            break

        if len(individuals_for_duel1) != NUMBER_OF_INDIVIDUALS_FOR_DUEL:
            index1 = random.randint(0, population_length - 1)
            candidate_for_duel1 = population[index1]
            if candidate_for_duel1 not in individuals_for_duel1:
                individuals_for_duel1.append(candidate_for_duel1)

        if len(individuals_for_duel2) != NUMBER_OF_INDIVIDUALS_FOR_DUEL:
            index2 = random.randint(0, population_length - 1)
            candidate_for_duel2 = population[index2]
            if candidate_for_duel2 not in individuals_for_duel1 and candidate_for_duel2 not in individuals_for_duel2:
                individuals_for_duel2.append(candidate_for_duel2)

    winner_of_duel1 = max(individuals_for_duel1, key=lambda x: x[0])
    winner_of_duel2 = max(individuals_for_duel2, key=lambda x: x[0])

    return winner_of_duel1, winner_of_duel2


def edge_recombination_crossover(parent1, parent2):
    dict_of_neighbors = generate_dict_of_neighbors(parent1, parent2)

    gen_index = random.randint(0, len(parent1) - 1)
    gen = parent1[gen_index]
    child = []
    while True:

        child.append(gen)

        if len(child) == len(parent1):
            return child

        for key in dict_of_neighbors.keys():
            if gen in dict_of_neighbors[key]:
                dict_of_neighbors[key].remove(gen)

        if not dict_of_neighbors[gen]:
            while True:
                # new_gen = random.randint(parent1[0], parent1[-1])
                new_gen_index = random.randint(0, len(parent1) - 1)
                new_gen = parent1[new_gen_index]
                if new_gen not in child:
                    break
        else:
            new_gen = dict_of_neighbors[gen][0]
            best_neighbor = len(dict_of_neighbors[new_gen])
            for neighbor in dict_of_neighbors[gen][1:]:
                possible_best_neighbor = len(dict_of_neighbors[neighbor])
                if possible_best_neighbor <= best_neighbor:
                    best_neighbor = possible_best_neighbor
                    new_gen = neighbor
        gen = new_gen


def generate_dict_of_neighbors(parent1, parent2):
    dict_of_neighbors = {}
    for i in range(0, len(parent1)):
        list_of_neighbors = []
        element = parent1[i]
        if i == 0:
            left_neighbor1 = parent1[-1]
            right_neighbor1 = parent1[i + 1]
        elif i == (len(parent1) - 1):
            left_neighbor1 = parent1[i - 1]
            right_neighbor1 = parent1[0]
        else:
            left_neighbor1 = parent1[i - 1]
            right_neighbor1 = parent1[i + 1]

        list_of_neighbors.extend([left_neighbor1, right_neighbor1])

        index = parent2.index(element)
        if index == 0:
            left_neighbor2 = parent2[-1]
            right_neighbor2 = parent2[index + 1]
        elif index == (len(parent2) - 1):
            left_neighbor2 = parent2[index - 1]
            right_neighbor2 = parent2[0]
        else:
            left_neighbor2 = parent2[index - 1]
            right_neighbor2 = parent2[index + 1]

        if left_neighbor2 not in list_of_neighbors:
            list_of_neighbors.append(left_neighbor2)
        if right_neighbor2 not in list_of_neighbors:
            list_of_neighbors.append(right_neighbor2)

        dict_of_neighbors[element] = list_of_neighbors

    return dict_of_neighbors


def mutation_function(population, travel_map):
    mutation_percentage = random.random()
    if mutation_percentage <= PERCENT_OF_MUTATION:
        count_individual_for_mutation = round(len(population) * mutation_percentage)
        mutants = set()
        for i in range(0, count_individual_for_mutation):
            while True:
                individual_for_mutation = random.randint(0, len(population) - 1)
                if individual_for_mutation not in mutants:
                    mutants.add(individual_for_mutation)
                    candidate_mutant = population[individual_for_mutation]
                    while True:
                        chromosome1 = random.randint(0, len(candidate_mutant[1]) - 1)
                        chromosome2 = random.randint(0, len(candidate_mutant[1]) - 1)
                        if chromosome1 != chromosome2:
                            candidate_mutant[1][chromosome1], candidate_mutant[1][chromosome2] = candidate_mutant[1][chromosome2], candidate_mutant[1][chromosome1]

                        candidate_mutant_priority = adaptation_function(candidate_mutant[1], travel_map)
                        mutant = (candidate_mutant_priority, candidate_mutant[1])

                        if mutant not in population:
                            population[individual_for_mutation] = mutant

                        break
                    break










