import random
from random import sample


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

            Algorithms.info(result)

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

        print("ROUTES MAP")
        Algorithms.info(routes_map)

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

        result = {}

        for _ in range(greedy_sol):
            rand = random.randint(0, len(initial_data) - 1)
            city_to_start = initial_data[rand]
            curr = Algorithms.greedy_algorithm(initial_data, city_to_start)
            result.update(curr)

        for _ in range(population_sol):
            curr = Algorithms.generate_random_route(initial_data)
            fitness = Algorithms.calculate_fitness(curr)
            result[tuple(curr)] = fitness

        return result



