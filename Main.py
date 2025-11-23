import random

from Coordinates import Coordinates
from Parser import Parser
"-------------------------TASK4-----------------------------------"
coordinates_berlin_11 = Parser.read_tsp_file("/Users/rusleak/Downloads/berlin11_modified.tsp")
coordinates_berlin_52 = Parser.read_tsp_file("/Users/rusleak/Downloads/berlin52.tsp")

def generate_random_route(cities):
    solution = cities.copy()
    random.shuffle(solution)
    return solution

random_route = generate_random_route(coordinates_berlin_11)
"------------------------TASK5------------------------------------"

def calculate_fitness(solution):
    total_distance = 0.0
    for i in range(len(solution) - 1):
        total_distance += solution[i].distance_to(solution[i + 1])
    # + from last city to origin
    total_distance += solution[-1].distance_to(solution[0])
    return total_distance

fitness = calculate_fitness(random_route)


"------------------------TASK6------------------------------------"

def info(routes_dict):
    for path, fitness in routes_dict.items():
        for city in path:
            print(f"{city.number} -> ", end="")
        print(path[0].number)
        print(f"Fitness: {fitness:.2f}")
        print("-" * 30)


"------------------------TASK7------------------------------------"
#Starting city is object of Coordinates, not an index
def greedy_algorithm(routes, starting_city):
    internal_routes = routes.copy()
    internal_routes.remove(starting_city)

    path = [starting_city]
    current_city = starting_city

    while internal_routes:
        min_city = None
        min_dist = float('inf')

        for route in internal_routes:
            dist = current_city.distance_to(route)
            if dist < min_dist:
                min_dist = dist
                min_city = route

        path.append(min_city)
        current_city = min_city
        internal_routes.remove(current_city)

    fitness = calculate_fitness(path)

    result = {tuple(path): fitness}

    # info(path)

    return result

greedy_algorithm(coordinates_berlin_11, coordinates_berlin_11[0])



"------------------------TASK8------------------------------------"

print("TASK 8")

best_starting_city_greedy = None
best_fitness_greedy = float('inf')

for city in coordinates_berlin_11:
    result = greedy_algorithm(coordinates_berlin_11, city)
    # result = {tuple(path): fitness}
    path, fitness = list(result.items())[0]  # [(tuple, float)] → (tuple, float)

    info(result)
    if fitness < best_fitness_greedy:
        best_fitness = fitness
        best_starting_city = path[0]
print("Best starting city by greedy algorithm : " + str(best_starting_city_greedy) + " fitness : " + str(best_fitness_greedy))
"------------------------TASK9------------------------------------"
print("TASK 9")


best_starting_city_hundred = None
best_starting_fitness_hundred = float('inf')
routes_map = {}

for i in range(101):
    current_route = generate_random_route(coordinates_berlin_11)
    current_fitness = calculate_fitness(current_route)
    routes_map[tuple(current_route)] = current_fitness

    if current_fitness < best_starting_fitness_hundred:
        best_starting_fitness_hundred = current_fitness
        best_starting_city_hundred = current_route[0]
print("ROUTES MAP")
info(routes_map)
print(f"Best starting city by 100 mixes: {best_starting_city_hundred.number}")
print(f"Fitness: {best_starting_fitness_hundred:.2f}")
