import random
from turtledemo.penrose import inflatedart

from Algorithms import Algorithms
from Parser import Parser

"-------------------------TASK4-----------------------------------"
coordinates_berlin_11 = Parser.read_tsp_file("/Users/rusleak/Downloads/berlin11_modified.tsp")
coordinates_berlin_52 = Parser.read_tsp_file("/Users/rusleak/Downloads/berlin52.tsp")
coordinates_berlin_100 = Parser.read_tsp_file("/Users/rusleak/Downloads/kroA150.tsp")

current_file = coordinates_berlin_52
random_route = Algorithms.generate_random_route(current_file)

"------------------------TASK5------------------------------------"
fitness = Algorithms.calculate_fitness(random_route)


print("------------------------TASK7------------------------------------")
greedy_result = Algorithms.greedy_algorithm(random_route, random_route[0])
Algorithms.info(greedy_result)


print("------------------------TASK 8 9 10------------------------------------")
best_city, best_fit = Algorithms.best_greedy_starting_city(current_file)
print("Best starting city by greedy algorithm :", best_city, "fitness:", best_fit)
#It has print inside method
best_route_fitness, dict_of_routes_fitness = Algorithms.random_routes_analysis(current_file, 100)


print("------------------------TASK12------------------------------------")
population_task12 = Algorithms.population_task12(current_file,100,5)
# Algorithms.info(population_task12)

print("------------------------TASK13------------------------------------")
Algorithms.info_task13(population_task12)
#
print("------------------------TASK14------------------------------------")
tournament_route1, tournament_fitness1 = Algorithms.tournament_task14(Algorithms.convert_dict_to_list(population_task12), 15)
#Converting to list because info function accept list or dict

print("Parent 1")
Algorithms.info({tournament_route1: tournament_fitness1})

tournament_route2, tournament_fitness2 = Algorithms.tournament_task14(Algorithms.convert_dict_to_list(population_task12), 15)

while tournament_route1 == tournament_route2:
    tournament_route2, tournament_fitness2 = Algorithms.tournament_task14(
        Algorithms.convert_dict_to_list(population_task12), 15
    )
print("Parent 2")
Algorithms.info({tournament_route2: tournament_fitness2})

print("------------------------TASK15------------------------------------")
crossover_route = Algorithms.PMX_alg(tournament_route1,tournament_route2)
Algorithms.info({tuple(crossover_route): Algorithms.calculate_fitness(crossover_route)})

print("------------------------TASK16------------------------------------")
# Мы заменили swap_mutation на inversion_mutation в классе, поэтому вызываем новый метод
# Для демонстрации ставим шанс 1.0 (всегда), чтобы увидеть результат
mutated_route = Algorithms.inversion_mutation(crossover_route, 0.2)
print("Mutated route (Inversion):")
Algorithms.info({tuple(mutated_route): Algorithms.calculate_fitness(mutated_route)})

print("------------------------TASK17------------------------------------")

# Converting dict to list
population_list = [list(r) for r in Algorithms.convert_dict_to_list(population_task12)]
current_population_dicts, best_results_of_epoch = Algorithms.epoch(population_list, 100)

print("Best 3 results of Epoch 1:")
Algorithms.info(best_results_of_epoch[0])
Algorithms.info(best_results_of_epoch[1])
Algorithms.info(best_results_of_epoch[2])

print("------------TASK18-------------")
list_of_dict_best_solutions = [best_results_of_epoch]
generations = 100
mutation_rate = 0.2

stagnation_counter = 0
last_best_fitness = list(best_results_of_epoch[0].values())[0]

for i in range(generations):
    # 1. Извлекаем маршруты и СРАЗУ конвертируем их в списки (list)
    next_gen_routes = [list(list(d.keys())[0]) for d in current_population_dicts]

    # --- ДИНАМИЧЕСКАЯ МУТАЦИЯ (Kick) ---
    if stagnation_counter > 5:
        print(f"!!! STAGNATION DETECTED at gen {i}. KICKING POPULATION !!!")
        # Берем маршруты с 5-го по 25-й и применяем сильную мутацию
        for k in range(5, 25):
            # Теперь next_gen_routes[k] это точно список, ошибки не будет
            next_gen_routes[k] = Algorithms.inversion_mutation(next_gen_routes[k], mutation_rate=0.8)
        stagnation_counter = 0

    # 2. Запускаем новую эпоху
    current_population_dicts, best_results_of_epoch = Algorithms.epoch(next_gen_routes, 100)
    list_of_dict_best_solutions.append(best_results_of_epoch)

    current_best_fitness = list(best_results_of_epoch[0].values())[0]

    # Проверка на застревание
    if abs(current_best_fitness - last_best_fitness) < 0.001:
        stagnation_counter += 1
    else:
        stagnation_counter = 0
        last_best_fitness = current_best_fitness

    if i % 10 == 0:
        print(f"Generation {i}: Best Fitness = {current_best_fitness:.2f}")

print("-------------Final Best Result----------------")
#Last list of dict and first dict in this list
Algorithms.info(list_of_dict_best_solutions[-1][0])

# ---------------- GRAPH ----------------
import matplotlib.pyplot as plt

best_fitnesses = []
for top3 in list_of_dict_best_solutions:
    # top3 - это список из 3-х словарей. Берем первый (самый лучший, т.к. они отсортированы)
    best_fit = list(top3[0].values())[0]
    best_fitnesses.append(best_fit)

plt.figure(figsize=(10, 6))
plt.plot(best_fitnesses, marker='o', markersize=3)
plt.title(f"Genetic Algorithm Progress ({len(best_fitnesses)} epochs)")
plt.xlabel("Epoch")
plt.ylabel("Best Fitness (Distance)")
plt.grid(True)

# Подписываем только начало и конец, чтобы не засорять график
plt.text(0, best_fitnesses[0], f"{best_fitnesses[0]:.1f}", ha='right', va='bottom', color='red')
plt.text(len(best_fitnesses) - 1, best_fitnesses[-1], f"{best_fitnesses[-1]:.1f}", ha='left', va='top', color='green')

plt.show()