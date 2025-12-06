import random

class Algorithms:

    @staticmethod
    def calculate_fitness(solution):
        total_distance = 0.0
        for i in range(len(solution) - 1):
            total_distance += solution[i].distance_to(solution[i + 1])
        total_distance += solution[-1].distance_to(solution[0])
        return total_distance

    @staticmethod
    def info(routes):
        if isinstance(routes, dict):
            for path, fitness in routes.items():
                for city in path:
                    print(f"{city.number} -> ", end="")
                print(path[0].number)
                print(f"Fitness: {fitness:.2f}")
                print("-" * 30)
        elif isinstance(routes, list):
            for city in routes:
                print(f"{city.number} -> ", end="")
            print(routes[0].number)
            print("Fitness: N/A")
            print("-" * 30)
        else:
            print("Unsupported type")

    @staticmethod
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

        fitness = Algorithms.calculate_fitness(path)
        result = {tuple(path): fitness}
        return result

    @staticmethod
    def best_greedy_starting_city(coordinates):
        best_city = None
        best_fitness = float('inf')

        for city in coordinates:
            result = Algorithms.greedy_algorithm(coordinates, city)
            path, fitness = list(result.items())[0]

            # Algorithms.info(result)

            if fitness < best_fitness:
                best_fitness = fitness
                best_city = path[0]

        return best_city, best_fitness

    @staticmethod
    def random_routes_analysis(coordinates, n=100):
        best_route_map = {}
        routes_map = {}

        for i in range(n + 1):
            current_route = Algorithms.generate_random_route(coordinates)
            current_fitness = Algorithms.calculate_fitness(current_route)

            route_key = tuple(
                current_route)
            routes_map[route_key] = current_fitness

            # updating
            if len(best_route_map) == 0 or current_fitness < list(best_route_map.values())[0]:
                best_route_map = {route_key: current_fitness}
        # print("ROUTES MAP")
        # Algorithms.info(routes_map)

        print("Best route by 100 randoms choice:")
        Algorithms.info(best_route_map)

        return best_route_map, routes_map

    @staticmethod
    def generate_random_route(cities):
        solution = cities.copy()
        random.shuffle(solution)
        return solution

    @staticmethod
    def population_task12(initial_data, population_sol, greedy_sol):
        if (population_sol < 1 and greedy_sol < 1) or (population_sol < 1):
            raise ValueError("Population size must be greater than or equal to 1")
        if greedy_sol > len(initial_data):
            raise ValueError("Quantity of greedy sol must be less than or equal to population size")

        result = {}

        while len(result) < greedy_sol:
            rand = random.randint(0, len(initial_data) - 1)
            city_to_start = initial_data[rand]
            curr = Algorithms.greedy_algorithm(initial_data, city_to_start)
            result.update(curr)

        while len(result) < population_sol :
            curr = Algorithms.generate_random_route(initial_data)
            fitness = Algorithms.calculate_fitness(curr)
            result[tuple(curr)] = fitness

        return result

    @staticmethod
    def info_task13(population):
        print("Population size:", len(population))

        best_result = None
        worst_result = None

        for route in population:
            fitness = Algorithms.calculate_fitness(route)

            if best_result is None or fitness < list(best_result.values())[0]:
                best_result = {tuple(route): fitness}
            if worst_result is None or fitness > list(worst_result.values())[0]:
                worst_result = {tuple(route): fitness}

        print("Best route:")
        Algorithms.info(best_result)

        print("Worst route:")
        Algorithms.info(worst_result)

    #Tournament selection : n stands for how much randomly chosen cities will take part in tournament
    #Takes list of population not dict
    @staticmethod
    def tournament_task14(population, n):
        randomly_chosen_routes = []

        winner = None
        best_fitness = float('inf')

        left_routes = population.copy()
        for _ in range( n+1 ):
            route = random.choice(left_routes)
            left_routes.remove(route)
            randomly_chosen_routes.append(route)

        for route in randomly_chosen_routes:
            curr_fitness = Algorithms.calculate_fitness(route)
            if curr_fitness < best_fitness:
                winner = route
                best_fitness = curr_fitness
        return winner, best_fitness

    @staticmethod
    def convert_dict_to_list(routes_fitness):
        return list(routes_fitness.keys())

    @staticmethod
    def PMX_alg(route1, route2):
        size = len(route1)
        # randomly chosen segment
        start = random.randint(0, size - 2)
        end = random.randint(start + 1, size - 1)

        child = [None] * size

        # 1) copy segment from parent1
        child[start:end+1] = route1[start:end+1]

        # 2) FIlling positions from parent2
        for i in range(size):
            if child[i] is not None:
                continue
            #parent1 = [A, B, C, D, E, F, G, H]
            #parent2 = [D, C, F, B, H, A, G, E]
            #child = [None, None, C, D, E, None, None, None]
            candidate = route2[i]

            # if candidate already in child, then look replacement in parent2
            while candidate in child:
                j = route2.index(candidate)  # returns index of candidate в parent2
                candidate = route1[j]  # taking city from parent1 in the same position


            child[i] = candidate

        return child

    @staticmethod
    def add_elite(old_best, new_population, elite_count):
        """
        old_best: list of dict {route_tuple : fitness}
        new_population: list of dict {route_tuple : fitness}
        elite_count: how much we need to insert
        """

        # if best < than needed add all of them
        limit = elite_count
        if len(old_best) < elite_count:
            limit = len(old_best)

        # adding
        for i in range(limit):
            new_population.append(old_best[i])

        return new_population

    @staticmethod
    def inversion_mutation(route, mutation_rate=0.1):

        if random.random() > mutation_rate:
            return route

        # converting to list bcs it can be passed as tuple
        child = list(route)

        # 2 random indexes
        idx1, idx2 = random.sample(range(len(child)), 2)

        start = min(idx1, idx2)
        end = max(idx1, idx2)

        # Reverse the segment
        child[start:end + 1] = child[start:end + 1][::-1]

        return child

    @staticmethod
    def two_opt_optimize(route):
        # converting to list bcs it can be passed as dict
        best_route = list(route)

        improved = True
        count = 0
        max_checks = 200

        while improved and count < max_checks:
            improved = False
            count += 1
            for i in range(1, len(route) - 2):
                for j in range(i + 1, len(route)):
                    if j - i == 1: continue

                    new_route = best_route[:]
                    # now it works like that :  best_route — is list
                    new_route[i:j] = best_route[i:j][::-1]

                    if Algorithms.calculate_fitness(new_route) < Algorithms.calculate_fitness(best_route):
                        best_route = new_route
                        improved = True
                        break
                if improved: break
        return best_route
    @staticmethod
    def ordered_crossover(parent1, parent2):
        size = len(parent1)
        start, end = sorted(random.sample(range(size), 2))

        child = [None] * size

        # 1. Copy segment from 1rst parent
        child[start:end + 1] = parent1[start:end + 1]

        # 2. Filling left places with second parent
        # following rules after first segment
        p2_index = (end + 1) % size
        c_index = (end + 1) % size

        while None in child:
            current_city = parent2[p2_index]

            # if city is not in child then add
            if current_city not in child:
                child[c_index] = current_city
                c_index = (c_index + 1) % size

            p2_index = (p2_index + 1) % size

        return child

    @staticmethod
    def epoch(initial_population_list, size, mutation_rate=0.1):
        new_population = []


        # --- step 1: sorting
        temp_list = []
        for i in range(len(initial_population_list)):
            route = initial_population_list[i]
            fitness = Algorithms.calculate_fitness(route)
            temp_list.append([fitness, i, route])
        temp_list.sort()
        sorted_routes = []
        for item in temp_list:
            route = item[2]
            sorted_routes.append(route)

        # --- step 2: elite ---
        elite_count = 2
        for i in range(elite_count):
            elite_route = sorted_routes[i]
            new_population.append(elite_route)

        # --- step 3: crossover and mutation ---
        while len(new_population) < size:
            parent1 = Algorithms.tournament_task14(initial_population_list, 5)[0]
            parent2 = Algorithms.tournament_task14(initial_population_list, 5)[0]

            child = Algorithms.ordered_crossover(list(parent1), list(parent2))

            child = Algorithms.inversion_mutation(child, mutation_rate=mutation_rate)

            new_population.append(child)

        # 2-opt
        best_candidate = new_population[0]
        optimized_best = Algorithms.two_opt_optimize(best_candidate)
        new_population[0] = optimized_best

        result_dicts = []
        for route in new_population:
            fit = Algorithms.calculate_fitness(route)
            entry = {tuple(route): fit}
            result_dicts.append(entry)

        best_three = []
        for i in range(3):
            best_three.append(result_dicts[i])

        return result_dicts, best_three