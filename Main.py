import random


from matplotlib import pyplot as plt
import statistics
from Algorithms import Algorithms
from Parser import Parser

"-------------------------TASK4-----------------------------------"
coordinates_berlin_11 = Parser.read_tsp_file("/Users/rusleak/Downloads/berlin11_modified.tsp")
coordinates_berlin_52 = Parser.read_tsp_file("/Users/rusleak/Downloads/berlin52.tsp")
coordinates_berlin_100 = Parser.read_tsp_file("/Users/rusleak/Downloads/kro100A.tsp")
coordinates_berlin_150 = Parser.read_tsp_file("/Users/rusleak/Downloads/kroA150.tsp")

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


# ---------------------------------------------------------
# INSERT THIS AT THE END OF YOUR SCRIPT (REPLACING TASK 20)
# ---------------------------------------------------------

def run_experiment(coordinates, pop_size, mut_rate, generations=100, seed_val=42):
    """
    Runs the GA with specific parameters and returns the history of best fitnesses.
    """
    # 1. Set seed for fairness (so every test starts with same random conditions)
    random.seed(seed_val)

    # 2. Initialize
    # We use 5 greedy solutions, rest are random
    greedy_count = 5
    if pop_size <= 5: greedy_count = 1

    pop_dict = Algorithms.population_task12(coordinates, pop_size, greedy_count)
    pop_list = [list(r) for r in Algorithms.convert_dict_to_list(pop_dict)]

    history = []

    # Initial best
    current_dicts, best_res = Algorithms.epoch(pop_list, pop_size, mutation_rate=mut_rate)
    best_fit = list(best_res[0].values())[0]
    history.append(best_fit)

    stagnation = 0
    last_best = best_fit

    for i in range(generations):
        # Prepare list for next epoch
        next_routes = [list(list(d.keys())[0]) for d in current_dicts]

        # --- Stagnation Kick Logic ---
        if stagnation > 10:  # If stuck for 10 gens
            # Mutate 30% of population heavily
            kick_size = int(pop_size * 0.3)
            indices = random.sample(range(2, len(next_routes)), kick_size)
            for k in indices:
                # Strong mutation to break stagnation
                next_routes[k] = Algorithms.inversion_mutation(next_routes[k], mutation_rate=0.8)
            stagnation = 0

        # Run Epoch
        current_dicts, best_res = Algorithms.epoch(next_routes, pop_size, mutation_rate=mut_rate)

        current_best = list(best_res[0].values())[0]
        history.append(current_best)

        if abs(current_best - last_best) < 0.001:
            stagnation += 1
        else:
            stagnation = 0
            last_best = current_best

    return history


print("\n--- RUNNING PART 2 EXPERIMENTS ---")
coords = current_file  # Make sure this is set to berlin52 or kroA150

# --- EXPERIMENT 1: POPULATION SIZE ---
print("Testing Population Sizes...")
pop_sizes = [50, 100, 200]
results_pop = {}

for p in pop_sizes:
    # Fixed mutation 0.1, variable population
    hist = run_experiment(coords, pop_size=p, mut_rate=0.1, generations=150, seed_val=10)
    results_pop[p] = hist
    print(f"Pop {p} finished. Best: {hist[-1]:.2f}")

plt.figure(figsize=(10, 6))
for p, h in results_pop.items():
    plt.plot(h, label=f"Pop Size {p} (Best: {h[-1]:.0f})")
plt.title("Impact of Population Size (Mutation=0.1)")
plt.xlabel("Generation")
plt.ylabel("Distance")
plt.legend()
plt.grid(True)
plt.show()

# --- EXPERIMENT 2: MUTATION RATE ---
print("\nTesting Mutation Rates...")
mut_rates = [0.01, 0.2, 0.5]
results_mut = {}

for m in mut_rates:
    # Fixed population 100, variable mutation
    hist = run_experiment(coords, pop_size=100, mut_rate=m, generations=150, seed_val=10)
    results_mut[m] = hist
    print(f"Mut {m} finished. Best: {hist[-1]:.2f}")

plt.figure(figsize=(10, 6))
for m, h in results_mut.items():
    plt.plot(h, label=f"Mutation {m} (Best: {h[-1]:.0f})")
plt.title("Impact of Mutation Rate (PopSize=100)")
plt.xlabel("Generation")
plt.ylabel("Distance")
plt.legend()
plt.grid(True)
plt.show()


def run_part3_comparison(coordinates):
    print("\n" + "=" * 50)
    print("STARTING PART 3: COMPARISON ANALYSIS")
    print("=" * 50)

    # --- 1. RANDOM SEARCH (1000 runs) ---
    print("\n[1/3] Running Random Search (1000 iterations)...")
    random_results = []
    for _ in range(1000):
        r = Algorithms.generate_random_route(coordinates)
        fit = Algorithms.calculate_fitness(r)
        random_results.append(fit)

    rand_best = min(random_results)
    rand_mean = statistics.mean(random_results)
    rand_stdev = statistics.stdev(random_results)
    rand_var = statistics.variance(random_results)

    print(f"Random Search Done.")
    print(f"Best: {rand_best:.2f} | Mean: {rand_mean:.2f} | StDev: {rand_stdev:.2f}")

    # --- 2. GREEDY ALGORITHM (All cities as start) ---
    print("\n[2/3] Running Greedy Algorithm (for every city)...")
    greedy_results = []

    # Run greedy starting from EACH city in the list
    for start_city in coordinates:
        res = Algorithms.greedy_algorithm(coordinates, start_city)
        fit = list(res.values())[0]
        greedy_results.append(fit)

    greedy_results.sort()  # Sort to find best easily

    greedy_best_5 = greedy_results[:5]
    greedy_mean = statistics.mean(greedy_results)
    greedy_stdev = statistics.stdev(greedy_results)
    greedy_var = statistics.variance(greedy_results)

    print(f"Greedy Done.")
    print(f"Best 5: {[round(x, 2) for x in greedy_best_5]}")
    print(f"Mean: {greedy_mean:.2f} | StDev: {greedy_stdev:.2f}")

    # --- 3. GENETIC ALGORITHM (10 runs with best parameters) ---
    print("\n[3/3] Running Genetic Algorithm (10 runs)...")
    # Parameters from Part 2 results
    pop_size = 100
    mut_rate = 0.2
    generations = 100

    ga_results = []

    for i in range(10):
        # Using a distinct seed for each run to get variation
        run_seed = i * 50

        # We reuse the logic from run_experiment but only need the final value
        # Silent run (no plotting inside loop)
        history = run_experiment(coordinates, pop_size, mut_rate, generations, seed_val=run_seed)
        final_fit = history[-1]

        ga_results.append(final_fit)
        print(f"  -> Run {i + 1}/10 finished. Result: {final_fit:.2f}")

    ga_best = min(ga_results)
    ga_mean = statistics.mean(ga_results)
    ga_stdev = statistics.stdev(ga_results)
    ga_var = statistics.variance(ga_results)

    # --- PRINTING FINAL TABLE FOR REPORT ---
    print("\n" + "=" * 60)
    print(f"{'METRIC':<20} | {'RANDOM (1000)':<15} | {'GREEDY (All)':<15} | {'GA (10 runs)':<15}")
    print("-" * 60)
    print(f"{'Best Result':<20} | {rand_best:<15.2f} | {greedy_results[0]:<15.2f} | {ga_best:<15.2f}")
    print(f"{'Average (Mean)':<20} | {rand_mean:<15.2f} | {greedy_mean:<15.2f} | {ga_mean:<15.2f}")
    print(f"{'Standard Deviation':<20} | {rand_stdev:<15.2f} | {greedy_stdev:<15.2f} | {ga_stdev:<15.2f}")
    print(f"{'Variance':<20} | {rand_var:<15.2f} | {greedy_var:<15.2f} | {ga_var:<15.2f}")
    print("=" * 60)

    print("\nGreedy Best 5 Results:", [round(x, 2) for x in greedy_best_5])
    print("GA All 10 Results:    ", [round(x, 2) for x in ga_results])


# Execute Part 3
run_part3_comparison(current_file)