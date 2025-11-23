# class Algorithms:
#
#     @staticmethod
#     def greedy_algorithm(routes, starting_city):
#         internal_routes = routes.copy()
#         internal_routes.remove(starting_city)
#
#         path = [starting_city]
#         current_city = starting_city
#
#         while internal_routes:
#             min_city = None
#             min_dist = float('inf')
#
#             for route in internal_routes:
#                 dist = current_city.distance_to(route)
#                 if dist < min_dist:
#                     min_dist = dist
#                     min_city = route
#
#             path.append(min_city)
#             current_city = min_city
#             internal_routes.remove(current_city)
#
#         fitness = calculate_fitness(path)
#         result = {tuple(path): fitness}
#         return result
#
#     @staticmethod
#     def find_best_starting_city_greedy(coordinates):
#         best_city = None
#         best_fitness = float('inf')
#
#         for city in coordinates:
#             result = Algorithms.greedy_algorithm(coordinates, city)
#             path, fitness = list(result.items())[0]
#
#             info(result)
#
#             if fitness < best_fitness:
#                 best_fitness = fitness
#                 best_city = path[0]
#
#         return best_city, best_fitness
