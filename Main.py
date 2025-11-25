import random
from turtledemo.penrose import inflatedart

from Algorithms import Algorithms
from Parser import Parser

"-------------------------TASK4-----------------------------------"
coordinates_berlin_11 = Parser.read_tsp_file("/Users/rusleak/Downloads/berlin11_modified.tsp")
coordinates_berlin_52 = Parser.read_tsp_file("/Users/rusleak/Downloads/berlin52.tsp")

random_route = Algorithms.generate_random_route(coordinates_berlin_11)

"------------------------TASK5------------------------------------"
fitness = Algorithms.calculate_fitness(random_route)


print("------------------------TASK7------------------------------------")
greedy_result = Algorithms.greedy_algorithm(random_route, random_route[0])
Algorithms.info(greedy_result)


print("------------------------TASK8------------------------------------")
best_city, best_fit = Algorithms.best_greedy_starting_city(coordinates_berlin_11)
print("Best starting city by greedy algorithm BERLIN11:", best_city, "fitness:", best_fit)


print("------------------------TASK9------------------------------------")
best_route_fitness, dict_of_routes_fitness = Algorithms.random_routes_analysis(coordinates_berlin_11, 100)

print("------------------------TASK10------------------------------------")
best_city, best_fit = Algorithms.best_greedy_starting_city(coordinates_berlin_52)
print("Best starting city by greedy algorithm  BERLIN52:", best_city, "fitness:", best_fit)

best_route_fitness, dict_of_routes_fitness = Algorithms.random_routes_analysis(coordinates_berlin_52, 100)
Algorithms.info(best_route_fitness)

print("------------------------TASK11------------------------------------")
