import random
from turtledemo.penrose import inflatedart

from Algorithms import Algorithms
from Parser import Parser

"-------------------------TASK4-----------------------------------"
coordinates_berlin_11 = Parser.read_tsp_file("/Users/rusleak/Downloads/berlin11_modified.tsp")
coordinates_berlin_52 = Parser.read_tsp_file("/Users/rusleak/Downloads/berlin52.tsp")

current_file = coordinates_berlin_11
random_route = Algorithms.generate_random_route(current_file)

"------------------------TASK5------------------------------------"
fitness = Algorithms.calculate_fitness(random_route)


print("------------------------TASK7------------------------------------")
greedy_result = Algorithms.greedy_algorithm(random_route, random_route[0])
Algorithms.info(greedy_result)


print("------------------------TASK8------------------------------------")
best_city, best_fit = Algorithms.best_greedy_starting_city(current_file)
print("Best starting city by greedy algorithm :", best_city, "fitness:", best_fit)


print("------------------------TASK9------------------------------------")
best_route_fitness, dict_of_routes_fitness = Algorithms.random_routes_analysis(current_file, 100)

print("------------------------TASK10------------------------------------")
best_city, best_fit = Algorithms.best_greedy_starting_city(current_file)
print("Best starting city by greedy algorithm  BERLIN52:", best_city, "fitness:", best_fit)

best_route_fitness, dict_of_routes_fitness = Algorithms.random_routes_analysis(current_file, 100)
Algorithms.info(best_route_fitness)

print("------------------------TASK12------------------------------------")
population_task12 = Algorithms.population_task12(current_file,100,11)
Algorithms.info(population_task12)

print("------------------------TASK13------------------------------------")
Algorithms.info_task13(population_task12)

print("------------------------TASK14------------------------------------")
tournament_route1, tournament_fitness1 = Algorithms.tournament_task14(Algorithms.convert_dict_to_list(population_task12), 5)
#Converting to list because info function accept list or dict

print("Parent 1")
Algorithms.info({tournament_route1: tournament_fitness1})

tournament_route2, tournament_fitness2 = Algorithms.tournament_task14(Algorithms.convert_dict_to_list(population_task12), 5)

while tournament_route1 == tournament_route2:
    tournament_route2, tournament_fitness2 = Algorithms.tournament_task14(
        Algorithms.convert_dict_to_list(population_task12), 5
    )
print("Parent 2")
Algorithms.info({tournament_route2: tournament_fitness2})

print("------------------------TASK15------------------------------------")
crossover_route = Algorithms.PMX_alg(tournament_route1,tournament_route2)
Algorithms.info({tuple(crossover_route): Algorithms.calculate_fitness(crossover_route)})

print("------------------------TASK16------------------------------------")
Algorithms.swap_mutation(crossover_route, 0.2)

print("------------------------TASK17------------------------------------")

population_list = Algorithms.convert_dict_to_list(population_task12)
print([len(r) for r in population_list])
population_list = [list(r) for r in Algorithms.convert_dict_to_list(population_task12)]
epoch1, best_results = Algorithms.epoch(population_list, 50000)
print("Best 3 results")
Algorithms.info(best_results[0])
Algorithms.info(best_results[1])
Algorithms.info(best_results[2])

print(len(epoch1))
print("------------TASK18-------------")
list_of_dict_best_solutions = [best_results]

for x in range (0, 5):
    epoch1, best_results = Algorithms.epoch(population_list, 1)
    list_of_dict_best_solutions.append(best_results)
print("-------------Best results from loop----------------")
#Information of best_results
for item in list_of_dict_best_solutions:
    if isinstance(item, list):               # это best_three_solutions
        for route_dict in item:              # в нём 3 словаря
            Algorithms.info(route_dict)
    else:
        Algorithms.info(item)

import matplotlib.pyplot as plt

best_fitnesses = []
for top3 in list_of_dict_best_solutions:
    if isinstance(top3, list):
        min_fit = min([list(d.values())[0] for d in top3])
        best_fitnesses.append(min_fit)
    else:
        best_fitnesses.append(list(top3.values())[0])

plt.plot(best_fitnesses, marker='o')
plt.title("Graph")
plt.xlabel("Attempt / Epoch")
plt.ylabel("Best fitness")
plt.grid()


for i, fitness in enumerate(best_fitnesses):
    plt.text(i, fitness, f"{fitness:.1f}", ha='center', va='bottom', fontsize=8)

plt.show()