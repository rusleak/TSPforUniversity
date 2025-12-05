import random
from turtledemo.penrose import inflatedart

from matplotlib import pyplot as plt

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
        print(f"!!! STAGNATION DETECTED at gen {i}. KICKING POPULATION (RANDOM) !!!")

        # ИЗМЕНЕНИЕ: Выбираем 20 СЛУЧАЙНЫХ индексов
        # range(2, 100) означает, что мы берем индексы от 2 до 99 (не трогаем элиту 0 и 1)
        indices_to_kick = random.sample(range(2, len(next_gen_routes)), 20)

        for k in indices_to_kick:
            # Мутируем выбранных счастливчиков
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
# Last list of dict and first dict in this list
Algorithms.info(list_of_dict_best_solutions[-1][0])

# ---------------- GRAPH ----------------
# Тут рисуется график для Task 18
best_fitnesses = []
for top3 in list_of_dict_best_solutions:
    best_fit = list(top3[0].values())[0]
    best_fitnesses.append(best_fit)

plt.figure(figsize=(10, 6))
plt.plot(best_fitnesses, marker='o', markersize=3)
plt.title(f"Genetic Algorithm Progress ({len(best_fitnesses)} epochs)")
plt.xlabel("Epoch")
plt.ylabel("Best Fitness (Distance)")
plt.grid(True)
# plt.show() # Можно закомментировать, чтобы показать оба графика в конце


print("\n------------------------TASK 20: Comparing Parameters----------------")
# Мы будем сравнивать влияние РАЗМЕРА ПОПУЛЯЦИИ на качество решения.
# Запустим алгоритм 3 раза: для 50, 100 и 200 особей.

parameters_to_test = [50, 100, 200]
comparison_histories = {}  # Словарь для хранения историй всех прогонов

for pop_size in parameters_to_test:
    print(f"Testing Population Size: {pop_size}...")

    # 1. Создаем начальную популяцию нужного размера
    pop_task20 = Algorithms.population_task12(current_file, pop_size, 5)

    # 2. Конвертация
    pop_list_20 = [list(r) for r in Algorithms.convert_dict_to_list(pop_task20)]

    # 3. Первая эпоха
    curr_pop_dicts_20, best_res_20 = Algorithms.epoch(pop_list_20, pop_size)

    # История для графика
    history_20 = []
    first_fit_20 = list(best_res_20[0].values())[0]
    history_20.append(first_fit_20)

    # Переменные цикла
    gens_20 = 100
    stag_20 = 0
    last_fit_20 = first_fit_20

    # 4. Цикл эволюции
    for i in range(gens_20):
        next_routes_20 = [list(list(d.keys())[0]) for d in curr_pop_dicts_20]

        # --- Kick (Динамический диапазон СЛУЧАЙНЫЙ) ---
        if stag_20 > 5:
            # Рассчитываем, сколько особей мутировать (25% от популяции)
            num_to_kick = int(pop_size * 0.25)

            # Берем случайные индексы, исключая элиту (0, 1)
            # range(2, len) - это пул доступных индексов
            indices_to_kick = random.sample(range(2, len(next_routes_20)), num_to_kick)

            for k in indices_to_kick:
                next_routes_20[k] = Algorithms.inversion_mutation(next_routes_20[k], 0.8)

            stag_20 = 0

        # Запуск Эпохи
        curr_pop_dicts_20, best_res_20 = Algorithms.epoch(next_routes_20, pop_size)

        # Запись результата
        curr_fit_20 = list(best_res_20[0].values())[0]
        history_20.append(curr_fit_20)

        # Проверка застоя
        if abs(curr_fit_20 - last_fit_20) < 0.001:
            stag_20 += 1
        else:
            stag_20 = 0
            last_fit_20 = curr_fit_20

    # Сохраняем историю
    comparison_histories[pop_size] = history_20
    print(f"Finished Size {pop_size}. Best Result: {history_20[-1]:.2f}")

# --- ГРАФИК СРАВНЕНИЯ (Task 19/20) ---
plt.figure(figsize=(12, 7))

# Рисуем линию для каждого размера популяции
for size, history in comparison_histories.items():
    plt.plot(history, label=f"Pop Size {size} (Best: {history[-1]:.0f})")

plt.title("Comparison of Different Initial Parameters (Population Size)")
plt.xlabel("Epoch")
plt.ylabel("Distance")
plt.legend()  # Показывает легенду (какой цвет что значит)
plt.grid(True)
plt.show()